# Documentation d’architecture du Module 4

Ce dossier contient la documentation technique du Module 4 —
Qualification des appels et FAQ.

Le module reçoit une demande sous forme de texte, identifie sa catégorie,
détecte les urgences, détermine l’action appropriée et recherche une réponse
dans la FAQ lorsque cela est pertinent.

## Contenu du dossier

- `flux_appels.md` : description technique du traitement d’une demande.
- `architecture_module.md` : présentation des composants internes du module.
- `modeles_donnees.md` : définition des objets échangés par le module.
- `api_rest.md` : contrats des interfaces REST.
- `diagrams/architecture_module.drawio` : architecture générale du Module 4.
- `diagrams/flux_qualification.drawio` : flux de qualification d’une demande.
- `diagrams/sequence_classification.drawio` : séquence de traitement d’une demande.
- `diagrams/exports/` : versions PNG ou SVG des diagrammes.
- `api_rest.md` : documentation des endpoints REST, des formats d’entrée/sortie et des erreurs.
- `sequence_classification.md` : description des échanges entre les composants pendant la qualification d’une demande.

## Organisation des diagrammes

Les fichiers `.drawio` sont les fichiers sources modifiables.

Les fichiers PNG ou SVG sont utilisés dans :

- le dépôt GitHub ;
- le rapport de stage ;
- les présentations ;
- la documentation technique.

## Hypothèses actuelles

- Le Module 4 reçoit une demande sous forme de texte.
- La transcription audio est réalisée par le Module 3.
- Une demande possède une catégorie principale.
- Les urgences sont traitées avant toute recherche dans la FAQ.
- Une demande non comprise est transférée à un humain.
- La FAQ contient des réponses validées.
- Les autres modules peuvent être simulés à l’aide de mocks.