# EternaDream Control Nexus — Suite locale Windows

Cette branche fournit une reconstruction complète d’Eterna 3.1 en application **100 % locale** pour Windows : interface WPF (.NET 8), backend Python modulaire et configuration prête pour un déploiement via Inno Setup. Aucun serveur web ou dépendance front-end web n’est requis.

## Structure du dépôt

```
Eterna2/
├── frontend/                # Projet WPF .NET 8 (Core Nexus + roadmap autonomie)
│   ├── Eterna.Desktop.csproj
│   ├── App.xaml(.cs)
│   ├── MainWindow.xaml(.cs)
│   ├── Assets/
│   └── ViewModels/, Models/, Commands/
├── backend/                 # Backend Python local-first
│   ├── eterna_core_manager.py
│   ├── ios_bridge.py
│   └── modules/
│       ├── llama_service.py, whisper_service.py, tts_service.py
│       ├── memory_manager.py, emotion_service.py, system_control.py
│       ├── image_service.py, network_manager.py
│       └── commerce_manager.py, security_manager.py, self_update_manager.py, task_orchestrator.py
├── Config/                  # Configuration locale (AppConfig, règles réseau, mémoire)
├── installers/              # Script Inno Setup + vérification dépendances
├── assets/logo.png          # Placeholder texte : remplacez-le par le logo Eternadream officiel avant compilation
├── docs/                    # Guides de conception
├── specs/                   # Spécifications matérielles de référence
└── startup_check.py         # Auto-test de démarrage des modules backend
```

## Fonctionnalités clés

- **Core Nexus** WPF en thème violet/rouge/or avec halo animé, logo Eternadream centré et panneaux CPU/GPU + état émotionnel.
- **Communication locale** via canal nommé `\\\\.\\pipe\\eterna_ipc` : le frontend tente automatiquement de consommer le heartbeat du backend, puis repasse en simulation si le pipe est indisponible.
- **Backend modulaire** couvrant mémoire long terme (ChromaDB/TinyDB), analyse émotionnelle (DeepFace + SpeechBrain), contrôle PC (PyAutoGUI + psutil + OpenRGB), génération IA (LLaMA/Whisper/TTS), sécurité (FaceNet + PyOTP), commerce (Shopify/Printify/Etsy), sauvegarde Git, orchestration (APScheduler + LangGraph) et passerelle iOS Socket.IO.
- **Gestion réseau locale** via `network_manager.py` : enregistre tous les accès dans `Logs/network.log`, applique les règles `Config/NetworkRules.json` et n’ouvre qu’un canal IPC local.
- **Installateur Windows** (`installers/eterna_setup.iss`) et vérification automatique (`check_dependencies.py`) des versions Python 3.11 / Torch 2.2.2 / CUDA 12.4 et outils systèmes.

## Prérequis

- Windows 10/11 64 bits.
- SDK .NET 8 avec le workload « Desktop development with C# » ou l’outil en ligne de commande `dotnet-wpf`.
- Python 3.11 et PyTorch 2.2.2 compatible CUDA 12.4 (pour exploiter GPU et modèles IA locaux).
- Dépendances optionnelles (installez-les selon vos besoins) : `chromadb`, `tinydb`, `transformers`, `TTS`, `whisper`, `speechbrain`, `realesrgan`, `rembg`, `gitpython`, `guardrails-ai`, `psutil`, `pyautogui`, `openrgb-python`, `python-socketio`, `apscheduler`, `langgraph`, etc.

## Compilation et exécution (interface WPF)

```bash
dotnet build frontend/Eterna.Desktop.csproj -p:EnableWindowsTargeting=true
dotnet run --project frontend/Eterna.Desktop.csproj -p:EnableWindowsTargeting=true
```

Le tableau de bord démarre en mode simulation si le backend n’est pas joignable ; la bannière d’état reflète la connexion IPC.

## Vérification des modules backend

```bash
python -m venv .venv
. .venv/bin/activate  # sous Windows : .venv\Scripts\activate
pip install -r requirements.txt  # à composer selon vos modules
python startup_check.py
```

Le script affiche un rapport JSON listant mémoire, émotions, contrôle système, image, commerce, sécurité, orchestration, services IA et état réseau. Il importe directement les classes depuis `backend.modules` et la façade `EternaCoreManager`.

## Configuration réseau et mémoire

- `Config/NetworkRules.json` définit les domaines autorisés pour les téléchargements (HuggingFace, Shopify, Printify, Etsy, ngrok…).
- `Config/AppConfig.json` centralise les chemins de modèles, emplacements mémoire et couleurs de thème.
- `Config/Memory/` reçoit les bases JSON/TinyDB générées par `EternaMemoryManager`.
- Les logs réseau sont écrits dans `Logs/network.log` ; créez le dossier au déploiement si nécessaire.
- Le logo Eternadream n'est pas versionné en binaire : placez `logo_or_rouge_no_text_transparent_300dpi.png` dans `assets/logo.png` ou `frontend/Assets/logo.png` avant la publication.

## Installateur

1. Publiez le projet WPF en `Release` cible `win10-x64` (`dotnet publish frontend/Eterna.Desktop.csproj -c Release -r win10-x64 --self-contained false`).
2. Exécutez `installers/check_dependencies.py` pour valider l’environnement.
3. Construisez l’installateur via Inno Setup en utilisant `installers/eterna_setup.iss`.

## Feuille de route locale

- Connecter le `NetworkManager` aux modules pour journaliser chaque téléchargement de modèle.
- Implémenter le serveur Named Pipe côté backend (par exemple via `multiprocessing.connection.Listener`) afin de répondre aux requêtes heartbeat du frontend.
- Étendre `EternaCoreManager` pour pousser les états émotionnels en temps réel et déclencher des actions planifiées via `APScheduler`.
- Ajouter des tests unitaires couvrant la lecture/écriture mémoire, le protocole de backup Git et les règles réseau.

Le projet reste totalement local : aucune page web, aucun serveur HTTP, mais un accès Internet sortant contrôlé pour les API et téléchargements autorisés.
