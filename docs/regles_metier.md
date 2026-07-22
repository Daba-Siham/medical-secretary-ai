# Règles métier — Module 4

## 1. Présentation

Ce document décrit les premières règles métier du Module 4 — Qualification des appels et FAQ.

Ces règles sont définies pendant la phase d’analyse. Elles pourront être modifiées après validation avec l’encadrant et après les premières expérimentations.

---

# 2. Règles liées aux données reçues

## RM01 — Texte obligatoire

Toute demande envoyée au service de classification doit contenir un texte non vide.

### Cas accepté

```json
{
  "text": "Je souhaite prendre un rendez-vous."
}
```

### Cas refusé

```json
{
  "text": ""
}
```

### Action

Le système retourne une erreur de validation lorsque le texte est vide ou absent.

---

## RM02 — Normalisation du texte

Avant la classification, le texte peut être normalisé.

La normalisation peut inclure :

- la suppression des espaces inutiles ;
- l’uniformisation de la casse ;
- la correction de certains caractères ;
- la suppression d’éléments sans valeur pour la classification.

Le texte original doit toutefois être conservé dans l’historique.

---

## RM03 — Longueur minimale et maximale

Le système doit définir une longueur minimale et maximale pour le texte reçu.

Les valeurs définitives seront fixées pendant la conception technique.

Une demande trop courte ou anormalement longue pourra être rejetée ou transmise à un humain.

---

# 3. Règles de classification

## RM04 — Catégories autorisées

Une demande doit être associée à l’une des catégories suivantes :

- `urgence` ;
- `rendez-vous` ;
- `devis` ;
- `informations` ;
- `administratif` ;
- `laboratoire` ;
- `pharmacie`.

Une catégorie supplémentaire `inconnue` peut être utilisée lorsque le système ne peut pas déterminer une catégorie avec suffisamment de confiance.

Cette catégorie doit être validée avec l’encadrant.

---

## RM05 — Une catégorie principale par demande

Dans la première version, chaque demande reçoit une seule catégorie principale.

Exemple :

```json
{
  "category": "rendez-vous"
}
```

La gestion de plusieurs intentions dans une même phrase pourra être étudiée ultérieurement.

Exemple de demande multi-intention :

```text
Je voudrais prendre rendez-vous et connaître le prix de la consultation.
```

---

## RM06 — Score de confiance obligatoire

Chaque classification doit être accompagnée d’un score de confiance compris entre `0` et `1`.

Exemple :

```json
{
  "category": "rendez-vous",
  "confidence": 0.91
}
```

---

## RM07 — Seuil général de confiance

Une première valeur provisoire peut être définie :

```text
Confiance ≥ 0,75 → accepter la classification
Confiance < 0,75 → transférer vers une personne
```

Le seuil définitif devra être déterminé à partir :

- des résultats des modèles ;
- de la matrice de confusion ;
- du niveau de risque associé aux erreurs ;
- des besoins métier.

La valeur `0,75` est donc une hypothèse initiale et non une valeur définitive.

---

## RM08 — Demande inconnue ou ambiguë

Lorsque le score de confiance est inférieur au seuil général :

```json
{
  "category": "inconnue",
  "action": "TRANSFER_TO_HUMAN"
}
```

Le système ne doit pas inventer une catégorie ou fournir une réponse non fiable.

---

# 4. Règles liées aux urgences

## RM09 — Priorité absolue aux urgences

Toute demande considérée comme urgente doit être traitée avant :

- la recherche dans la FAQ ;
- le routage vers les services normaux ;
- la génération d’une réponse automatique.

Flux :

```text
Demande
   ↓
Classification
   ↓
Urgence ?
 ├── Oui → transfert immédiat
 └── Non → traitement normal
```

---

## RM10 — Seuil spécifique pour l’urgence

La classe `urgence` peut utiliser un seuil plus prudent que les autres catégories.

Exemple initial :

```text
Probabilité urgence ≥ 0,50
→ déclencher une vérification ou un transfert
```

Cette valeur devra être déterminée après évaluation du modèle.

L’objectif est de limiter les faux négatifs, c’est-à-dire les urgences non détectées.

---

## RM11 — Règles de sécurité complémentaires

La détection d’urgence peut combiner :

- le score du modèle ;
- des mots ou expressions sensibles ;
- des règles définies avec des professionnels compétents ;
- le contexte de la demande.

Les règles médicales définitives ne doivent pas être inventées par l’équipe technique. Elles devront être validées par une personne qualifiée.

---

## RM12 — Aucun diagnostic

Le système ne doit jamais :

- annoncer qu’un patient souffre d’une maladie ;
- confirmer un diagnostic ;
- interpréter un résultat médical ;
- recommander un médicament ;
- prescrire un traitement ;
- remplacer un médecin ou un professionnel de santé.

