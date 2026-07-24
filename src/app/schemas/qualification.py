from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class CallCategory(str, Enum):
    EMERGENCY = "urgence"
    APPOINTMENT = "rendez-vous"
    QUOTE = "devis"
    INFORMATION = "informations"
    ADMINISTRATIVE = "administratif"
    LABORATORY = "laboratoire"
    PHARMACY = "pharmacie"
    UNKNOWN = "inconnue"


class QualificationAction(str, Enum):
    TRANSFER_IMMEDIATELY = "TRANSFER_IMMEDIATELY"
    ROUTE_TO_APPOINTMENT_SERVICE = "ROUTE_TO_APPOINTMENT_SERVICE"
    ROUTE_TO_QUOTE_SERVICE = "ROUTE_TO_QUOTE_SERVICE"
    SEARCH_FAQ = "SEARCH_FAQ"
    ROUTE_TO_ADMINISTRATIVE_SERVICE = "ROUTE_TO_ADMINISTRATIVE_SERVICE"
    ROUTE_TO_LAB_SERVICE = "ROUTE_TO_LAB_SERVICE"
    ROUTE_TO_PHARMACY_SERVICE = "ROUTE_TO_PHARMACY_SERVICE"
    TRANSFER_TO_HUMAN = "TRANSFER_TO_HUMAN"
    ANSWER_WITH_FAQ = "ANSWER_WITH_FAQ"


class CallEntry(BaseModel):
    call_id: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=5000)
    language: str = "fr"
    patient_id: str | None = None
    context: dict[str, Any] | None = None
    created_at: datetime | None = None


class ClassificationResult(BaseModel):
    call_id: str
    category: CallCategory
    confidence: float = Field(ge=0, le=1)
    is_emergency: bool
    action: QualificationAction
    category_scores: dict[str, float] | None = None
    model_name: str
    model_version: str
    processing_time_ms: int = Field(ge=0)


class FAQResponse(BaseModel):
    matched: bool
    matched_faq_id: int | None = None
    question: str | None = None
    answer: str | None = None
    confidence: float = Field(ge=0, le=1)
    action: QualificationAction


class QualificationResponse(BaseModel):
    classification: ClassificationResult
    faq: FAQResponse | None = None