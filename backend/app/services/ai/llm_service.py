import abc
import asyncio
from typing import Dict, List


class LLMService(abc.ABC):
    @abc.abstractmethod
    async def generate_response(self, system_prompt: str, messages: List[Dict[str, str]], context: str) -> str:
        """Generate a response based on the conversation history and context."""
        pass
        
    @abc.abstractmethod
    async def generate_report(self, system_prompt: str, context: str) -> str:
        """Generate a structured report from context."""
        pass

class MockLLMService(LLMService):
    """A simulated LLM service for testing and development."""
    
    async def generate_response(self, system_prompt: str, messages: List[Dict[str, str]], context: str) -> str:
        await asyncio.sleep(1.0) # Simulate network latency
        last_message = messages[-1]["content"].lower() if messages else ""
        
        if "summarize" in last_message:
            return "Based on the evidence provided, this investigation targets a URL that has been flagged as suspicious. The threat intel indicates a reputation score below 50 in some feeds. \n\n**Evidence cited:** Threat intel reputation metrics."
        
        if "recommend" in last_message:
            return "I recommend pivoting on the IP address observed in the DNS records to identify related infrastructure. \n\n**Evidence cited:** Associated IP address in URL findings."
            
        return f"This is a simulated AI response. I have analyzed the provided context which contains {len(context)} characters. I note that this investigation requires further evidence gathering."

    async def generate_report(self, system_prompt: str, context: str) -> str:
        await asyncio.sleep(2.0)
        return """# Investigation Report
        
## Executive Summary
This report summarizes the findings of the investigation. The target exhibits characteristics common to social engineering campaigns.

## Technical Details
- **Risk Level**: Elevated
- **Indicators Observed**: Multiple suspicious indicators were flagged by Threat Intelligence.

## Recommendations
1. Block the associated domain at the proxy level.
2. Search internal logs for interaction with this IOC.
"""
