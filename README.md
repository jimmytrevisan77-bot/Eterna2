# EternaDream Control Nexus Prototype

Prototype d'application pour le système **Eterna 3.0 Ultimate ECX Partner**. Ce dépôt contient :

- Les spécifications produit de référence (`specs/Eterna_3.0_Ultimate_ECX_Partner_Specs.txt`).
- Trois propositions d'interfaces complètes détaillées dans `docs/ui_design_solutions.md`.
- Une maquette interactive statique située dans le dossier `web/` permettant de parcourir les quatre concepts d'interface.
- Un module "Self-Coding & Autonomy" simulant la boucle de sauvegarde, validation et sandbox décrite pour Eterna 3.0.
- Un tableau de bord "Full Stack Local IA v3.1" détaillant les 10 modules stratégiques manquants (mémoire, NLU, émotions, PC,
  sécurité, e-commerce, etc.).

## Utilisation

1. Placer le fichier officiel du logo `logo_or_rouge_no_text_transparent_300dpi.png` dans le dossier `assets/` sans le modifier.
2. Ouvrir `web/index.html` dans un navigateur moderne pour explorer les concepts.
3. Lire `docs/ui_design_solutions.md` pour comprendre les parcours utilisateurs, l'architecture de navigation et les composants clés.

## Technologies

- HTML5 et CSS3 responsifs, basés sur un système de grille 12 colonnes.
- JavaScript minimal pour gérer le changement de concept et l'accessibilité.
- Palette de couleurs et typographies alignées sur l'identité EternaDream.

## Prochaines étapes suggérées

- Ajouter des visualisations réelles en s'appuyant sur les télémétries (shunt PSU, capteurs thermiques, MQTT).
- Connecter la maquette à un backend simulé pour démontrer OTA, RMA et analytics.
- Préparer des exports design (Figma) et composants réutilisables (Storybook) pour accélérer l'industrialisation.
- Prototyper l'orchestrateur d'auto-codage (FastAPI + watcher Python) et brancher l'UI Self-Coding sur des APIs locales.
- Prioriser la livraison des modules v3.1 selon la roadmap (mémoire long terme, NLU, sécurité biométrique, autonomie multi-agents).
