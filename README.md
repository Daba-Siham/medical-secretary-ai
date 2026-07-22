# Medical Secretary AI – Module 4

## Description

Ce projet est réalisé dans le cadre d'un Projet de Fin d'Année (PFA) à l'École Nationale de l'Intelligence Artificielle et du Digital (ENIAD).

Il consiste à développer le **Module 4** d'une secrétaire médicale intelligente, dédié à la **qualification automatique des appels** et à la **gestion des questions fréquentes (FAQ)**.

Le module est capable de :
- classifier automatiquement les demandes des patients ;
- détecter les situations potentiellement urgentes ;
- répondre aux questions fréquentes à partir d'une FAQ configurable ;
- orienter les demandes vers le service approprié.

---

## Fonctionnalités prévues

- Classification automatique des demandes.
- Détection des urgences.
- Réponse automatique via une FAQ.
- API REST pour les services du module.
- Comparaison entre une approche Machine Learning et une approche basée sur un LLM.
- Tests unitaires et d'intégration.

---

## Structure du projet

```text
medical-secretary-ai/
│
├── docs/          # Documentation du projet
├── src/           # Code source
├── data/          # Jeux de données
├── tests/         # Tests
├── report/        # Rapport de stage (LaTeX)
├── README.md
└── .gitignore
```

---

## Technologies envisagées

- Python
- FastAPI
- scikit-learn
- pandas
- PostgreSQL
- LLM
- pytest
- Docker

---

## État d'avancement

### ✅ Jour 1 – Analyse du besoin

Les travaux réalisés :

- Analyse du cahier des charges.
- Définition du contexte et de la problématique.
- Définition des objectifs du projet.
- Délimitation du périmètre du Module 4.
- Rédaction du document d'analyse du besoin.

Le document est disponible dans :

```text
docs/analyse_besoin.md
```

---

## Roadmap

- [x] Analyse du besoin
- [ ] Analyse fonctionnelle
- [ ] Conception de l'architecture
- [ ] Construction du jeu de données
- [ ] Développement des modèles de classification
- [ ] Développement du module FAQ
- [ ] Développement de l'API REST
- [ ] Tests et évaluation
- [ ] Intégration
- [ ] Documentation finale

---

## Auteur

**Siham Daba**  
Étudiante en Intelligence Artificielle – ENIAD