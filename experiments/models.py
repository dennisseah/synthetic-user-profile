from typing import Literal

from pydantic import BaseModel


class ProfileChoice(BaseModel):
    gender: Literal["male", "female"]
    state: str
    annual_income_k: int = 0
    generated: str | None = None


class Result(ProfileChoice):
    decision: float
