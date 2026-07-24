# Base de données FAQ

## 1. Objectif

La table `faqs` stocke les questions et réponses validées utilisées par
le Module 4.

La FAQ est paramétrable et peut être modifiée sans réentraîner le modèle
de classification.

## 2. Structure de la table

| Champ | Type | Description |
|---|---|---|
| `id` | integer | Identifiant unique |
| `question` | varchar(500) | Question fréquente |
| `answer` | text | Réponse validée |
| `category` | varchar(100) | Catégorie principale |
| `tags` | JSON | Liste des mots-clés |
| `active` | boolean | Statut actif ou inactif |
| `created_at` | datetime | Date de création |
| `updated_at` | datetime | Date de modification |

## 3. Règles principales

- Une question et une réponse sont obligatoires.
- Une question doit être unique.
- Une FAQ inactive ne doit pas être utilisée.
- Les urgences ne doivent pas être traitées par la FAQ.
- Les réponses médicales doivent être validées.
- Une FAQ est désactivée plutôt que supprimée définitivement.
- Les contenus initiaux doivent être validés par l’établissement.

## 4. Migration

La table est créée avec Alembic.

```bash
alembic upgrade head
```
## 5. Initialisation

Les FAQ initiales sont ajoutées avec :

python -m scripts.seed_faq