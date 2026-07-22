# Medical Secretary AI – Module 4

## Description

Ce projet est réalisé dans le cadre d’un Projet de Fin d’Année (PFA) à l’École Nationale de l’Intelligence Artificielle et du Digital (ENIAD).

Il consiste à concevoir et développer le **Module 4** d’une secrétaire médicale intelligente, dédié à la **qualification automatique des appels** et à la **gestion des questions fréquentes (FAQ)**.

Le module reçoit une demande patient sous forme de texte, généralement issue de la transcription d’un appel par le Module 3. Il doit ensuite :

- identifier la catégorie de la demande ;
- calculer un score de confiance ;
- détecter en priorité les situations potentiellement urgentes ;
- orienter la demande vers le service approprié ;
- rechercher une réponse dans une bibliothèque FAQ lorsque cela est pertinent ;
- transférer la demande vers un interlocuteur humain en cas d’incertitude.

Le système ne réalise aucun diagnostic médical. Il détecte uniquement les situations nécessitant une prise en charge prioritaire et déclenche l’action prévue.

---

## Catégories de classification

Le classificateur doit reconnaître les catégories suivantes :

- urgence ;
- rendez-vous ;
- devis ;
- informations ;
- administratif ;
- laboratoire ;
- pharmacie.

Une catégorie supplémentaire `inconnue` est prévue lorsque la demande ne peut pas être classifiée avec un niveau de confiance suffisant.

---

## Fonctionnalités prévues

- Classification automatique des demandes des patients.
- Calcul d’un score de confiance.
- Détection prioritaire des urgences.
- Routage selon la catégorie détectée.
- Transfert vers un humain en cas d’incertitude.
- Recherche de réponses dans une FAQ configurable.
- Gestion des FAQ actives et inactives.
- Historisation des classifications et des actions exécutées.
- Correction humaine des classifications.
- Exposition des fonctionnalités via une API REST.
- Comparaison entre une approche Machine Learning classique et une approche basée sur un LLM.
- Tests unitaires, fonctionnels et d’intégration.
- Simulation des autres modules à l’aide de mocks.

---

## Architecture générale

Le Module 4 s’intègre dans une architecture plus large composée notamment :

- du **Module 3**, responsable de la gestion des appels et de la transcription audio en texte ;
- du **Module 1**, responsable des comptes utilisateurs, des rôles, des permissions et de la base centrale ;
- des services cibles, comme le service de rendez-vous, le laboratoire, la pharmacie ou le service administratif.

Les principaux composants internes prévus sont :

- API REST ;
- service de validation ;
- service de prétraitement ;
- moteur de classification ;
- gestionnaire des urgences ;
- service de routage ;
- gestionnaire FAQ ;
- service d’historisation.

La classification et la recherche FAQ sont séparées afin de pouvoir modifier ou remplacer l’une sans affecter directement l’autre.

---

## Flux principal

```text
Appel du patient
        ↓
Transcription par le Module 3
        ↓
Réception du texte par le Module 4
        ↓
Validation et prétraitement
        ↓
Classification
        ↓
Urgence détectée ?
├── Oui → transfert immédiat
└── Non → vérification du score de confiance
              ↓
       Score suffisant ?
       ├── Non → transfert vers un humain
       └── Oui → routage selon la catégorie
                         ↓
          FAQ, rendez-vous ou autre service
```

---

## Structure du projet

