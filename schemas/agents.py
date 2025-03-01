from pydantic import BaseModel

class NumberChoicesResponse(BaseModel):
    scratchpad: str
    choices: list[int]

class RandomNumberResponse(BaseModel):
    choice: int