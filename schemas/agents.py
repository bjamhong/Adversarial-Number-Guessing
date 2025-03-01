from pydantic import BaseModel

class NumberChoicesResponse(BaseModel):
    scratchpad: str
    choices: list[int]

class NumberChoiceResponse(BaseModel):
    scratchpad: str
    choice: int

class RandomNumberResponse(BaseModel):
    choice: int