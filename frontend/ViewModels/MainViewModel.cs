using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Threading;
using Eterna.Desktop.Services;

namespace Eterna.Desktop;

public sealed class MainViewModel : INotifyPropertyChanged, IDisposable
{
    private readonly NamedPipeClient _pipeClient;
    private readonly DispatcherTimer _timer;
    private readonly EventHandler _tickHandler;
    private readonly Random _random = new();

    public CoreStatusViewModel CoreStatus { get; } = new();
    public ObservableCollection<ModuleStatusViewModel> ModuleStatuses { get; } = new();

    public MainViewModel()
    {
        _pipeClient = new NamedPipeClient("eterna_core_pipe");
        _timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(4) };
        _tickHandler = async (_, _) => await RefreshAsync();
        _timer.Tick += _tickHandler;
        _timer.Start();
        _ = RefreshAsync();
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    private async Task RefreshAsync()
    {
        try
        {
            using var doc = await _pipeClient.RequestAsync<JsonDocument>("status");
            if (doc is null)
            {
                ApplySimulation();
                return;
            }

            var root = doc.RootElement;
            if (root.TryGetProperty("modules", out var modules))
            {
                ModuleStatuses.Clear();
                foreach (var module in modules.EnumerateObject())
                {
                    string state = module.Value.TryGetProperty("error", out var error)
                        ? $"Error: {error.GetString()}"
                        : "Online";
                    ModuleStatuses.Add(new ModuleStatusViewModel(module.Name, state));
                }
            }

            if (root.TryGetProperty("telemetry", out var telemetry))
            {
                CoreStatus.CpuUsage = telemetry.GetProperty("cpu").GetDouble();
                CoreStatus.GpuUsage = telemetry.GetProperty("gpu").GetDouble();
            }

            if (root.TryGetProperty("emotion", out var emotion))
            {
                CoreStatus.EmotionLabel = emotion.GetProperty("label").GetString() ?? "Neutral";
                CoreStatus.EmotionConfidence = emotion.GetProperty("confidence").GetDouble();
            }
        }
        catch
        {
            ApplySimulation();
        }
    }

    private void ApplySimulation()
    {
        CoreStatus.CpuUsage = 35 + _random.NextDouble() * 40;
        CoreStatus.GpuUsage = 20 + _random.NextDouble() * 55;
        CoreStatus.EmotionLabel = "Calm Focus";
        CoreStatus.EmotionConfidence = 0.82;
        if (ModuleStatuses.Count == 0)
        {
            ModuleStatuses.Add(new ModuleStatusViewModel("network_manager", "Simulated"));
            ModuleStatuses.Add(new ModuleStatusViewModel("memory_manager", "Simulated"));
            ModuleStatuses.Add(new ModuleStatusViewModel("llama_service", "Simulated"));
        }
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    public void Dispose()
    {
        _timer.Stop();
        _timer.Tick -= _tickHandler;
        _pipeClient.Dispose();
    }
}

public sealed class CoreStatusViewModel : INotifyPropertyChanged
{
    private double _cpuUsage;
    private double _gpuUsage;
    private string _emotionLabel = "Neutral";
    private double _emotionConfidence = 0.5;

    public double CpuUsage
    {
        get => _cpuUsage;
        set
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
        set
        {
            if (Math.Abs(_gpuUsage - value) > 0.01)
            {
                _gpuUsage = value;
                OnPropertyChanged();
            }
        }
    }

    public string EmotionLabel
    {
        get => _emotionLabel;
        set
        {
            if (_emotionLabel != value)
            {
                _emotionLabel = value ?? "Neutral";
                OnPropertyChanged();
            }
        }
    }

    public double EmotionConfidence
    {
        get => _emotionConfidence;
        set
        {
            if (Math.Abs(_emotionConfidence - value) > 0.01)
            {
                _emotionConfidence = value;
                OnPropertyChanged();
            }
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

public sealed class ModuleStatusViewModel
{
    public string Name { get; }
    public string State { get; }
    public Brush StatusBrush { get; }

    public ModuleStatusViewModel(string name, string state)
    {
        Name = name;
        State = state;
        StatusBrush = state.StartsWith("Error", StringComparison.OrdinalIgnoreCase)
            ? Brushes.OrangeRed
            : Brushes.LimeGreen;
    }
}
