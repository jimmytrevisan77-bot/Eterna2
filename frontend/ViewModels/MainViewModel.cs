using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.IO.Pipes;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows.Threading;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Eterna.Desktop.Commands;
using Eterna.Desktop.Models;

namespace Eterna.Desktop.ViewModels;

public class MainViewModel : INotifyPropertyChanged
{
    private ModuleCategory? _selectedModule;
    private string _statusBanner = "Prêt pour la prochaine itération";
    private double _cpuUsage;
    private double _gpuUsage;
    private string _emotionState = "Neutre";
    private double _emotionConfidence = 0.72;
    private ImageSource? _logoImage;
    private bool _isLogoAvailable;
    private readonly DispatcherTimer _telemetryTimer;
    private readonly Random _random = new();
    private const string PipeName = "eterna_ipc";

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
        LoadLogo();

        CreateBackupCommand = new RelayCommand(_ => CreateBackup());
        ApproveChangeCommand = new RelayCommand(param => UpdateChangeStatus(param as ChangeRequest, "Validé"));
        RejectChangeCommand = new RelayCommand(param => UpdateChangeStatus(param as ChangeRequest, "Rejeté"));
        ClearBannerCommand = new RelayCommand(() => StatusBanner = "");

        SelectedModule = ModuleCategories.FirstOrDefault();

        _telemetryTimer = new DispatcherTimer
        {
            Interval = TimeSpan.FromSeconds(3)
        };
        _telemetryTimer.Tick += async (_, _) => await RefreshTelemetryAsync();
        _ = RefreshTelemetryAsync();
        _telemetryTimer.Start();
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

    public double CpuUsage
    {
        get => _cpuUsage;
        private set
        {
            if (Math.Abs(_cpuUsage - value) > 0.01)
            {
                _cpuUsage = value;
                OnPropertyChanged();
            }
        }
    }

    public double GpuUsage
    {
        get => _gpuUsage;
        private set
        {
            if (Math.Abs(_gpuUsage - value) > 0.01)
            {
                _gpuUsage = value;
                OnPropertyChanged();
            }
        }
    }

    public string EmotionState
    {
        get => _emotionState;
        private set
        {
            if (_emotionState != value)
            {
                _emotionState = value;
                OnPropertyChanged();
            }
        }
    }

    public double EmotionConfidence
    {
        get => _emotionConfidence;
        private set
        {
            if (Math.Abs(_emotionConfidence - value) > 0.001)
            {
                _emotionConfidence = value;
                OnPropertyChanged();
            }
        }
    }

    public ImageSource? LogoImage
    {
        get => _logoImage;
        private set
        {
            if (!Equals(_logoImage, value))
            {
                _logoImage = value;
                OnPropertyChanged();
            }
        }
    }

