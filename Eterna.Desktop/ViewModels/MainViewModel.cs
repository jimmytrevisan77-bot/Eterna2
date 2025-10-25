using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using Eterna.Desktop.Commands;
using Eterna.Desktop.Models;

namespace Eterna.Desktop.ViewModels;

public class MainViewModel : INotifyPropertyChanged
{
    private ModuleCategory? _selectedModule;
    private string _statusBanner = "Prêt pour la prochaine itération";

    public ObservableCollection<ModuleCategory> ModuleCategories { get; } = new();
    public ObservableCollection<BackupRecord> BackupVault { get; } = new();
    public ObservableCollection<ChangeRequest> ChangeQueue { get; } = new();
    public ObservableCollection<WatcherItem> Watchers { get; } = new();
    public ObservableCollection<AutonomyLogEntry> AutonomyLogs { get; } = new();
    public ObservableCollection<EmotionProfile> EmotionProfiles { get; } = new();

    public RelayCommand CreateBackupCommand { get; }
    public RelayCommand ApproveChangeCommand { get; }
    public RelayCommand RejectChangeCommand { get; }
    public RelayCommand ClearBannerCommand { get; }

    public MainViewModel()
    {
        SeedModules();
        SeedOperationalData();

        CreateBackupCommand = new RelayCommand(_ => CreateBackup());
        ApproveChangeCommand = new RelayCommand(param => UpdateChangeStatus(param as ChangeRequest, "Validé"));
        RejectChangeCommand = new RelayCommand(param => UpdateChangeStatus(param as ChangeRequest, "Rejeté"));
        ClearBannerCommand = new RelayCommand(() => StatusBanner = "");

        SelectedModule = ModuleCategories.FirstOrDefault();
    }

    public ModuleCategory? SelectedModule
    {
        get => _selectedModule;
        set
        {
            if (_selectedModule != value)
            {
                _selectedModule = value;
                OnPropertyChanged();
            }
        }
    }

    public string StatusBanner
    {
        get => _statusBanner;
        set
        {
            if (_statusBanner != value)
            {
                _statusBanner = value;
                OnPropertyChanged();
            }
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));

