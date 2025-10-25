using System;

namespace Eterna.Desktop.Models;

public class ChangeRequest
{
    public string Id { get; init; } = string.Empty;
    public string Title { get; init; } = string.Empty;
    public string RiskLevel { get; init; } = string.Empty;
    public bool RequiresApproval { get; init; }
    public string Status { get; set; } = "Pending";
    public DateTime CreatedAt { get; init; }
}
