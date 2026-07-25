from typing import List, Dict, Any

class ReputationEngine:
    """Calculates overall reputation and confidence from multiple feeds."""
    
    # Weight of each feed in the final score (0.0 to 1.0)
    FEED_WEIGHTS = {
        "virustotal": 0.8,
        "google_safe_browsing": 0.9,
        "abuseipdb": 0.7,
        "phish_tank": 0.8,
        "internal": 1.0
    }

    @classmethod
    def calculate(cls, feed_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate reputation based on feed results.
        Returns a dict with `reputation_score`, `confidence`, and `threat_classification`.
        
        feed_results: List of dicts, each with 'source', 'reputation_score' (0-100), and 'confidence' (0-100)
        """
        if not feed_results:
            return {
                "reputation_score": 0.0,
                "confidence_score": 0.0,
                "threat_classification": None
            }
            
        total_weighted_score = 0.0
        total_weight = 0.0
        total_confidence = 0.0
        
        malicious_votes = 0
        
        for result in feed_results:
            source = result.get('source', 'unknown')
            score = result.get('reputation_score', 0.0)
            conf = result.get('confidence', 0.0)
            
            weight = cls.FEED_WEIGHTS.get(source, 0.5)
            
            total_weighted_score += (score * weight)
            total_weight += weight
            total_confidence += conf
            
            if score > 50:
                malicious_votes += 1
                
        if total_weight == 0:
            return {
                "reputation_score": 0.0,
                "confidence_score": 0.0,
                "threat_classification": None
            }
            
        final_score = total_weighted_score / total_weight
        avg_confidence = total_confidence / len(feed_results)
        
        # Determine classification
        classification = None
        if final_score > 75:
            classification = "Malicious"
        elif final_score > 50:
            classification = "Suspicious"
        elif final_score > 0:
            classification = "Low Risk"
        else:
            classification = "Safe"
            
        return {
            "reputation_score": round(final_score, 2),
            "confidence_score": round(avg_confidence, 2),
            "threat_classification": classification
        }
