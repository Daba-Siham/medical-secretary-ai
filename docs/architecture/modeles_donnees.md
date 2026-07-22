# Modèles de données du Module 4

## 1. Présentation

Ce document définit les principaux objets échangés par le Module 4 —
Qualification des appels et FAQ.

Les modèles présentés sont provisoires. Ils devront être validés avec les
responsables des Modules 1 et 3 avant l’intégration finale.

Les trois modèles principaux sont :

- `CallEntry` : demande reçue depuis le Module 3 ;
- `ClassificationResult` : résultat de la classification ;
- `FAQResponse` : résultat d’une recherche dans la FAQ.

---

## 2. CallEntry

`CallEntry` représente une demande transmise par le Module 3 au Module 4.

Dans le système final, le texte correspond à la transcription de la demande
formulée par le patient pendant l’appel.

### 2.1 Représentation JSON

```json
{
  "call_id": "CALL-0001",
  "text": "Je voudrais annuler mon rendez-vous de demain.",
  "language": "fr",
  "patient_id": null,
  "context": {
    "channel": "phone",
    "source_module": "module_3"
  },
  "created_at": "2026-07-22T14:30:00Z"
}
```

### 2.2 Description des champs

| Champ | Type | Obligatoire | Description |
|---|---|---:|---|
| `call_id` | string | Oui | Identifiant unique de l’appel |
| `text` | string | Oui | Texte de la demande du patient |
| `language` | string | Non | Langue de la demande |
| `patient_id` | string ou null | Non | Identifiant du patient lorsqu’il est disponible |
| `context` | object ou null | Non | Informations supplémentaires sur l’appel |
| `created_at` | datetime ou null | Non | Date et heure de création de la demande |

### 2.3 Modèle Python

```python
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CallEntry(BaseModel):
    call_id: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=5000)
    language: str = "fr"
    patient_id: str | None = None
    context: dict[str, Any] | None = None
    created_at: datetime | None = None
```

---

## 3. ClassificationResult

`ClassificationResult` représente le résultat retourné par le moteur de
classification.

Il contient notamment :

- la catégorie prédite ;
- le score de confiance ;
- l’indication d’urgence ;
- l’action à exécuter ;
- les informations sur le modèle utilisé.

### 3.1 Représentation JSON

```json
{
  "call_id": "CALL-0001",
  "category": "rendez-vous",
  "confidence": 0.94,
  "is_emergency": false,
  "action": "ROUTE_TO_APPOINTMENT_SERVICE",
  "category_scores": {
    "urgence": 0.01,
    "rendez-vous": 0.94,
    "devis": 0.01,
    "informations": 0.02,
    "administratif": 0.01,
    "laboratoire": 0.0,
    "pharmacie": 0.01
  },
  "model_name": "linear_svm",
  "model_version": "1.0.0",
  "processing_time_ms": 95
}
```

### 3.2 Description des champs

| Champ | Type | Obligatoire | Description |
|---|---|---:|---|
| `call_id` | string | Oui | Identifiant de l’appel concerné |
| `category` | string | Oui | Catégorie principale prédite |
| `confidence` | float | Oui | Score de confiance entre 0 et 1 |
| `is_emergency` | boolean | Oui | Indique si une urgence est détectée |
| `action` | string | Oui | Action à exécuter après la classification |
| `category_scores` | object ou null | Non | Scores obtenus pour chaque catégorie |
| `model_name` | string | Oui | Nom du modèle utilisé |
| `model_version` | string | Oui | Version du modèle |
| `processing_time_ms` | integer | Oui | Temps de traitement en millisecondes |

### 3.3 Catégories possibles

Les catégories provisoires sont :

```text
urgence
rendez-vous
devis
informations
administratif
laboratoire
pharmacie
inconnue
```

La catégorie `inconnue` est utilisée lorsque le score de confiance est
insuffisant.

### 3.4 Actions possibles

