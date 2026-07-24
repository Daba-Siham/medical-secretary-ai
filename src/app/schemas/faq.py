from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FAQBase(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=500,
    )

    answer: str = Field(
        min_length=3,
    )

    category: str = Field(
        min_length=2,
        max_length=100,
    )

    tags: list[str] = Field(
        default_factory=list,
    )

    active: bool = True


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: str | None = Field(
        default=None,
        min_length=3,
        max_length=500,
    )

    answer: str | None = Field(
        default=None,
        min_length=3,
    )

    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    tags: list[str] | None = None
    active: bool | None = None


class FAQRead(FAQBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)