# Flux fonctionnel — Module 4

## 1. Objectif

Ce document décrit le fonctionnement général du Module 4 depuis la réception de la demande jusqu’à l’exécution de l’action appropriée.

---

## 2. Source de la demande

Dans le système final, la demande suivra le flux suivant :

```text
Appel du patient
        ↓
Module 3 — Système téléphonique
        ↓
Transcription de la parole en texte
        ↓
Module 4 — Qualification des appels et FAQ
```

Dans le premier prototype, la partie téléphonique et la transcription seront simulées.

La demande sera saisie directement sous forme de texte.

---

## 3. Flux principal

```text
Réception du texte
        ↓
Validation du texte
        ↓
Nettoyage et normalisation
        ↓
Classification de la demande
        ↓
Calcul des scores
        ↓
┌─────────────────────────────┐
│ Risque d’urgence détecté ?  │
└─────────────────────────────┘
       │ Oui                         │ Non
       ↓                             ↓
Enregistrer l’urgence        Score général suffisant ?
       ↓                       │ Oui          │ Non
Transfert immédiat            ↓              ↓
       ↓                 Identifier      Catégorie inconnue
Réponse de transfert       la catégorie        ↓
                             ↓          Transfert vers humain
                       Déterminer l’action
                             ↓
           ┌─────────────────┼───────────────────┐
           ↓                 ↓                   ↓
       Rendez-vous      Question FAQ      Autre service
           ↓                 ↓                   ↓
   Service rendez-vous  Recherche FAQ      Routage adapté
                             ↓
                    Réponse fiable ?
                       │ Oui      │ Non
                       ↓          ↓
                 Réponse FAQ   Transfert humain
```

---

## 4. Description détaillée

### Étape 1 — Réception

Le module reçoit une requête contenant au minimum :

```json
{
  "text": "Je voudrais connaître les horaires du cabinet."
}
```

---

### Étape 2 — Validation

Le système vérifie :

- que le champ `text` existe ;
- que sa valeur n’est pas vide ;
- que son type est valide ;
- que sa longueur respecte les limites définies.

En cas d’erreur :

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Le texte de la demande est obligatoire."
  }
}
```

---

### Étape 3 — Prétraitement

Le système prépare le texte pour la classification.

Exemples d’opérations :

- suppression des espaces inutiles ;
- normalisation de la casse ;
- traitement de certains caractères ;
- préparation selon le modèle utilisé.

Le texte original doit être conservé.

---

### Étape 4 — Classification

Le classificateur retourne :

- la catégorie la plus probable ;
- le score de cette catégorie ;
- éventuellement les scores des autres catégories ;
- le nom du modèle utilisé ;
- le temps de traitement.

Exemple :

```json
{
  "predicted_category": "informations",
  "confidence": 0.89,
  "model_name": "linear_svm",
  "model_version": "1.0.0",
  "processing_time_ms": 95
}
```

---

### Étape 5 — Vérification de l’urgence

Le système vérifie en priorité le score associé à la classe `urgence`.

Si le seuil est dépassé :

```json
{
  "category": "urgence",
  "action": "TRANSFER_IMMEDIATELY"
}
```

Aucune recherche FAQ ne doit être réalisée avant le traitement de l’urgence.

---

### Étape 6 — Vérification du seuil général

Si la demande n’est pas urgente, le système vérifie le score général.

```text
Score suffisant
→ accepter la catégorie

