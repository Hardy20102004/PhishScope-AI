import pytest

from app.prompt_platform.composer import PromptComposer


def test_prompt_composer():
    composer = PromptComposer()
    
    system = "You are an assistant for {{ company }}."
    user = "My name is {{ name }}. Welcome to {{ company }}."
    
    sys_out, user_out = composer.compose(system, user, {"company": "PHOENIX", "name": "Alice"})
    
    assert sys_out == "You are an assistant for PHOENIX."
    assert user_out == "My name is Alice. Welcome to PHOENIX."

def test_prompt_composer_missing_vars():
    composer = PromptComposer()
    system = "You are {{ company }}."
    
    with pytest.raises(ValueError) as exc:
        composer.compose(system, "Hello", {})
    assert "company" in str(exc.value)
