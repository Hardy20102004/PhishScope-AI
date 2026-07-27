from datetime import datetime, timezone
import hashlib
import json
from loguru import logger
from sqlalchemy.orm import Session

from app.ti_feed.models import FeedRegistry, FeedVersion, SyncStatus, FeedIndicator, FeedAuditLog
from app.ti_feed.connectors.stix_rest import STIX21RESTConnector
from app.ti_feed.connectors.csv_import import CSVImportConnector
from app.ti_feed.validation import FeedValidator
from app.ti_feed.normalization import FeedNormalizer
from app.ti_feed.enrichment import FeedEnrichmentEngine

from app.ioc_engine.correlation import IOCCorrelationEngine
from app.ioc_engine.schemas import IndicatorCreate

class FeedScheduler:
    """
    Orchestrates the synchronization of feeds.
    """

    def __init__(self, db: Session):
        self.db = db
        self.enrichment_engine = FeedEnrichmentEngine(db)
        self.correlation_engine = IOCCorrelationEngine(db)

    def _get_connector(self, feed: FeedRegistry):
        if feed.format == "STIX 2.1":
            return STIX21RESTConnector(feed)
        elif feed.format == "CSV":
            return CSVImportConnector(feed)
        else:
            raise ValueError(f"Unsupported feed format: {feed.format}")

    def sync_feed(self, feed_id: str):
        """
        Executes a synchronization run for a specific feed.
        """
        feed = self.db.query(FeedRegistry).filter(FeedRegistry.id == feed_id).first()
        if not feed:
            logger.error(f"Feed {feed_id} not found.")
            return

        # 1. Create a FeedVersion (Execution Context)
        version = FeedVersion(feed_id=feed.id, status=SyncStatus.IN_PROGRESS)
        self.db.add(version)
        self.db.commit()
        self.db.refresh(version)
        
        self._log_audit(feed.id, version.id, "INFO", "Started feed synchronization")

        try:
            connector = self._get_connector(feed)
            connector.connect()
            
            indicators_processed = 0
            errors = 0
            
            # 2. Fetch Data (Incremental if possible)
            # In a real app, use feed.last_sync_at to pass a `since` parameter
            for raw_record in connector.fetch():
                try:
                    # 3. Validate
                    is_valid, reason = FeedValidator.validate_indicator(raw_record)
                    if not is_valid:
                        self._log_audit(feed.id, version.id, "WARNING", f"Validation failed: {reason}", details={"raw": raw_record})
                        errors += 1
                        continue

                    # 4. Normalize to Internal Structure
                    extracted_value, internal_type = FeedNormalizer.normalize_to_internal(raw_record)
                    
                    # 5. Delegate to IOC Correlation Engine
                    ioc_create = IndicatorCreate(
                        value=extracted_value,
                        type=internal_type,
                        source_module=f"TI_Feed_{feed.name}",
                        raw_context=raw_record.get("raw_data", {})
                    )
                    
                    # The correlation engine handles ingestion, correlation, and KG sync
                    indicator = self.correlation_engine.ingest_indicator(ioc_create)
                    
                    # 6. Enrich (Post-correlation or pre-correlation depending on architecture)
                    # We do it post-ingest here to add tags to the DB record
                    indicator = self.enrichment_engine.enrich_indicator(indicator)
                    self.db.add(indicator)

                    # 7. Link to Feed History
                    feed_indicator = FeedIndicator(
                        feed_id=feed.id,
                        version_id=version.id,
                        global_indicator_id=indicator.id,
                        raw_data=raw_record.get("raw_data", {})
                    )
                    self.db.add(feed_indicator)
                    
                    indicators_processed += 1
                    
                    # Batch commit to save memory
                    if indicators_processed % 100 == 0:
                        self.db.commit()
                        
                except Exception as e:
                    logger.error(f"Error processing record in feed {feed.name}: {e}")
                    errors += 1
            
            # Final commit
            self.db.commit()

            # 8. Finalize Version
            version.status = SyncStatus.COMPLETED if errors == 0 else SyncStatus.PARTIAL
            version.indicators_added = indicators_processed # Simplifying logic here (added vs updated)
            version.errors_encountered = errors
            version.completed_at = datetime.now(timezone.utc)
            
            # Create a mock hash for version tracking
            version.version_hash = hashlib.sha256(f"{feed.id}_{version.completed_at}".encode()).hexdigest()

            feed.last_sync_at = version.completed_at
            feed.status = "Active"
            
            self._log_audit(feed.id, version.id, "INFO", f"Sync completed. Processed {indicators_processed}, Errors {errors}")
            self.db.commit()

        except Exception as e:
            logger.error(f"Feed sync failed for {feed.name}: {e}")
            version.status = SyncStatus.FAILED
            version.completed_at = datetime.now(timezone.utc)
            feed.status = "Error"
            self._log_audit(feed.id, version.id, "ERROR", f"Sync failed: {str(e)}")
            self.db.commit()

    def _log_audit(self, feed_id, version_id, level, message, details=None):
        log = FeedAuditLog(feed_id=feed_id, version_id=version_id, level=level, message=message, details=details)
        self.db.add(log)
        # Note: caller must commit
