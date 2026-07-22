# Cas d’utilisation — Module 4

## 1. Présentation

Ce document décrit les principaux cas d’utilisation du Module 4 — Qualification des appels et FAQ.

Le module reçoit une demande formulée par un patient sous forme de texte. Il doit :

- identifier la catégorie de la demande ;
- calculer un niveau de confiance ;
- détecter les situations urgentes ;
- déterminer l’action à exécuter ;
- rechercher une réponse dans la FAQ lorsque cela est pertinent ;
- transférer la demande à un humain lorsque le système n’est pas suffisamment fiable.

---

## 2. Acteurs concernés

### 2.1 Patient

Le patient formule une demande concernant :

- une urgence ;
- un rendez-vous ;
- un devis ;
- une information générale ;
- une démarche administrative ;
- un laboratoire ;
- une pharmacie.

### 2.2 Secrétaire médicale

La secrétaire médicale peut :

- consulter les demandes reçues ;
- reprendre une demande transférée ;
- consulter la catégorie prédite ;
- corriger une mauvaise classification ;
- superviser les demandes urgentes.

### 2.3 Administrateur

L’administrateur peut :

- ajouter une question fréquente ;
- modifier une question fréquente ;
- désactiver une question fréquente ;
- consulter l’historique des traitements ;
- gérer les paramètres du module.

### 2.4 Module 3 — Système téléphonique

Le Module 3 transmet au Module 4 le texte issu de la transcription d’un appel.

Dans la première version, ce module sera simulé à l’aide d’un mock.

### 2.5 Module 1 — Backend central

Le Module 1 fournit les services centraux, notamment :

- les comptes utilisateurs ;
- les rôles et permissions ;
- la base de données centrale ;
- les fonctions partagées entre les différents modules.

---

# 3. UC01 — Classifier une demande

## Objectif

Identifier automatiquement la catégorie d’une demande formulée par un patient.

## Acteur principal

Patient ou Module 3.

## Préconditions

- Le service de classification est disponible.
- Le texte reçu n’est pas vide.
- Le modèle de classification est chargé.

## Entrée

```json
{
  "text": "Je souhaite annuler mon rendez-vous de demain"
}
```

## Scénario nominal

1. Le système reçoit le texte.
2. Le système vérifie que le texte est valide.
3. Le système nettoie et prépare le texte.
4. Le modèle analyse la demande.
5. Le système détermine la catégorie la plus probable.
6. Le système calcule un score de confiance.
7. Le système détermine l’action à réaliser.
8. Le résultat est enregistré dans l’historique.
9. Le système retourne la réponse.

## Sortie

```json
{
  "category": "rendez-vous",
  "confidence": 0.96,
  "action": "ROUTE_TO_APPOINTMENT_SERVICE"
}
```

## Postconditions

- La demande est classifiée.
- La prédiction est enregistrée.
- La demande peut être transmise au service correspondant.

## Cas d’erreur

- Texte vide.
- Modèle indisponible.
- Erreur pendant le prétraitement.
- Score de confiance insuffisant.
- Catégorie non reconnue.

---

# 4. UC02 — Détecter une urgence

## Objectif

Identifier une demande potentiellement urgente et déclencher immédiatement la procédure prévue.

## Acteur principal

Patient ou Module 3.

## Préconditions

- Le texte de la demande est disponible.
- Le service de classification fonctionne.
- Le mécanisme de transfert est disponible ou simulé.

## Entrée

```json
{
  "text": "J’ai une douleur très forte à la poitrine et je respire mal"
}
```

## Scénario nominal

1. Le système reçoit la demande.
2. Le système analyse le texte.
3. Le système calcule la probabilité associée à la classe `urgence`.
4. La probabilité dépasse le seuil défini pour les urgences.
5. Le système interrompt le traitement normal.
6. Le système déclenche immédiatement l’action de transfert.
7. Le système enregistre la demande et l’action réalisée.
8. Le système retourne le résultat.

## Sortie

```json
{
  "category": "urgence",
  "confidence": 0.98,
  "action": "TRANSFER_IMMEDIATELY"
}
```

## Règle importante

Le système ne doit pas :

- établir un diagnostic ;
- interpréter les symptômes ;
- conseiller un traitement ;
- remplacer un professionnel de santé.

Il doit uniquement détecter un risque potentiel et déclencher la procédure de transfert prévue.

## Cas alternatif

Si le score d’urgence est proche du seuil défini, le système peut transmettre la demande à un humain pour vérification.

