# Eterna2

Eterna2 is a fully local Windows experience delivering autonomous creativity and system management. The backend is written in Python and the frontend is a native WPF application targeting .NET 8.

## Project Layout

- `backend/` — Python modules that power autonomy, AI generation, emotion detection, and system control.
- `frontend/` — WPF desktop application with the Eternadream Control Nexus interface.
- `Config/` — Application configuration files and memory store.
- `installers/` — Packaging scripts and dependency checks for Windows delivery.
- `assets/` — Placeholder for the official Eternadream logo.
- `docs/` — UI design documentation and specifications.

## Local Requirements

- Python 3.11+
- CUDA 12.4 compatible NVIDIA GPU (for Torch 2.2.2 and acceleration)
- .NET 8 SDK for building the desktop interface

## Startup Check

Run the startup check to verify module availability:

```bash
python startup_check.py
```

The script validates that each backend module can be imported and initialised with default parameters.
