# Interfaces API REST — Module 4

## 1. Objectif

Ce document décrit les interfaces REST prévues pour le Module 4 —
Qualification des appels et FAQ.

Les contrats présentés sont provisoires. Ils devront être validés avec les
responsables des Modules 1 et 3 avant l’intégration finale.

L’API permet principalement :

- de qualifier une demande transmise par le Module 3 ;
- de rechercher une réponse dans la bibliothèque FAQ ;
- de consulter les FAQ ;
- d’ajouter une FAQ ;
- de modifier une FAQ ;
- de désactiver une FAQ ;
- de vérifier l’état du service.

---

## 2. Convention générale

### 2.1 URL de base

```text
/api/v1
```

### 2.2 Format des données

Les requêtes et les réponses utilisent le format :

```text
application/json
```

### 2.3 Authentification

L’authentification sera fournie par le Module 1.

Le mécanisme exact reste à valider.

Exemple provisoire :

```http
Authorization: Bearer <token>
```

### 2.4 Codes HTTP principaux

| Code | Signification |
|---|---|
| `200` | Requête traitée avec succès |
| `201` | Ressource créée avec succès |
| `204` | Requête réussie sans contenu retourné |
| `400` | Requête invalide |
| `401` | Authentification requise |
| `403` | Accès interdit |
| `404` | Ressource inexistante |
| `409` | Conflit ou ressource déjà existante |
| `422` | Données non valides |
| `500` | Erreur interne |
| `503` | Service temporairement indisponible |

---

# 3. Qualification d’une demande

## 3.1 Endpoint

```http
POST /api/v1/calls/classify
```

## 3.2 Objectif

Recevoir une demande textuelle, déterminer sa catégorie, calculer son score
de confiance et retourner l’action à exécuter.

## 3.3 Acteur appelant

```text
Module 3 — Système téléphonique
```

Dans le prototype, le Module 3 peut être simulé avec un mock.

## 3.4 Corps de la requête

Le corps correspond au modèle `CallEntry`.

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

## 3.5 Champs de la requête

| Champ | Type | Obligatoire | Description |
|---|---|---:|---|
| `call_id` | string | Oui | Identifiant unique de l’appel |
| `text` | string | Oui | Texte de la demande |
| `language` | string | Non | Langue utilisée |
| `patient_id` | string ou null | Non | Identifiant du patient |
| `context` | object ou null | Non | Contexte fourni par le module appelant |
| `created_at` | datetime ou null | Non | Date de création de la demande |

## 3.6 Réponse réussie — demande de rendez-vous

```http
HTTP/1.1 200 OK
```

```json
{
  "classification": {
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
  },
  "faq": null
}
```

## 3.7 Réponse réussie — urgence

```http
HTTP/1.1 200 OK
```

```json
{
  "classification": {
    "call_id": "CALL-0002",
    "category": "urgence",
    "confidence": 0.93,
    "is_emergency": true,
    "action": "TRANSFER_IMMEDIATELY",
    "category_scores": null,
    "model_name": "linear_svm",
    "model_version": "1.0.0",
    "processing_time_ms": 82
  },
  "faq": null
}
```

## 3.8 Réponse réussie — demande traitée par la FAQ

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

## 3.9 Demande non comprise

```json
{
  "classification": {
    "call_id": "CALL-0004",
    "category": "inconnue",
    "confidence": 0.42,
    "is_emergency": false,
    "action": "TRANSFER_TO_HUMAN",
    "category_scores": null,
    "model_name": "linear_svm",
    "model_version": "1.0.0",
    "processing_time_ms": 87
  },
  "faq": null
}
```

## 3.10 Erreurs possibles

### Texte vide

```http
HTTP/1.1 422 Unprocessable Entity
```

```json
{
  "error": {
    "code": "EMPTY_TEXT",
    "message": "Le texte de la demande est obligatoire.",
    "details": {
      "field": "text"
    }
  }
}
```

### Modèle indisponible

```http
HTTP/1.1 503 Service Unavailable
```

```json
{
  "error": {
    "code": "CLASSIFIER_UNAVAILABLE",
    "message": "Le service de classification est temporairement indisponible.",
    "details": null
  }
}
```

---

# 4. Rechercher une réponse FAQ

## 4.1 Endpoint

```http
POST /api/v1/faqs/search
```

## 4.2 Objectif

Rechercher une réponse dans les FAQ actives à partir d’une question formulée
par un patient.

Cet endpoint peut être utilisé directement ou appelé en interne après la
classification d’une demande.

## 4.3 Corps de la requête

```json
{
  "question": "Est-ce que le cabinet est ouvert le samedi ?",
  "category": "informations",
  "language": "fr"
}
```

## 4.4 Champs de la requête