## Postconditions

- La demande urgente est priorisée.
- Le transfert est demandé.
- L’événement est enregistré dans l’historique.

---

# 5. UC03 — Interroger la FAQ

## Objectif

Trouver une réponse validée à une question fréquente du patient.

## Acteur principal

Patient.

## Préconditions

- La bibliothèque FAQ est disponible.
- Elle contient au moins une question active.
- La demande n’est pas considérée comme urgente.

## Entrée

```json
{
  "question": "Est-ce que le cabinet est ouvert le samedi ?"
}
```

## Scénario nominal

1. Le système reçoit la question.
2. Le système vérifie que la demande n’est pas urgente.
3. Le système détermine que la question peut être traitée par la FAQ.
4. Le système recherche les questions actives les plus proches.
5. Le système calcule un score de similarité.
6. La meilleure réponse dépasse le seuil minimal.
7. Le système retourne la réponse correspondante.
8. La consultation est enregistrée dans l’historique.

## Sortie

```json
{
  "answer": "Le cabinet est ouvert du lundi au vendredi de 8h30 à 18h00.",
  "matched_faq_id": 12,
  "confidence": 0.91,
  "action": "ANSWER_WITH_FAQ"
}
```

## Cas alternatif

Si aucune réponse suffisamment fiable n’est trouvée :

```json
{
  "answer": null,
  "matched_faq_id": null,
  "confidence": 0.38,
  "action": "TRANSFER_TO_HUMAN"
}
```

## Postconditions

- Une réponse fiable est fournie, ou
- la demande est transmise à un humain.

---

# 6. UC04 — Gérer une demande non comprise

## Objectif

Éviter de fournir une réponse incorrecte lorsque la demande est ambiguë ou inconnue.

## Acteur principal

Patient.

## Préconditions

- Le texte a été analysé.
- Aucun résultat ne dépasse le seuil de confiance défini.

## Entrée

```json
{
  "text": "Je voulais savoir pour la chose dont on a parlé l’autre fois"
}
```

## Scénario nominal

1. Le système reçoit la demande.
2. Le modèle produit plusieurs catégories avec des scores faibles.
3. Aucun score ne dépasse le seuil minimal.
4. Le système classe la demande comme `inconnue`.
5. Le système évite de générer une réponse incertaine.
6. La demande est transférée vers une secrétaire.
7. Le résultat est enregistré.

## Sortie

```json
{
  "category": "inconnue",
  "confidence": 0.42,
  "action": "TRANSFER_TO_HUMAN"
}
```

---

# 7. UC05 — Ajouter une FAQ

## Objectif

Permettre à un administrateur d’ajouter une nouvelle question fréquente.

## Acteur principal

Administrateur.

## Préconditions

- L’administrateur est authentifié.
- L’administrateur possède les permissions nécessaires.

## Données saisies

- question ;
- réponse ;
- catégorie ;
- mots-clés ;
- statut actif ou inactif.

## Entrée

```json
{
  "question": "Quels moyens de paiement acceptez-vous ?",
  "answer": "Le cabinet accepte les paiements par carte bancaire, chèque et espèces.",
  "category": "informations",
  "keywords": [
    "paiement",
    "carte bancaire",
    "chèque",
    "espèces"
  ],
  "active": true
}
```

## Scénario nominal

1. L’administrateur saisit les informations.
2. Le système vérifie les champs obligatoires.
3. Le système vérifie qu’une FAQ identique n’existe pas déjà.
4. Le système enregistre la nouvelle FAQ.
5. La FAQ devient disponible pour les recherches si elle est active.
6. Le système retourne une confirmation.

## Sortie

```json
{
  "id": 15,
  "message": "La FAQ a été ajoutée avec succès."
}
```

## Cas d’erreur

- Question vide.
- Réponse vide.
- Catégorie invalide.
- FAQ déjà existante.
- Utilisateur non autorisé.

---

# 8. UC06 — Modifier une FAQ

## Objectif

Permettre la correction ou la mise à jour d’une FAQ existante.

## Acteur principal

Administrateur.

## Scénario nominal

1. L’administrateur sélectionne une FAQ.
2. Il modifie une ou plusieurs informations.
3. Le système vérifie les nouvelles valeurs.
4. Le système enregistre les modifications.
5. Le système met à jour la date de modification.
6. Le système retourne une confirmation.

## Exemple

```json
{
  "answer": "Le cabinet est ouvert du lundi au vendredi de 8h00 à 18h00.",
  "active": true
}
```

