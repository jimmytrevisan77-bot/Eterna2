using System;

namespace Eterna.Desktop.Models;

public class BackupRecord
{
    public string Id { get; init; } = string.Empty;
    public DateTime Timestamp { get; init; }
    public string Scope { get; init; } = string.Empty;
    public string Notes { get; init; } = string.Empty;
    public bool IsEncrypted { get; init; }
}
