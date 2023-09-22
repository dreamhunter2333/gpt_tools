from pydantic import BaseModel


class PromptBody(BaseModel):
    prompt: str
