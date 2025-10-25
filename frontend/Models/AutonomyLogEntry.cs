using System;

namespace Eterna.Desktop.Models;

public class AutonomyLogEntry
{
    public string Id { get; init; } = string.Empty;
    public DateTime Timestamp { get; init; }
    public string Message { get; init; } = string.Empty;
    public string Status { get; init; } = string.Empty;
}
