# EternaDream Control Nexus — Application Windows

Cette version du projet matérialise le cockpit **Eterna 3.1 Self-Coding & Autonomy** sous la forme d'une application **WPF** native pour Windows. Elle s'appuie sur les spécifications `specs/Eterna_3.0_Ultimate_ECX_Partner_Specs.txt` et expose l'intégralité de la roadmap "Full Stack Local IA" v3.1 demandée.

## Contenu du dépôt

- `Eterna.Desktop/` : projet WPF (.NET 7) fournissant l'application Windows.
- `docs/ui_design_solutions.md` : dossier de conception décrivant les logiques d'écran et les parcours associés.
- `specs/Eterna_3.0_Ultimate_ECX_Partner_Specs.txt` : fiche technique complète servant de base fonctionnelle.

## Fonctionnalités clés

- Tableau de bord principal du module **Self-Coding & Autonomy** : backups chiffrés, files de changements, journal d'autonomie, watcher interne et adaptation émotionnelle.
- **Liste exhaustive des 10 modules manquants v3.1** avec objectifs, priorités, impacts et bibliothèques GitHub associées, directement intégrée à l'expérience.
- Synthèse du protocole d'auto-modification (backups, validations, sandbox, auto-test, rollback) affichée dans l'application.
- Génération de backups simulés et mise à jour des journaux afin de tester l'orchestration locale.

## Prérequis

- Windows 10 ou supérieur avec le **.NET SDK 7.0** (ou ultérieur) et le workload `Desktop development with C#` (Visual Studio) ou `dotnet-wpf` (CLI).

## Compilation et exécution

```bash
cd Eterna.Desktop
 dotnet build
 dotnet run
```

La commande `dotnet run` ouvrira la fenêtre "Eterna 3.1 — Cockpit d'autonomie locale". Le dépôt ne contient aucune dépendance externe : toutes les données affichées sont simulées côté client.

## Ressources visuelles

Le logo officiel `logo_or_rouge_no_text_transparent_300dpi.png` doit être ajouté dans un dossier `assets/` si vous souhaitez l'afficher dans l'application. **Ne le modifiez jamais** conformément aux directives partenaires.

## Prochaines étapes suggérées

- Brancher les commandes de backup, validation et watchers à un backend FastAPI sandboxé.
- Implémenter la mémoire long terme locale (ChromaDB / FAISS) et les contrôles PC (psutil, PyAutoGUI) via interopérabilité.
- Ajouter la synchronisation iOS (FastAPI WebSocket + SwiftNIO) et renforcer la sécurité biométrique.
- Étendre les vues WPF vers un système multi-fenêtres (Performance Command Center, Showroom, Fleet Portal).
