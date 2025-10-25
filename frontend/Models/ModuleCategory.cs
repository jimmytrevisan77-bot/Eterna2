using System.Collections.Generic;

namespace Eterna.Desktop.Models;

public class ModuleCategory
{
    public string Identifier { get; init; } = string.Empty;
    public string Title { get; init; } = string.Empty;
    public string Objective { get; init; } = string.Empty;
    public string Icon { get; init; } = string.Empty;
    public IReadOnlyList<ModuleLibrary> Libraries { get; init; } = new List<ModuleLibrary>();
    public string Impact { get; init; } = string.Empty;
    public string Priority { get; init; } = string.Empty;
}