| Champ | Type | Obligatoire | Description |
|---|---|---:|---|
| `question` | string | Oui | Question formulée par le patient |
| `category` | string ou null | Non | Catégorie utilisée pour filtrer la FAQ |
| `language` | string | Non | Langue de recherche |

## 4.5 Réponse avec correspondance

```http
HTTP/1.1 200 OK
```

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

## 4.6 Réponse sans correspondance fiable

```http
HTTP/1.1 200 OK
```

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

## 4.7 Erreurs possibles

- question absente ;
- question vide ;
- catégorie invalide ;
- bibliothèque FAQ indisponible ;
- erreur pendant la recherche.

---

# 5. Consulter les FAQ

## 5.1 Endpoint

```http
GET /api/v1/faqs
```

## 5.2 Objectif

Retourner la liste des FAQ disponibles.

L’accès peut être limité aux secrétaires et administrateurs.

## 5.3 Paramètres de requête

| Paramètre | Type | Obligatoire | Description |
|---|---|---:|---|
| `category` | string | Non | Filtrer par catégorie |
| `active` | boolean | Non | Filtrer selon le statut |
| `page` | integer | Non | Numéro de page |
| `page_size` | integer | Non | Nombre de résultats par page |

## 5.4 Exemple de requête

```http
GET /api/v1/faqs?category=informations&active=true&page=1&page_size=20
```

## 5.5 Exemple de réponse

```json
{
  "items": [
    {
      "id": 12,
      "question": "Quels sont les horaires du cabinet ?",
      "answer": "Le cabinet est ouvert du lundi au vendredi de 8h30 à 18h00.",
      "category": "informations",
      "tags": [
        "horaires",
        "ouverture"
      ],
      "active": true,
      "created_at": "2026-07-22T10:00:00Z",
      "updated_at": "2026-07-22T10:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```

---

# 6. Consulter une FAQ

## 6.1 Endpoint

```http
GET /api/v1/faqs/{faq_id}
```

## 6.2 Objectif

Retourner une FAQ à partir de son identifiant.

## 6.3 Réponse réussie

```json
{
  "id": 12,
  "question": "Quels sont les horaires du cabinet ?",
  "answer": "Le cabinet est ouvert du lundi au vendredi de 8h30 à 18h00.",
  "category": "informations",
  "tags": [
    "horaires",
    "ouverture"
  ],
  "active": true,
  "created_at": "2026-07-22T10:00:00Z",
  "updated_at": "2026-07-22T10:00:00Z"
}
```

## 6.4 FAQ inexistante

```http
HTTP/1.1 404 Not Found
```

```json
{
  "error": {
    "code": "FAQ_NOT_FOUND",
    "message": "La FAQ demandée n’existe pas.",
    "details": {
      "faq_id": 12
    }
  }
}
```

---

# 7. Ajouter une FAQ

## 7.1 Endpoint

```http
POST /api/v1/faqs
```

## 7.2 Objectif

Permettre à un utilisateur autorisé d’ajouter une FAQ.

## 7.3 Rôle requis

```text
Administrateur
```

Le rôle exact sera contrôlé par le Module 1.

## 7.4 Corps de la requête

```json
{
  "question": "Quels moyens de paiement acceptez-vous ?",
  "answer": "Le cabinet accepte les paiements par carte bancaire, chèque et espèces.",
  "category": "informations",
  "tags": [
    "paiement",
    "carte bancaire",
    "chèque",
    "espèces"
  ],
  "active": true
}
```

## 7.5 Réponse réussie

```http
HTTP/1.1 201 Created
```

```json
{
  "id": 15,
  "question": "Quels moyens de paiement acceptez-vous ?",
  "answer": "Le cabinet accepte les paiements par carte bancaire, chèque et espèces.",
  "category": "informations",
  "tags": [
    "paiement",
    "carte bancaire",
    "chèque",
    "espèces"
  ],
  "active": true,
  "created_at": "2026-07-22T15:00:00Z",
  "updated_at": "2026-07-22T15:00:00Z"
}
```

## 7.6 Erreurs possibles

- question vide ;
- réponse vide ;
- catégorie invalide ;
- FAQ déjà existante ;
- utilisateur non autorisé.

---

# 8. Modifier une FAQ

## 8.1 Endpoint

```http
PUT /api/v1/faqs/{faq_id}
```

## 8.2 Objectif

Modifier complètement une FAQ existante.

## 8.3 Corps de la requête

```json
{
  "question": "Quels sont les horaires du cabinet ?",
  "answer": "Le cabinet est ouvert du lundi au vendredi de 8h00 à 18h00.",
  "category": "informations",
  "tags": [
    "horaires",
    "ouverture"
  ],
  "active": true
}
```

## 8.4 Réponse réussie

```http
HTTP/1.1 200 OK
```

