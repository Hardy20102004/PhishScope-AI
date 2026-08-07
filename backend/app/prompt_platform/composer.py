from typing import Any, Dict, Tuple

import jinja2
import structlog

logger = structlog.get_logger("phoenix.prompt_platform.composer")

class PromptComposer:
    def __init__(self):
        # We use strict undefined to fail fast if variables are missing
        self.env = jinja2.Environment(undefined=jinja2.StrictUndefined)

    def compose(self, system_template: str, user_template: str, variables: Dict[str, Any]) -> Tuple[str, str]:
        """
        Dynamically renders the template strings using Jinja2 with provided variables.
        Supports loops, conditions, and complex nested dictionaries.
        """
        try:
            sys_t = self.env.from_string(system_template)
            usr_t = self.env.from_string(user_template)
            
            rendered_system = sys_t.render(**variables)
            rendered_user = usr_t.render(**variables)
            
            return rendered_system, rendered_user
            
        except jinja2.exceptions.TemplateError as e:
            logger.error("template_rendering_failed", error=str(e))
            raise ValueError(f"Failed to render prompt template: {str(e)}")