```text
TRANSFER_IMMEDIATELY
ROUTE_TO_APPOINTMENT_SERVICE
ROUTE_TO_QUOTE_SERVICE
SEARCH_FAQ
ROUTE_TO_ADMINISTRATIVE_SERVICE
ROUTE_TO_LAB_SERVICE
ROUTE_TO_PHARMACY_SERVICE
TRANSFER_TO_HUMAN
ANSWER_WITH_FAQ
```

### 3.5 Modèle Python

```python
from enum import Enum

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
```

---

## 4. FAQResponse

`FAQResponse` représente le résultat d’une recherche dans la bibliothèque
de questions fréquentes.

Ce modèle indique si une FAQ suffisamment proche a été trouvée.

### 4.1 Exemple avec réponse trouvée

```json
{
  "matched": true,
  "matched_faq_id": 12,
  "question": "Quels sont les horaires du cabinet ?",
  "answer": "Le cabinet est ouvert du lundi au vendredi de 8h30 à 18h00.",
  "confidence": 0.91,
  "action": "ANSWER_WITH_FAQ"
}
```

### 4.2 Exemple sans réponse fiable

```json
{
  "matched": false,
  "matched_faq_id": null,
  "question": null,
  "answer": null,
  "confidence": 0.38,
  "action": "TRANSFER_TO_HUMAN"
}
```

### 4.3 Description des champs

| Champ | Type | Obligatoire | Description |
|---|---|---:|---|
| `matched` | boolean | Oui | Indique si une FAQ fiable a été trouvée |
| `matched_faq_id` | integer ou null | Non | Identifiant de la FAQ sélectionnée |
| `question` | string ou null | Non | Question enregistrée dans la FAQ |
| `answer` | string ou null | Non | Réponse validée retournée au patient |
| `confidence` | float | Oui | Score de similarité entre 0 et 1 |
| `action` | string | Oui | Action à exécuter |

### 4.4 Modèle Python

```python
from pydantic import BaseModel, Field


class FAQResponse(BaseModel):
    matched: bool
    matched_faq_id: int | None = None
    question: str | None = None
    answer: str | None = None
    confidence: float = Field(ge=0, le=1)
    action: QualificationAction
```

---

## 5. Réponse globale du Module 4

La réponse finale du Module 4 peut réunir le résultat de classification et
la réponse FAQ.

Cette partie est facultative, mais elle permet de représenter clairement
la réponse complète de l’API.

### 5.1 Modèle Python

```python
class QualificationResponse(BaseModel):
    classification: ClassificationResult
    faq: FAQResponse | None = None
```

### 5.2 Exemple pour une demande traitée par la FAQ

```json
{
  "classification": {
    "call_id": "CALL-0003",
    "category": "informations",
    "confidence": 0.89,
    "is_emergency": false,
    "action": "ANSWER_WITH_FAQ",
    "category_scores": null,
    "model_name": "linear_svm",
    "model_version": "1.0.0",
    "processing_time_ms": 120
  },
  "faq": {
    "matched": true,
    "matched_faq_id": 12,
    "question": "Quels sont les horaires du cabinet ?",
    "answer": "Le cabinet est ouvert du lundi au vendredi de 8h30 à 18h00.",
    "confidence": 0.91,
    "action": "ANSWER_WITH_FAQ"
  }
}
```

---

## 6. Format des erreurs

Les erreurs doivent être retournées sous une forme structurée.

### 6.1 Exemple JSON

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Le texte de la demande est obligatoire.",
    "details": {
      "field": "text"
    }
  }
}
```

### 6.2 Modèle Python

```python
from typing import Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
```

---

## 7. Points à valider

Les éléments suivants devront être confirmés avec l’encadrant :

- le nom exact des champs transmis par le Module 3 ;
- le caractère obligatoire ou non de `patient_id` ;
- la longueur maximale du texte ;
- la présence des scores de toutes les catégories ;
- le format exact des dates ;
- la présence de la catégorie `inconnue` ;
- les actions définitives de routage ;
- la politique de conservation du texte reçu ;
- le format partagé des erreurs entre les modules.
