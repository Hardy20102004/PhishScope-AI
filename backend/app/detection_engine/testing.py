import uuid
from sqlalchemy.ext.asyncio import AsyncSession
import random

from app.models.detection import RuleTestResult

class RuleTestingEngine:
    """
    Mocks testing logic for rules against historical or synthetic data.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute_test(self, rule_id: uuid.UUID, version_id: uuid.UUID, dataset_name: str) -> RuleTestResult:
        """
        Executes a test and records the result.
        """
        # Mock logic: Generate random test results
        coverage = round(random.uniform(70.0, 100.0), 2)
        fps = random.randint(0, 5)
        fns = random.randint(0, 2)
        exec_time = random.randint(10, 500)
        
        passed = (fps <= 2) and (coverage >= 80.0)
        
        test_result = RuleTestResult(
            rule_id=rule_id,
            version_id=version_id,
            dataset_name=dataset_name,
            coverage_score=coverage,
            false_positives=fps,
            false_negatives=fns,
            execution_time_ms=exec_time,
            passed=passed
        )
        
        self.db.add(test_result)
        await self.db.commit()
        await self.db.refresh(test_result)
        
        return test_result