Le système doit seulement détecter un risque potentiel et déclencher la procédure prévue.

---

## RM13 — Message en cas d’urgence

Lorsqu’une urgence potentielle est détectée, le système doit utiliser un message neutre.

Exemple provisoire :

```text
Votre demande nécessite une prise en charge prioritaire.
Je vais vous transférer immédiatement vers le service prévu.
```

Le contenu définitif du message devra être validé.

---

# 5. Règles de routage

## RM14 — Association entre catégorie et action

Chaque catégorie doit correspondre à une action.

| Catégorie | Action provisoire |
|---|---|
| urgence | `TRANSFER_IMMEDIATELY` |
| rendez-vous | `ROUTE_TO_APPOINTMENT_SERVICE` |
| devis | `ROUTE_TO_QUOTE_SERVICE` |
| informations | `SEARCH_FAQ` |
| administratif | `ROUTE_TO_ADMINISTRATIVE_SERVICE` |
| laboratoire | `ROUTE_TO_LAB_SERVICE` |
| pharmacie | `ROUTE_TO_PHARMACY_SERVICE` |
| inconnue | `TRANSFER_TO_HUMAN` |

Cette table est provisoire et devra être validée avec les autres modules.

---

## RM15 — La FAQ n’est pas utilisée pour toutes les catégories

Une demande non urgente ne doit pas automatiquement être envoyée vers la FAQ.

Exemples :

- une demande de rendez-vous doit être transmise au service de rendez-vous ;
- une question sur les horaires peut être traitée par la FAQ ;
- une demande administrative spécifique peut être transférée au service administratif ;
- une demande inconnue doit être transmise à un humain.

---

## RM16 — Échec du service cible

Si le service cible est indisponible :

1. le système enregistre l’échec ;
2. le système ne perd pas la demande ;
3. la demande est placée en attente ou transférée vers un humain ;
4. une erreur contrôlée est retournée.

Le comportement définitif dépendra de l’architecture globale.

---

# 6. Règles de la FAQ

## RM17 — FAQ paramétrable

Une FAQ doit contenir au minimum :

- un identifiant ;
- une question ;
- une réponse ;
- une catégorie ;
- des mots-clés éventuels ;
- un statut actif ou inactif ;
- une date de création ;
- une date de modification.

---

## RM18 — Question et réponse obligatoires

Une FAQ ne peut pas être créée si :

- la question est vide ;
- la réponse est vide ;
- la catégorie est invalide.

---

## RM19 — FAQ inactive

Une FAQ avec :

```text
active = false
```

ne doit jamais être utilisée pour répondre à un patient.

Elle peut cependant rester enregistrée dans la base pour assurer la traçabilité.

---

## RM20 — Recherche uniquement dans les FAQ actives

Lors d’une recherche, le système doit filtrer les FAQ inactives avant de calculer la similarité.

---

## RM21 — Seuil minimal de similarité

Une réponse FAQ ne doit être retournée que si son score dépasse un seuil minimal.

Exemple provisoire :

```text
Similarité ≥ 0,70 → retourner la réponse
Similarité < 0,70 → transférer à une secrétaire
```

La valeur définitive sera choisie après les tests.

---

## RM22 — Absence de réponse fiable

Lorsque la similarité est insuffisante, le système ne doit pas inventer de réponse.

Exemple de message :

```text
Je ne dispose pas d’une réponse suffisamment fiable à votre question.
Je vais transmettre votre demande à une secrétaire.
```

Action associée :

```text
TRANSFER_TO_HUMAN
```

---

## RM23 — Réponse basée sur un contenu validé

La réponse fournie au patient doit provenir d’un contenu FAQ validé.

Si un LLM est utilisé pour reformuler la réponse, il ne doit pas ajouter d’informations absentes de la FAQ sélectionnée.

---

## RM24 — Modification d’une FAQ

Lorsqu’une FAQ est modifiée, le système doit conserver :

- la date de modification ;
- l’utilisateur ayant réalisé la modification ;
- éventuellement l’ancienne version.

La gestion complète des versions doit être confirmée.

---

## RM25 — Suppression logique recommandée

Il est préférable de désactiver une FAQ plutôt que de la supprimer définitivement.

Exemple :

```text
active = false
```

Cela permet de conserver l’historique.

---

# 7. Règles relatives aux corrections humaines

## RM26 — Conservation de la prédiction initiale

Lorsqu’une secrétaire corrige une classification, la prédiction initiale ne doit pas être écrasée.

Le système doit conserver :

- la catégorie prédite ;
- le score initial ;
- la catégorie corrigée ;
- l’auteur de la correction ;
- la date de correction ;
- un commentaire éventuel.

---

## RM27 — Utilisation des corrections

Les corrections humaines pourront être utilisées pour :

- analyser les erreurs du modèle ;
- enrichir le dataset ;
- préparer un nouvel entraînement ;
- améliorer les performances futures.