Score insuffisant
→ catégorie inconnue
→ transfert vers un humain
```

---

### Étape 7 — Détermination de l’action

Le système associe la catégorie à une action.

| Catégorie | Traitement |
|---|---|
| urgence | Transfert immédiat |
| rendez-vous | Routage vers le service de rendez-vous |
| devis | Routage vers le service de devis |
| informations | Recherche éventuelle dans la FAQ |
| administratif | Routage vers le service administratif |
| laboratoire | Routage vers le service laboratoire |
| pharmacie | Routage vers le service pharmacie |
| inconnue | Transfert vers un humain |

Cette correspondance est provisoire.

---

### Étape 8 — Recherche FAQ

La recherche dans la FAQ est exécutée uniquement lorsqu’elle est adaptée à la demande.

Exemples de sujets FAQ :

- horaires ;
- adresse ;
- parking ;
- spécialités ;
- préparation avant consultation ;
- tarifs ;
- moyens de paiement ;
- résultats d’examens ;
- téléconsultation.

Le système recherche uniquement dans les FAQ actives.

---

### Étape 9 — Vérification de la réponse FAQ

Si la similarité dépasse le seuil :

```json
{
  "category": "informations",
  "answer": "Le cabinet est ouvert du lundi au vendredi de 8h30 à 18h00.",
  "matched_faq_id": 12,
  "faq_confidence": 0.91,
  "action": "ANSWER_WITH_FAQ"
}
```

Si la similarité est insuffisante :

```json
{
  "category": "informations",
  "answer": null,
  "matched_faq_id": null,
  "faq_confidence": 0.42,
  "action": "TRANSFER_TO_HUMAN"
}
```

---

### Étape 10 — Historisation

Le système enregistre le traitement :

```json
{
  "request_id": "REQ-0001",
  "original_text": "Je voudrais connaître les horaires.",
  "predicted_category": "informations",
  "classification_confidence": 0.89,
  "action": "ANSWER_WITH_FAQ",
  "matched_faq_id": 12,
  "model_name": "linear_svm",
  "model_version": "1.0.0",
  "processing_time_ms": 120,
  "created_at": "YYYY-MM-DDTHH:MM:SS"
}
```

---

# 5. Flux d’une urgence

```text
Demande du patient
        ↓
Classification
        ↓
Score urgence supérieur au seuil
        ↓
Arrêt du traitement normal
        ↓
Création d’un événement d’urgence
        ↓
Transfert immédiat
        ↓
Journalisation
```

Exemple :

```json
{
  "category": "urgence",
  "confidence": 0.93,
  "action": "TRANSFER_IMMEDIATELY",
  "message": "Votre demande nécessite une prise en charge prioritaire."
}
```

---

# 6. Flux d’une question FAQ

```text
Question du patient
        ↓
Classification
        ↓
Catégorie compatible avec la FAQ
        ↓
Recherche dans les FAQ actives
        ↓
Calcul de similarité
        ↓
┌─────────────────────────┐
│ Score suffisant ?       │
└─────────────────────────┘
     │ Oui          │ Non
     ↓              ↓
Réponse FAQ     Transfert humain
```

---

# 7. Flux d’une demande inconnue

```text
Demande reçue
      ↓
Classification
      ↓
Score inférieur au seuil
      ↓
Catégorie inconnue
      ↓
Aucune réponse automatique
      ↓
Transfert vers une secrétaire
      ↓
Correction humaine éventuelle
```

---

# 8. Flux de correction

```text
Classification enregistrée
        ↓
Consultation par la secrétaire
        ↓
Prédiction incorrecte ?
     │ Oui          │ Non
     ↓              ↓
Correction       Aucune action
     ↓
Enregistrement de la catégorie réelle
     ↓
Validation de la donnée
     ↓
Ajout futur au dataset
```

---

# 9. Flux avec les mocks

Pendant la phase de développement, les autres modules seront simulés.

```text
Mock du Module 3
        ↓
Envoi d’un texte de test
        ↓
Module 4
        ↓
Classification et routage
        ↓
Mock du service cible
        ↓
Confirmation de l’action
```

Exemples de mocks :

- `MockCallService` pour simuler la transcription ;
- `MockTransferService` pour simuler un transfert ;
- `MockAppointmentService` pour simuler le service de rendez-vous ;
- `MockUserService` pour simuler les utilisateurs ;
- `MockFAQRepository` pour simuler la base FAQ.

---

# 10. Hypothèses actuelles

- Le Module 4 reçoit principalement du texte.
- La transcription audio est gérée par le Module 3.
- Une demande possède une catégorie principale.
- Les urgences sont traitées en priorité.
- Les demandes peu fiables sont transférées à un humain.
- Les FAQ sont administrables.
- Les réponses FAQ proviennent de contenus validés.
- Les services externes peuvent être simulés avec des mocks.
- Le système ne réalise aucun diagnostic médical.

---

# 11. Points à valider

- Le format exact transmis par le Module 3.
- Les actions disponibles pour chaque catégorie.
- La définition technique du transfert immédiat.
- Les seuils de classification.
- Les catégories compatibles avec la FAQ.
- Le comportement en cas de service indisponible.
- Le format de l’historique.
- La gestion des demandes contenant plusieurs intentions.