# EternaDream Control Nexus – Interface Concepts

This document outlines three complete interface solutions for the companion application requested for the Eterna 3.0 Ultimate ECX Partner system. Each concept is grounded in the official hardware specification and tailored to different partner priorities.

## Shared Design System Principles
- **Branding**: Crimson-and-gold palette inspired by the titanium chassis accents and EternaDream logo. Typography pairs a bold geometric display font for headings with a highly legible sans-serif for data tables.
- **Layout Grid**: 12-column responsive grid with modular cards and contextual drawers for quick actions.
- **Data Visualization**: Smoothly animated radial gauges for thermal/power metrics and stacked line graphs for telemetry history. Uses color-coded thresholds aligned with acoustic/thermal targets.
- **Device Awareness**: Hardware summary drawer surfaces CPU, GPU, memory, storage, and PSU metrics using the telemetry API and power monitoring shunt described in the specification.

## Concept A – Performance Command Center
Designed for esports lounges and creators who need real-time control.

### Key Screens
1. **Home Dashboard**
   - Hero banner showing current performance profile (Silent / Balanced / Turbo) with contextual lighting preview.
   - Dual-column telemetry: CPU & GPU radial gauges with temperature and utilization derived from Ryzen 9 9950X and RTX 5090 sensors.
   - Live acoustic meter to validate the <32 dBA silent target and GPU <82 °C performance target.
2. **Profile Orchestrator**
   - Drag-and-drop curve editor for fan and pump curves tied to the dual-chamber vapor loop and 280 mm radiator.
   - Preset cards for "Creator", "AI Lab", and "Partner Demo" with configurable power limits referencing the 1000 W PSU headroom.
3. **Firmware Studio**
   - Timeline view for OTA updates to BIOS, GPU vBIOS, and lighting controller with rollback checkpoints.

### Differentiators
- Scenario alerts for power surge logs using the integrated 2 kV suppressor data.
- Quick toggle to mirror ambient lighting zones with streaming overlays.

## Concept B – Immersive Showroom Companion
Optimized for sales floors and luxury partner showrooms.

### Key Screens
1. **Welcome Experience**
   - Full-bleed 3D render of the 12L titanium chassis with interactive hotspots for front USB4 ports, fingerprint scanner, and ambient lighting strips.
   - Guided story about the luxury finish, concierge service, and 5-year warranty commitments.
2. **Feature Explorer**
   - Tabbed content modules for Core Platform, Connectivity, Cooling, and Security, pulling data from the spec file.
   - Embedded 360° view toggling lighting moods (Silent Sapphire, Turbo Ember, Partner Signature).
3. **Partner Customization**
   - Drag zones for uploading co-branding assets (with guardrails to preserve the original EternaDream logo) and scheduling showroom scenes.

### Differentiators
- Offline mode caching ensures the experience works in pop-up demo booths.
- Lead capture modal integrates with partner CRM via REST telemetry export.

## Concept C – Enterprise Service Portal
Built for partner operations teams who require fleet visibility and RMA automation.

### Key Screens
1. **Fleet Overview**
   - KPI cards for system health, firmware currency, and support ticket backlog.
   - Map visualization showing deployed systems with intrusion sensor status and TPM health.
2. **Automation Playbooks**
   - Workflow builder for remote tasks: push BIOS update, schedule maintenance reminders for liquid metal service, or adjust power budgets.
   - Audit log referencing the physical intrusion sensor and warranty SLA clock.
3. **Support Concierge**
   - AI-assisted chat leveraging telemetry to troubleshoot CPU/GPU temps, PSU load, or network throughput (dual 10 GbE, Wi-Fi 7).
   - RMA intake wizard using asset tags and partner portal automation.

### Differentiators
- MQTT bridge panel to subscribe or publish to telemetry topics.
- Compliance dashboard ensuring encrypted BIOS recovery and TPM verification.

## Concept D – Self-Coding & Autonomy Module
Extends the companion with an autonomy cockpit qui permet à Eterna 3.0 d’analyser, modifier et tester son propre code en local.

### Key Screens
1. **Autonomy Cycle Monitor**
   - Hero strip summarising backup timestamp, validation mode (manuel vs automatique) et statut de la sandbox FastAPI isolée.
   - Visual pipeline (Observation → Proposition → Validation → Application → Vérification → Mémorisation) highlighting the active phase.
2. **Secure Backup & Rollback Vault**
   - Cards listing `AUTO_BACKUP_YYYYMMDD_HHMMSS` snapshots, taille chiffrée, et actions de restauration instantanée.
   - Live logbook (`AUTO_PATCH_*`) qui archive validations, tests sandbox et rollbacks.
3. **Autonomous Change Queue**
   - Kanban lite classant les patchs par criticité (UI, Sécurité, IA) avec boutons de validation/approbation selon le protocole décrit.
   - Emotion slider pilotant la stratégie (stabilité vs innovation) relié au module d’analyse émotionnelle.
4. **Sandbox & Watcher Control**
   - Statuts des watchers (UI, backend FastAPI, modèles émotionnels) et résultats des tests (18/18 checks) exécutés dans un venv isolé.
   - CTA pour déclencher un nouvel auto-test ou exporter les journaux vers `Eterna\Logs\Autonomy`.

### Differentiators
- Simule entièrement le protocole d’auto-modification : backup automatique, validation manuelle obligatoire pour les patchs sensibles, auto-test sandbox et rollback sécurisé.
- Prépare l’intégration future avec OpenDevin / Auto-GPT en exposant des points d’extension backend (FastAPI) et watchers Python.
- Visualise l’impact émotionnel (ton utilisateur) sur la priorisation des améliorations grâce au module d’adaptation contextuelle.

## Implementation Roadmap
1. **Information Architecture**: Build navigation schema that allows switching between the four interface modes from a shared shell.
2. **Design Tokens**: Encode color, typography, spacing, and lighting accent variables for reuse.
3. **Component Library**: Develop card, telemetry gauge, map, workflow builder, sandbox monitor, and modal components as responsive web components.
4. **Prototype Build**: Implement interactive prototype (see `/web` directory) with theme toggles representing chaque concept dont le module autonome.
5. **Validation**: Conduct partner workshops aligning features with service-level expectations from the spec, especially OTA updates and concierge support.