---

# 9. UC07 — Désactiver une FAQ

## Objectif

Empêcher l’utilisation d’une FAQ devenue incorrecte ou obsolète.

## Acteur principal

Administrateur.

## Scénario nominal

1. L’administrateur sélectionne la FAQ.
2. Il modifie son statut.
3. Le système définit `active` à `false`.
4. La FAQ reste enregistrée dans la base.
5. Elle n’est plus utilisée pour répondre aux patients.

## Sortie

```json
{
  "id": 12,
  "active": false,
  "message": "La FAQ a été désactivée."
}
```

---

# 10. UC08 — Corriger une classification

## Objectif

Permettre à une secrétaire de corriger une prédiction incorrecte.

## Acteur principal

Secrétaire médicale.

## Préconditions

- La classification existe dans l’historique.
- La secrétaire est authentifiée.
- Elle possède les permissions nécessaires.

## Exemple

```text
Prédiction initiale : informations
Catégorie correcte : administratif
```

## Entrée

```json
{
  "classification_id": 128,
  "predicted_category": "informations",
  "corrected_category": "administratif",
  "comment": "Le patient demandait un document administratif."
}
```

## Scénario nominal

1. La secrétaire consulte une classification.
2. Elle détecte une mauvaise catégorie.
3. Elle indique la catégorie correcte.
4. Elle peut ajouter un commentaire.
5. Le système enregistre la correction.
6. La prédiction initiale reste conservée pour assurer la traçabilité.
7. La correction pourra être utilisée ultérieurement pour améliorer le dataset.

## Sortie

```json
{
  "classification_id": 128,
  "correction_saved": true,
  "message": "La correction a été enregistrée."
}
```

---

# 11. UC09 — Router une demande vers un service

## Objectif

Déterminer l’action à exécuter après la classification.

## Acteur principal

Système.

## Scénario nominal

1. La demande est classifiée.
2. Le score est supérieur au seuil minimal.
3. Le système associe la catégorie à une action.
4. La demande est transmise au service approprié.

## Exemples de routage

| Catégorie | Action possible |
|---|---|
| urgence | `TRANSFER_IMMEDIATELY` |
| rendez-vous | `ROUTE_TO_APPOINTMENT_SERVICE` |
| devis | `ROUTE_TO_QUOTE_SERVICE` |
| informations | `SEARCH_FAQ` |
| administratif | `ROUTE_TO_ADMINISTRATIVE_SERVICE` |
| laboratoire | `ROUTE_TO_LAB_SERVICE` |
| pharmacie | `ROUTE_TO_PHARMACY_SERVICE` |
| inconnue | `TRANSFER_TO_HUMAN` |

Les actions définitives devront être validées avec les responsables des autres modules.

---

# 12. UC10 — Consulter l’historique

## Objectif

Permettre à un utilisateur autorisé de consulter les classifications précédentes.

## Acteurs concernés

- secrétaire ;
- administrateur.

## Informations affichées

- identifiant de la demande ;
- texte reçu ;
- catégorie prédite ;
- score de confiance ;
- action exécutée ;
- modèle utilisé ;
- date et heure ;
- temps de traitement ;
- correction humaine éventuelle.

## Cas d’erreur

- Utilisateur non autorisé.
- Historique indisponible.
- Classification inexistante.

---

# 13. Tableau récapitulatif

| Identifiant | Cas d’utilisation | Acteur principal |
|---|---|---|
| UC01 | Classifier une demande | Patient / Module 3 |
| UC02 | Détecter une urgence | Patient / Module 3 |
| UC03 | Interroger la FAQ | Patient |
| UC04 | Gérer une demande non comprise | Système |
| UC05 | Ajouter une FAQ | Administrateur |
| UC06 | Modifier une FAQ | Administrateur |
| UC07 | Désactiver une FAQ | Administrateur |
| UC08 | Corriger une classification | Secrétaire |
| UC09 | Router une demande | Système |
| UC10 | Consulter l’historique | Secrétaire / Administrateur |

---

# 14. Points à valider

Les éléments suivants restent à confirmer avec l’encadrant :

- la liste définitive des actions de routage ;
- la présence d’une catégorie `inconnue` ;
- le seuil général de confiance ;
- le seuil particulier de détection des urgences ;
- les utilisateurs autorisés à gérer la FAQ ;
- la possibilité d’utiliser les corrections pour réentraîner le modèle ;
- le format des échanges avec les Modules 1 et 3 ;
- le contenu exact de l’historique.