from datetime import datetime
from pydantic import BaseModel, Field


class TermBase(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=120)
    description: str = Field(..., min_length=1, max_length=4000)


class TermCreate(TermBase):
    pass


class TermUpdate(BaseModel):
    description: str | None = Field(None, min_length=1, max_length=4000)


class TermOut(TermBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


