# Analyse du besoin

## 1. Identification du projet

| Élément | Description |
|---|---|
| Nom du projet | Secrétaire Médicale IA |
| Module concerné | Module 4 — Qualification des appels et FAQ |
| Domaine | Intelligence artificielle, NLP, santé |
| Utilisateurs principaux | Patients, secrétaires, médecins, administrateurs |
| Entrée principale | Texte représentant la demande d’un patient |
| Sortie principale | Catégorie, niveau de confiance et action à exécuter |
| Technologie principale | Python |
| Intégration | API REST et base de données centrale |

## 2. Besoin principal

Le système doit analyser automatiquement une demande formulée par un patient,
identifier sa nature et déterminer l’action adaptée.

Il doit notamment être capable de :

- détecter une situation urgente ;
- reconnaître une demande liée à un rendez-vous ;
- reconnaître une demande de devis ;
- reconnaître une demande d’information ;
- reconnaître une demande administrative ;
- reconnaître une demande liée à un laboratoire ;
- reconnaître une demande liée à une pharmacie ;
- fournir une réponse à partir d’une bibliothèque de FAQ ;
- transférer la demande lorsqu’une réponse fiable ne peut pas être fournie.


## 3. Contexte

Les cabinets médicaux, cliniques et centres de santé reçoivent quotidiennement
un nombre important d’appels provenant des patients.

Ces appels peuvent concerner la prise, la modification ou l’annulation d’un
rendez-vous, une demande d’information, une question administrative, une
demande de devis, un résultat de laboratoire, une question liée à une pharmacie
ou une situation potentiellement urgente.

La gestion manuelle de ces demandes peut représenter une charge importante
pour les secrétaires médicales. Elle peut également entraîner des temps
d’attente, des appels manqués et une disponibilité limitée en dehors des
horaires d’ouverture.

Le projet de Secrétaire Médicale IA vise à automatiser une partie de cette
gestion. Le Module 4 est chargé d’analyser la demande du patient, de la
classifier et de fournir une réponse à partir d’une bibliothèque de questions
fréquentes lorsque cela est possible.

Le système doit également reconnaître les situations urgentes afin de les
transférer immédiatement vers un interlocuteur humain ou vers le service prévu.

## 4. Problématique

Comment concevoir un système intelligent capable de qualifier automatiquement
les demandes téléphoniques des patients, de détecter les situations urgentes
et de fournir des réponses fiables aux questions fréquentes, tout en limitant
les erreurs de classification, les coûts d’utilisation et les risques liés aux
demandes médicales sensibles ?

### Sous-problèmes

- Comment différencier des demandes parfois très proches ?
- Comment limiter le risque de ne pas reconnaître une urgence ?
- Comment mesurer objectivement la qualité du classificateur ?
- Comment garantir que les réponses FAQ restent fiables et paramétrables ?
- Comment traiter les demandes inconnues ou ambiguës ?
- Comment développer le module avant que les autres modules soient disponibles ?
- Comment comparer une solution Machine Learning classique à une solution LLM ?

## 5. Objectif général

Développer un module intelligent de traitement du langage capable d’analyser
une demande formulée par un patient, de l’associer à une catégorie fonctionnelle,
de détecter les demandes urgentes et de répondre automatiquement aux questions
fréquentes à partir d’une bibliothèque paramétrable.

## 6. Objectifs spécifiques

- Étudier et formaliser les besoins fonctionnels du Module 4.
- Définir précisément les catégories de demandes.
- Construire un jeu de données représentatif des demandes des patients.
- Prétraiter et analyser les textes collectés.
- Développer plusieurs modèles de classification.
- Comparer une approche Machine Learning classique à une approche utilisant un LLM.
- Mesurer les performances à l’aide de métriques adaptées.
- Accorder une attention particulière au rappel de la classe urgence.
- Développer une logique de gestion prioritaire des urgences.
- Mettre en place une bibliothèque FAQ paramétrable.
- Développer une API REST pour exposer les services du module.
- Tester le module avec des mocks.
- Préparer l’intégration avec le backend central et le module téléphonique.
- Documenter le développement, les résultats et les limites de la solution.

## 7. Périmètre du projet

### Fonctionnalités incluses

Le travail couvre :

- la réception d’une demande sous forme de texte ;
- le nettoyage et le prétraitement de la demande ;
- la classification de la demande ;
- le calcul d’un score de confiance ;
- la détection des demandes urgentes ;
- la détermination de l’action à exécuter ;
- la recherche d’une réponse dans la FAQ ;
- la gestion des questions et réponses de la FAQ ;
- l’historisation éventuelle des classifications ;
- les tests unitaires et les tests avec mocks ;
- l’exposition des fonctions avec une API REST.


### Fonctionnalités non incluses dans la première version

La première version ne couvre pas directement :

- la gestion complète des comptes utilisateurs ;
- la gestion complète des rendez-vous ;
- le développement du système téléphonique ;
- la transcription réelle des appels ;
- la synthèse vocale ;
- la gestion des paiements ;
- l’interprétation médicale des résultats ;
- le diagnostic médical ;
- la prescription d’un traitement ;
- le remplacement d’un professionnel de santé.

Ces fonctions appartiennent à d’autres modules ou à une phase d’intégration
ultérieure.

## 8. Entrées du module

Le module peut recevoir :

- le texte de la demande du patient ;
- l’identifiant de l’appel ;
- l’identifiant du patient, lorsqu’il est disponible ;
- la langue de la demande ;
- le contexte transmis par un autre module ;
- les données de la bibliothèque FAQ.

## 9. Sorties du module

Le module peut retourner :

- la catégorie prédite ;
- le score de confiance ;
- l’action à réaliser ;
- l’identifiant de la FAQ sélectionnée ;
- la réponse associée ;
- une indication de transfert vers un humain ;
- une indication de transfert immédiat pour une urgence ;
- le temps de traitement ;
- le nom et la version du modèle utilisé.

Exemple :

{
  "category": "rendez-vous",
  "confidence": 0.94,
  "action": "ROUTE_TO_APPOINTMENT_SERVICE",
  "faq_answer": null
}

## 10. Hypothèses initiales

- La demande est reçue sous forme de texte.
- La transcription vocale est fournie par un autre module.
- Une demande possède une catégorie principale.
- Le système ne fournit pas de diagnostic médical.
- Les urgences sont traitées avant toute recherche dans la FAQ.
- Une demande avec une confiance insuffisante est transmise à un humain.
- Les réponses FAQ sont validées par un responsable autorisé.
- La FAQ est modifiable sans réentraîner le modèle de classification.
- Le module peut être développé avec des mocks avant l’intégration réelle.

