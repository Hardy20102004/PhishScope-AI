from typing import Any


class ProviderAdapter:
    """
    Adapts rendered System and User prompts into provider-specific schemas (e.g. OpenAI messages array vs Anthropic Claude XML layout).
    """
    
    @staticmethod
    def format_for_provider(system_text: str, user_text: str, provider: str = "openai") -> Any:
        provider_lower = provider.lower()
        
        if provider_lower in ["openai", "azure_openai", "mistral"]:
            return [
                {"role": "system", "content": system_text},
                {"role": "user", "content": user_text}
            ]
            
        elif provider_lower == "anthropic":
            # Claude often performs best with XML tags or distinct System parameters depending on the SDK version
            # Here we mock the Messages API layout.
            return {
                "system": system_text,
                "messages": [
                    {"role": "user", "content": user_text}
                ]
            }
            
        elif provider_lower == "gemini":
            return {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": f"System Instructions:\n{system_text}\n\nTask:\n{user_text}"}
                        ]
                    }
                ]
            }
            
        else:
            # Fallback for unknown
            return f"{system_text}\n\n{user_text}"