    private void SeedModules()
    {
        ModuleCategories.Clear();

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "LT",
            Title = "🧠 Mémoire long terme (travail / personnel)",
            Objective = "Permettre à Eterna de se souvenir durablement et de séparer mémoire personnelle et professionnelle.",
            Impact = "Garantit la continuité des projets et l'empathie durable.",
            Priority = "Critique",
            Icon = "🧠",
            Libraries = new[]
            {
                new ModuleLibrary("ChromaDB", "Mémoire vectorielle légère.", "https://github.com/chroma-core/chroma"),
                new ModuleLibrary("FAISS", "Recherche vectorielle rapide par Meta.", "https://github.com/facebookresearch/faiss"),
                new ModuleLibrary("LangChain Memory", "Gestion mémoire conversationnelle.", "https://github.com/langchain-ai/langchain"),
                new ModuleLibrary("TinyDB", "Base locale JSON pour préférences.", "https://github.com/msiemens/tinydb"),
                new ModuleLibrary("Weaviate", "Base de mémoire vectorielle complète auto-hébergeable.", "https://github.com/weaviate/weaviate")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "NLU",
            Title = "💬 Compréhension naturelle du langage",
            Objective = "Comprendre le langage humain sans commandes spécifiques.",
            Impact = "Accès instantané aux intentions utilisateurs.",
            Priority = "Critique",
            Icon = "💬",
            Libraries = new[]
            {
                new ModuleLibrary("Transformers", "Support LLaMA 3, Mistral, etc.", "https://github.com/huggingface/transformers"),
                new ModuleLibrary("FastIntent", "Détection automatique des intentions.", "https://github.com/paulovn/fastintent"),
                new ModuleLibrary("Rasa NLU", "Parsing contextuel des requêtes.", "https://github.com/RasaHQ/rasa"),
                new ModuleLibrary("spaCy + neuralcoref", "Compréhension linguistique avancée.", "https://github.com/explosion/spaCy"),
                new ModuleLibrary("ParlAI", "Modèles de dialogue contextuels.", "https://github.com/facebookresearch/ParlAI")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "EMO",
            Title = "❤️ Compréhension et gestion émotionnelle",
            Objective = "Détecter, comprendre et réagir aux émotions dans la voix, le texte ou les images.",
            Impact = "Renforce la confiance et la co-création empathique.",
            Priority = "Priorité haute",
            Icon = "❤️",
            Libraries = new[]
            {
                new ModuleLibrary("HSEmotion", "Reconnaissance des émotions faciales.", "https://github.com/av-savchenko/hsemotion"),
                new ModuleLibrary("DeepFace", "Reconnaissance faciale et émotionnelle.", "https://github.com/serengil/deepface"),
                new ModuleLibrary("Emotion-LLaMA", "Analyse multimodale texte/audio/visuel.", "https://github.com/ZebangCheng/Emotion-LLaMA"),
                new ModuleLibrary("SpeechBrain Emotion", "Détection émotionnelle vocale.", "https://github.com/speechbrain/speechbrain"),
                new ModuleLibrary("Affectiva SDK", "Analyse émotionnelle visuelle commerciale.", "https://github.com/Affectiva/affdexme")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "PC",
            Title = "💻 Contrôle total du PC (hors achats)",
            Objective = "Permettre à Eterna de gérer le PC, les fichiers, logiciels, périphériques et RGB.",
            Impact = "Automatisation complète de l'environnement utilisateur.",
            Priority = "Priorité haute",
            Icon = "💻",
            Libraries = new[]
            {
                new ModuleLibrary("PyAutoGUI", "Automatisation clavier/souris/écran.", "https://github.com/asweigart/pyautogui"),
                new ModuleLibrary("Psutil", "Monitoring CPU, GPU, RAM.", "https://github.com/giampaolo/psutil"),
                new ModuleLibrary("OpenRGB SDK", "Gestion lumière RGB.", "https://github.com/CalcProgrammer1/OpenRGB"),
                new ModuleLibrary("PyPsexec", "Exécution de commandes Windows.", "https://github.com/jborean93/pypsexec"),
                new ModuleLibrary("Keyboard / Mouse", "Gestion directe des entrées physiques.", "https://github.com/boppreh/keyboard")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "AUTO",
            Title = "🧩 Auto-modification du code + backup",
            Objective = "Permettre à Eterna de réécrire ses propres modules localement avec sauvegarde automatique.",
            Impact = "Autonomie contrôlée et sécurisée.",
            Priority = "Critique",
            Icon = "🧩",
            Libraries = new[]
            {
                new ModuleLibrary("GitPython", "Commits et rollbacks automatiques.", "https://github.com/gitpython-developers/GitPython"),
                new ModuleLibrary("OpenDevin", "Agents d'auto-codage.", "https://github.com/OpenDevin/OpenDevin"),
                new ModuleLibrary("Awesome LLM Agents", "Catalogue de frameworks d'agents.", "https://github.com/yoheinakajima/awesome-llm-agents"),
                new ModuleLibrary("Guardrails.ai", "Validation et sécurité du code généré.", "https://github.com/ShreyaR/guardrails"),
                new ModuleLibrary("GitBackupPy", "Backups automatiques de projets.", "https://github.com/jkallini/git-backup-py")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "VIS",
            Title = "🖼️ Upscale / retouche visuelle automatique",
            Objective = "Améliorer les designs, corriger défauts, restaurer visuels et upscaler automatiquement.",
            Impact = "Rendu premium des créations visuelles.",
            Priority = "Priorité haute",
            Icon = "🖼️",
            Libraries = new[]
            {
                new ModuleLibrary("Real-ESRGAN", "Super-résolution IA.", "https://github.com/xinntao/Real-ESRGAN"),
                new ModuleLibrary("GIMP-Python", "Automatisation des retouches via GIMP.", "https://github.com/GNOME/gimp"),
                new ModuleLibrary("GFPGAN", "Restauration et amélioration des visages.", "https://github.com/TencentARC/GFPGAN"),
                new ModuleLibrary("StableSR", "Upscale par diffusion.", "https://github.com/Iceclear/StableSR"),
                new ModuleLibrary("RemBG", "Suppression automatique de fond.", "https://github.com/danielgatis/rembg")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "COM",
            Title = "🛒 Gestion e-commerce (Shopify, Printify, Etsy)",
            Objective = "Gérer produits, SEO, prix, descriptions, images et publications automatiques.",
            Impact = "Monétisation et distribution automatisées.",
            Priority = "Priorité moyenne",
            Icon = "🛒",
            Libraries = new[]
            {
                new ModuleLibrary("ShopifyAPI", "Intégration complète Shopify.", "https://github.com/Shopify/shopify_python_api"),
                new ModuleLibrary("PrintifyAPI", "Wrapper non officiel.", "https://github.com/ralphbean/printify-api"),
                new ModuleLibrary("Etsy OpenAPI", "SDK officiel Etsy.", "https://github.com/Etsy/open-api"),
                new ModuleLibrary("SEO-Analyzer", "Audit SEO automatique.", "https://github.com/seomoz/SEO-Analyzer"),
                new ModuleLibrary("BeautifulSoup + Requests", "Scrapping tendances Etsy/Printify.", "https://github.com/psf/requests")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "IOS",
            Title = "📱 Synchronisation iOS (remote)",
            Objective = "Contrôler Eterna depuis iPhone, exécution vocale et visuelle à distance.",
            Impact = "Accessibilité totale des fonctionnalités IA.",
            Priority = "Priorité moyenne",
            Icon = "📱",
            Libraries = new[]
            {
                new ModuleLibrary("FastAPI WebSocket", "Communication locale bidirectionnelle.", "https://github.com/tiangolo/fastapi"),
                new ModuleLibrary("Python-Socket.IO", "Liaison directe PC ↔ iOS.", "https://github.com/miguelgrinberg/python-socketio"),
                new ModuleLibrary("PyNgrok", "Tunnel sécurisé entre appareils.", "https://github.com/alexdlaird/ngrok"),
                new ModuleLibrary("SwiftNIO", "Pile réseau native iOS.", "https://github.com/apple/swift-nio"),
                new ModuleLibrary("React Native Bridge", "App hybride optionnelle.", "https://github.com/facebook/react-native")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "SEC",
            Title = "🔐 Sécurité adaptative et biométrique",
            Objective = "Authentification par voix ou comportement, verrouillage intelligent.",
            Impact = "Sécurise l'autonomie locale d'Eterna.",
            Priority = "Critique",
            Icon = "🔐",
            Libraries = new[]
            {
                new ModuleLibrary("SpeechBrain Speaker Verification", "Authentification vocale.", "https://github.com/speechbrain/speechbrain"),
                new ModuleLibrary("FaceNet", "Reconnaissance visage pour login.", "https://github.com/davidsandberg/facenet"),
                new ModuleLibrary("PyOTP", "Double authentification locale.", "https://github.com/pyauth/pyotp"),
                new ModuleLibrary("Cryptography", "Chiffrement de fichiers sensibles.", "https://github.com/pyca/cryptography"),
                new ModuleLibrary("Watchdog", "Détection d'activité suspecte.", "https://github.com/gorakhargosh/watchdog")
            }
        });

        ModuleCategories.Add(new ModuleCategory
        {
            Identifier = "AUTO2",
            Title = "🤖 Autonomie totale (planification + veille + création)",
            Objective = "Permettre à Eterna de travailler seule : veille concurrentielle, création, correction, upload.",
            Impact = "Boucle autonome complète de production.",
            Priority = "Critique",
            Icon = "🤖",
            Libraries = new[]
            {
                new ModuleLibrary("OpenDevin", "Agents d'auto-développement.", "https://github.com/OpenDevin/OpenDevin"),
                new ModuleLibrary("TaskWeaver", "Orchestration et planification IA.", "https://github.com/microsoft/TaskWeaver"),
                new ModuleLibrary("LangGraph", "Raisonnement par graphes d'agents.", "https://github.com/langchain-ai/langgraph"),
                new ModuleLibrary("APScheduler", "Planification locale des tâches.", "https://github.com/agronholm/apscheduler"),
                new ModuleLibrary("AlphaCode", "Référence IA auto-codage.", "https://github.com/deepmind/code_contests")
            }
        });
    }

    private void SeedOperationalData()
    {
        BackupVault.Clear();
        BackupVault.Add(new BackupRecord
        {
            Id = "AUTO_PATCH_20240605_221500",
            Timestamp = DateTime.Today.AddDays(-2).AddHours(22).AddMinutes(15),
            Scope = "Core + UI",
            Notes = "Backup complet avant refonte autonomie.",
            IsEncrypted = true
        });
        BackupVault.Add(new BackupRecord
        {
            Id = "AUTO_PATCH_20240606_104200",
            Timestamp = DateTime.Today.AddDays(-1).AddHours(10).AddMinutes(42),
            Scope = "Sandbox + modèles émotionnels",
            Notes = "Snapshots émotionnels synchronisés.",
            IsEncrypted = true
        });

        ChangeQueue.Clear();
        ChangeQueue.Add(new ChangeRequest
        {
            Id = "CR-221",
            Title = "Refonte pipeline backup pour fichiers volumineux",
            RiskLevel = "Élevé",
            RequiresApproval = true,
            CreatedAt = DateTime.Today.AddDays(-1).AddHours(9)
        });
        ChangeQueue.Add(new ChangeRequest
        {
            Id = "CR-222",
            Title = "Optimisation UI cycle d'auto-apprentissage",
            RiskLevel = "Faible",
            RequiresApproval = false,
            CreatedAt = DateTime.Today.AddHours(-5)
        });

        Watchers.Clear();
        Watchers.Add(new WatcherItem { Path = "sandbox/scripts", Purpose = "Validation des scripts générés", Mode = "Analyse statique + tests" });
        Watchers.Add(new WatcherItem { Path = "models/emotion", Purpose = "Mise à jour des embeddings émotionnels", Mode = "Diff" });
        Watchers.Add(new WatcherItem { Path = "configs/policies", Purpose = "Changements de sécurité", Mode = "Audit" });

        AutonomyLogs.Clear();
        AutonomyLogs.Add(new AutonomyLogEntry
        {
            Id = "AUTO_PATCH_20240606_110501",
            Timestamp = DateTime.Today.AddDays(-1).AddHours(11).AddMinutes(5),
            Message = "Validation manuelle requise pour la mise à jour sécurité biométrique.",
            Status = "En attente"
        });
        AutonomyLogs.Add(new AutonomyLogEntry
        {
            Id = "AUTO_PATCH_20240607_083212",
            Timestamp = DateTime.Today.AddHours(-3).AddMinutes(-18),
            Message = "Tests sandbox complétés pour la synchronisation iOS.",
            Status = "Succès"
        });

        EmotionProfiles.Clear();
        EmotionProfiles.Add(new EmotionProfile
        {
            Name = "Serenity Boost",
            Signal = "Voix stable, rythme cardiaque normal",
            RecommendedAction = "Prioriser la planification de tâches longues et stratégiques."
        });
        EmotionProfiles.Add(new EmotionProfile
        {
            Name = "Focus Surge",
            Signal = "Ton ferme, pulsations accélérées",
            RecommendedAction = "Lancer l'analyse concurrentielle et les tests de performance."
        });
        EmotionProfiles.Add(new EmotionProfile
        {
            Name = "Empathy Sync",
            Signal = "Expressions faciales positives détectées",
            RecommendedAction = "Proposer des améliorations UI/UX et du contenu créatif."
        });
    }

    private void CreateBackup()
    {
        var now = DateTime.Now;
        var backup = new BackupRecord
        {
            Id = $"AUTO_PATCH_{now:yyyyMMdd_HHmmss}",
            Timestamp = now,
            Scope = "Full Stack Local IA",
            Notes = "Snapshot généré depuis le cockpit autonomie.",
            IsEncrypted = true
        };

        BackupVault.Insert(0, backup);
        StatusBanner = "Backup complet créé et chiffré.";
        AutonomyLogs.Insert(0, new AutonomyLogEntry
        {
            Id = backup.Id,
            Timestamp = now,
            Message = "Backup automatique déclenché manuellement depuis l'interface.",
            Status = "Succès"
        });
    }

    private void UpdateChangeStatus(ChangeRequest? change, string newStatus)
    {
        if (change is null)
        {
            StatusBanner = "Impossible de mettre à jour la demande : sélection invalide.";
            return;
        }

        change.Status = newStatus;
        StatusBanner = $"{change.Id} → {newStatus}.";
        AutonomyLogs.Insert(0, new AutonomyLogEntry
        {
            Id = change.Id,
            Timestamp = DateTime.Now,
            Message = $"La demande '{change.Title}' est passée à l'état {newStatus}.",
            Status = newStatus
        });
        OnPropertyChanged(nameof(ChangeQueue));
    }
}