```text
medical-secretary-ai/
│
├── docs/
│   ├── analyse_besoin.md
│   ├── cas_utilisation.md
│   ├── flux_fonctionnel.md
│   ├── regles_metier.md
│   │
│   └── architecture/
│       ├── README.md
│       ├── architecture_module.md
│       ├── flux_appels.md
│       ├── modeles_donnees.md
│       ├── api_rest.md
│       │
│       └── diagrams/
│           ├── architecture_module.drawio
│           ├── flux_qualification.drawio
│           ├── sequence_classification.drawio
│           │
│           └── exports/
│               ├── architecture_module.png
│               ├── flux_qualification.png
│               └── sequence_classification.png
│
├── src/
│   ├── __init__.py
│   └── schemas/
│       ├── __init__.py
│       └── qualification.py
│
├── data/
│
├── tests/
│   └── test_schemas.py
│
├── report/
│
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Documentation disponible

### Analyse fonctionnelle

- `docs/analyse_besoin.md` : contexte, problématique, objectifs et périmètre.
- `docs/cas_utilisation.md` : cas d’utilisation du Module 4.
- `docs/regles_metier.md` : règles de classification, urgences, FAQ, routage et traçabilité.
- `docs/flux_fonctionnel.md` : description générale des flux métier.

### Architecture technique

- `docs/architecture/architecture_module.md` : architecture générale et responsabilités des composants.
- `docs/architecture/flux_appels.md` : flux technique d’une demande.
- `docs/architecture/modeles_donnees.md` : schémas `CallEntry`, `ClassificationResult` et `FAQResponse`.
- `docs/architecture/api_rest.md` : contrats des interfaces REST.
- `docs/architecture/diagrams/` : sources Draw.io et exports des diagrammes.

---

## Modèles de données

Les premiers schémas ont été définis avec Pydantic.

### `CallEntry`

Représente une demande transmise par le Module 3.

Principaux champs :

- `call_id`
- `text`
- `language`
- `patient_id`
- `context`
- `created_at`

### `ClassificationResult`

Représente le résultat du classificateur.

Principaux champs :

- `category`
- `confidence`
- `is_emergency`
- `action`
- `category_scores`
- `model_name`
- `model_version`
- `processing_time_ms`

### `FAQResponse`

Représente le résultat d’une recherche dans la FAQ.

Principaux champs :

- `matched`
- `matched_faq_id`
- `question`
- `answer`
- `confidence`
- `action`

---

## Interfaces API prévues

Les contrats REST sont définis dans :

```text
docs/architecture/api_rest.md
```

Principaux endpoints prévus :

| Méthode | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/calls/classify` | Classifier une demande |
| `POST` | `/api/v1/faqs/search` | Rechercher une réponse FAQ |
| `GET` | `/api/v1/faqs` | Lister les FAQ |
| `GET` | `/api/v1/faqs/{faq_id}` | Consulter une FAQ |
| `POST` | `/api/v1/faqs` | Ajouter une FAQ |
| `PUT` | `/api/v1/faqs/{faq_id}` | Modifier une FAQ |
| `PATCH` | `/api/v1/faqs/{faq_id}` | Modifier partiellement une FAQ |
| `PATCH` | `/api/v1/faqs/{faq_id}/status` | Activer ou désactiver une FAQ |
| `GET` | `/api/v1/health` | Vérifier l’état du service |

Ces contrats restent provisoires jusqu’à validation avec les autres modules.

---

## Installation

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd medical-secretary-ai
```

### 2. Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Sous Linux ou macOS :

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Tests

Les premiers tests concernent les schémas Pydantic.

Pour exécuter les tests :

```bash
python -m pytest
```

Ou :

```bash
pytest
```

Le fichier `pytest.ini` configure le chemin Python du projet.

---

## Technologies envisagées

- Python
- FastAPI
- Pydantic
- scikit-learn
- pandas
- PostgreSQL
- SQLAlchemy
- Alembic
- LLM avec function calling
- pytest
- Docker
- Draw.io

Les choix définitifs seront validés au fur et à mesure de l’avancement du projet.

---

## État d’avancement

### Phase 1 — Analyse du besoin

- [x] Analyse du cahier des charges.
- [x] Définition du contexte et de la problématique.
- [x] Définition des objectifs.
- [x] Délimitation du périmètre.
- [x] Identification des entrées et sorties.
- [x] Rédaction de l’analyse du besoin.

### Phase 2 — Analyse fonctionnelle

- [x] Définition des acteurs.
- [x] Rédaction des cas d’utilisation.
- [x] Définition des règles métier.
- [x] Conception des flux fonctionnels.
- [x] Définition du routage par catégorie.

### Phase 3 — Conception de l’architecture

- [x] Diagramme d’architecture générale.
- [x] Diagramme de flux de qualification.
- [x] Diagramme de séquence.
- [x] Définition des composants internes.
- [x] Séparation entre classification et FAQ.
- [x] Définition des schémas de données.
- [x] Implémentation des schémas Pydantic.
- [x] Documentation des contrats API REST.
- [x] Ajout des tests initiaux des schémas.

---

## Roadmap

- [x] Analyse du besoin
- [x] Analyse fonctionnelle
- [x] Conception de l’architecture
- [ ] Construction du jeu de données
- [ ] Développement du classificateur scikit-learn
- [ ] Développement du classificateur LLM
- [ ] Évaluation et comparaison des modèles
- [ ] Création de la base de données FAQ
- [ ] Développement du gestionnaire FAQ
- [ ] Implémentation de l’API REST
- [ ] Développement des mocks
- [ ] Tests unitaires et fonctionnels
- [ ] Tests d’intégration
- [ ] Intégration avec les Modules 1 et 3
- [ ] Documentation finale
- [ ] Finalisation du rapport

---

## Limites actuelles

À ce stade :

- les endpoints sont documentés mais pas encore implémentés ;
- le classificateur n’est pas encore entraîné ;
- le dataset n’est pas encore construit ;
- la base FAQ n’est pas encore créée ;
- les seuils de confiance restent provisoires ;
- les échanges exacts avec les Modules 1 et 3 restent à valider ;
- les règles de détection médicale doivent être validées par une personne compétente.

---

## Auteur

**Siham Daba**  
Étudiante en Intelligence Artificielle  
École Nationale de l’Intelligence Artificielle et du Digital — ENIAD  
Projet de Fin d’Année — 2025–2026