    public bool IsLogoAvailable
    {
        get => _isLogoAvailable;
        private set
        {
            if (_isLogoAvailable != value)
            {
                _isLogoAvailable = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(LogoStatusMessage));
            }
        }
    }

    public string LogoStatusMessage => IsLogoAvailable
        ? "Logo Eternadream chargé."
        : "Déposez le fichier officiel 'logo_or_rouge_no_text_transparent_300dpi.png' dans assets/logo.png.";

    public event PropertyChangedEventHandler? PropertyChanged;

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));

    private async Task RefreshTelemetryAsync()
    {
        var updated = await TryUpdateTelemetryFromBackendAsync();
        if (!updated)
        {
            ApplyFallbackTelemetry();
        }
    }

    private void ApplyFallbackTelemetry()
    {
        CpuUsage = 35 + _random.NextDouble() * 45;
        GpuUsage = 25 + _random.NextDouble() * 55;
        var emotions = new[] { "Neutre", "Enthousiaste", "Concentré", "Inspiré" };
        EmotionState = emotions[_random.Next(emotions.Length)];
        EmotionConfidence = 0.55 + _random.NextDouble() * 0.4;
        if (string.IsNullOrWhiteSpace(StatusBanner))
        {
            StatusBanner = "Mode simulation active";
        }
    }

    private void LoadLogo()
    {
        foreach (var path in GetCandidateLogoPaths())
        {
            if (!File.Exists(path))
            {
                continue;
            }

            try
            {
                using var stream = File.OpenRead(path);
                var image = new BitmapImage();
                image.BeginInit();
                image.CacheOption = BitmapCacheOption.OnLoad;
                image.StreamSource = stream;
                image.EndInit();
                image.Freeze();
                LogoImage = image;
                IsLogoAvailable = true;
                return;
            }
            catch
            {
                // Continue to next candidate if the file is invalid.
            }
        }

        LogoImage = null;
        IsLogoAvailable = false;
    }

    private static string[] GetCandidateLogoPaths()
    {
        var baseDir = AppDomain.CurrentDomain.BaseDirectory;
        var candidates = new[]
        {
            Path.Combine(baseDir, "Assets", "logo.png"),
            Path.Combine(baseDir, "assets", "logo.png"),
            Path.Combine(Directory.GetCurrentDirectory(), "assets", "logo.png"),
            Path.Combine(Directory.GetCurrentDirectory(), "frontend", "Assets", "logo.png")
        };

        return candidates
            .Select(Path.GetFullPath)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToArray();
    }

    private async Task<bool> TryUpdateTelemetryFromBackendAsync()
    {
        try
        {
            using var pipe = new NamedPipeClientStream(".", PipeName, PipeDirection.InOut, PipeOptions.Asynchronous);
            await pipe.ConnectAsync(200).ConfigureAwait(true);
            pipe.ReadMode = PipeTransmissionMode.Message;

            var payload = Encoding.UTF8.GetBytes("{\"command\":\"heartbeat\"}");
            await pipe.WriteAsync(payload).ConfigureAwait(true);
            await pipe.FlushAsync().ConfigureAwait(true);

            using var responseBuffer = new MemoryStream();
            var buffer = new byte[2048];
            do
            {
                var read = await pipe.ReadAsync(buffer, 0, buffer.Length).ConfigureAwait(true);
                if (read <= 0)
                {
                    break;
                }
                responseBuffer.Write(buffer, 0, read);
                if (pipe.ReadMode == PipeTransmissionMode.Message && pipe.IsMessageComplete)
                {
                    break;
                }
                if (read < buffer.Length)
                {
                    break;
                }
            }
            while (true);

            if (responseBuffer.Length == 0)
            {
                StatusBanner = "Backend local détecté sans réponse";
                return false;
            }

            var json = Encoding.UTF8.GetString(responseBuffer.ToArray());
            using var document = JsonDocument.Parse(json);
            ApplyBackendSnapshot(document.RootElement);
            StatusBanner = "Connecté au backend local";
            return true;
        }
        catch (TimeoutException)
        {
            StatusBanner = "Backend en attente";
        }
        catch (IOException)
        {
            StatusBanner = "Canal IPC indisponible";
        }
        catch (UnauthorizedAccessException)
        {
            StatusBanner = "Accès IPC refusé";
        }
        catch (JsonException)
        {
            StatusBanner = "Réponse backend invalide";
        }

        return false;
    }

    private void ApplyBackendSnapshot(JsonElement root)
    {
        if (root.ValueKind != JsonValueKind.Object)
        {
            return;
        }

        if (root.TryGetProperty("system_control", out var systemControl))
        {
            ApplySystemSnapshot(systemControl);
        }
        else if (root.TryGetProperty("core_manager", out var core) && core.ValueKind == JsonValueKind.Object)
        {
            if (core.TryGetProperty("system", out var systemNode))
            {
                ApplySystemSnapshot(systemNode);
            }
        }

        if (root.TryGetProperty("emotion_state", out var emotionNode) && emotionNode.ValueKind == JsonValueKind.String)
        {
            EmotionState = emotionNode.GetString() ?? EmotionState;
        }
        if (root.TryGetProperty("emotion_confidence", out var confidenceNode) && confidenceNode.TryGetDouble(out var conf))
        {
            EmotionConfidence = conf;
        }
    }

    private void ApplySystemSnapshot(JsonElement element)
    {
        if (element.ValueKind != JsonValueKind.Object)
        {
            return;
        }

        if (element.TryGetProperty("cpu_percent", out var cpu) && cpu.TryGetDouble(out var cpuValue))
        {
            CpuUsage = cpuValue;
        }
        if (element.TryGetProperty("gpu_percent", out var gpu) && gpu.TryGetDouble(out var gpuValue))
        {
            GpuUsage = gpuValue;
        }
    }

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
                new ModuleLibrary("Named Pipes Windows", "Canal local sécurisé.", "https://learn.microsoft.com/dotnet/standard/io/pipe-operations"),
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