```json
{
  "id": 12,
  "question": "Quels sont les horaires du cabinet ?",
  "answer": "Le cabinet est ouvert du lundi au vendredi de 8h00 à 18h00.",
  "category": "informations",
  "tags": [
    "horaires",
    "ouverture"
  ],
  "active": true,
  "created_at": "2026-07-22T10:00:00Z",
  "updated_at": "2026-07-22T16:00:00Z"
}
```

---

# 9. Modifier partiellement une FAQ

## 9.1 Endpoint

```http
PATCH /api/v1/faqs/{faq_id}
```

## 9.2 Objectif

Modifier un ou plusieurs champs sans remplacer toute la FAQ.

## 9.3 Exemple

```json
{
  "answer": "Le cabinet est ouvert du lundi au vendredi de 8h00 à 18h00."
}
```

---

# 10. Désactiver une FAQ

## 10.1 Endpoint recommandé

```http
PATCH /api/v1/faqs/{faq_id}/status
```

## 10.2 Objectif

Activer ou désactiver une FAQ sans la supprimer définitivement.

## 10.3 Corps de la requête

```json
{
  "active": false
}
```

## 10.4 Réponse réussie

```json
{
  "id": 12,
  "active": false,
  "message": "La FAQ a été désactivée."
}
```

La désactivation logique est privilégiée pour conserver l’historique.

---

# 11. Vérifier l’état du service

## 11.1 Endpoint

```http
GET /api/v1/health
```

## 11.2 Objectif

Vérifier que l’API est disponible.

## 11.3 Exemple de réponse

```json
{
  "status": "healthy",
  "module": "qualification-and-faq",
  "version": "0.1.0"
}
```

Une version plus complète pourra également vérifier :

- la disponibilité du modèle ;
- la connexion à la base ;
- la disponibilité du service FAQ.

---

# 12. Format commun des erreurs

Toutes les erreurs doivent respecter la structure suivante :

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Description compréhensible de l’erreur.",
    "details": {}
  }
}
```

## Exemples de codes

| Code | Signification |
|---|---|
| `EMPTY_TEXT` | Texte absent ou vide |
| `INVALID_CATEGORY` | Catégorie non reconnue |
| `FAQ_NOT_FOUND` | FAQ inexistante |
| `FAQ_ALREADY_EXISTS` | FAQ déjà existante |
| `ACCESS_DENIED` | Utilisateur non autorisé |
| `CLASSIFIER_UNAVAILABLE` | Modèle indisponible |
| `FAQ_SERVICE_UNAVAILABLE` | Service FAQ indisponible |
| `INTERNAL_ERROR` | Erreur interne |

---

# 13. Résumé des endpoints

| Méthode | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/calls/classify` | Classifier une demande |
| `POST` | `/api/v1/faqs/search` | Rechercher une réponse FAQ |
| `GET` | `/api/v1/faqs` | Lister les FAQ |
| `GET` | `/api/v1/faqs/{faq_id}` | Consulter une FAQ |
| `POST` | `/api/v1/faqs` | Ajouter une FAQ |
| `PUT` | `/api/v1/faqs/{faq_id}` | Remplacer une FAQ |
| `PATCH` | `/api/v1/faqs/{faq_id}` | Modifier partiellement une FAQ |
| `PATCH` | `/api/v1/faqs/{faq_id}/status` | Activer ou désactiver une FAQ |
| `GET` | `/api/v1/health` | Vérifier l’état de l’API |

---

# 14. Points d’intégration

## 14.1 Module 3 vers Module 4

Le Module 3 envoie :

- l’identifiant de l’appel ;
- le texte issu de la transcription ;
- la langue ;
- le contexte disponible.

Le Module 4 retourne :

- la catégorie ;
- le score de confiance ;
- l’indication d’urgence ;
- l’action à exécuter ;
- la réponse FAQ éventuelle.

## 14.2 Module 4 vers Module 1

Le Module 4 peut utiliser le Module 1 pour :

- vérifier l’authentification ;
- vérifier les rôles et permissions ;
- accéder à la base centrale ;
- enregistrer l’historique ;
- récupérer les paramètres partagés.

## 14.3 Module 4 vers Module 3

Pour une urgence, le Module 4 retourne :

```json
{
  "action": "TRANSFER_IMMEDIATELY"
}
```

Le Module 3 reste responsable de l’exécution technique du transfert.

---

# 15. Points à valider

Les éléments suivants doivent encore être confirmés :

- les noms définitifs des endpoints ;
- le préfixe exact de version ;
- le mécanisme d’authentification ;
- le format exact transmis par le Module 3 ;
- les rôles autorisés à modifier la FAQ ;
- le stockage de l’historique ;
- la présence de `patient_id` ;
- les codes d’erreur partagés entre les modules ;
- la méthode utilisée pour désactiver une FAQ ;
- la différence entre recherche FAQ interne et endpoint public ;
- la politique de pagination ;
- la politique de versionnement de l’API.