Une validation des données devra être réalisée avant leur ajout au dataset d’entraînement.

---

# 8. Règles de traçabilité

## RM28 — Historisation des traitements

Chaque traitement doit conserver au minimum :

```text
identifiant
texte original reçu
texte éventuellement normalisé
catégorie prédite
score de confiance
action exécutée
date et heure
méthode utilisée
nom du modèle
version du modèle
temps de traitement
réponse FAQ éventuelle
correction humaine éventuelle
```

---

## RM29 — Identification du modèle

Chaque prédiction doit être associée au modèle qui l’a produite.

Exemple :

```json
{
  "model_name": "linear_svm",
  "model_version": "1.0.0"
}
```

---

## RM30 — Temps de traitement

Le système doit mesurer le temps nécessaire pour traiter une demande.

Exemple :

```json
{
  "processing_time_ms": 125
}
```

Cette information permettra de comparer les solutions Machine Learning et LLM.

---

# 9. Règles de confidentialité et de sécurité

## RM31 — Minimisation des données

Le système doit stocker uniquement les données nécessaires au fonctionnement et à l’évaluation du module.

---

## RM32 — Données sensibles

Les données médicales et personnelles ne doivent pas être exposées dans :

- les logs techniques ;
- les messages d’erreur ;
- le dépôt Git ;
- les datasets publics ;
- les captures d’écran du rapport.

---

## RM33 — Contrôle des accès

Seuls les utilisateurs autorisés peuvent :

- consulter l’historique ;
- modifier la FAQ ;
- corriger les classifications ;
- accéder aux données sensibles.

La gestion des rôles dépendra du Module 1.

---

## RM34 — Logs sécurisés

Les logs doivent contenir les informations techniques nécessaires sans exposer inutilement les données du patient.

---

# 10. Règles relatives aux erreurs

## RM35 — Gestion contrôlée des erreurs

Le système doit retourner des messages d’erreur structurés.

Exemple :

```json
{
  "error": {
    "code": "EMPTY_TEXT",
    "message": "Le texte de la demande est obligatoire."
  }
}
```

---

## RM36 — Aucun détail technique sensible

Les erreurs retournées au client ne doivent pas contenir :

- une trace complète de l’exception ;
- des informations de connexion à la base ;
- des clés API ;
- des chemins internes sensibles.

---

## RM37 — Indisponibilité du modèle

Si le modèle est indisponible, le système doit :

1. enregistrer l’erreur ;
2. éviter de produire une fausse prédiction ;
3. transférer la demande vers un humain lorsque cela est possible.

---

# 11. Tableau récapitulatif

| Règle | Description |
|---|---|
| RM01 | Texte obligatoire |
| RM02 | Normalisation du texte |
| RM03 | Longueur du texte contrôlée |
| RM04 | Catégories autorisées |
| RM05 | Une catégorie principale |
| RM06 | Score de confiance obligatoire |
| RM07 | Seuil général de confiance |
| RM08 | Gestion des demandes inconnues |
| RM09 | Priorité aux urgences |
| RM10 | Seuil spécifique pour l’urgence |
| RM11 | Règles complémentaires de sécurité |
| RM12 | Aucun diagnostic médical |
| RM13 | Message neutre en cas d’urgence |
| RM14 | Association catégorie-action |
| RM15 | FAQ non systématique |
| RM16 | Gestion d’un service indisponible |
| RM17 | FAQ paramétrable |
| RM18 | Question et réponse obligatoires |
| RM19 | FAQ inactive non utilisée |
| RM20 | Recherche dans les FAQ actives |
| RM21 | Seuil minimal de similarité |
| RM22 | Absence de réponse fiable |
| RM23 | Réponse basée sur un contenu validé |
| RM24 | Traçabilité des modifications |
| RM25 | Suppression logique recommandée |
| RM26 | Conservation de la prédiction initiale |
| RM27 | Utilisation contrôlée des corrections |
| RM28 | Historisation des traitements |
| RM29 | Identification du modèle |
| RM30 | Mesure du temps de traitement |
| RM31 | Minimisation des données |
| RM32 | Protection des données sensibles |
| RM33 | Contrôle des accès |
| RM34 | Logs sécurisés |
| RM35 | Erreurs structurées |
| RM36 | Protection des détails techniques |
| RM37 | Gestion de l’indisponibilité du modèle |

---

# 12. Éléments à valider

Les règles suivantes nécessitent une validation :

- le seuil général de confiance ;
- le seuil spécifique de l’urgence ;
- le seuil de similarité de la FAQ ;
- les règles médicales complémentaires ;
- le message utilisé lors d’une urgence ;
- la table de routage ;
- le traitement des demandes multi-intentions ;
- la politique de conservation des données ;
- la gestion des versions des FAQ ;
- la politique d’utilisation des corrections humaines.