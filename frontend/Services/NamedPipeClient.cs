using System;
using System.IO;
using System.IO.Pipes;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace Eterna.Desktop.Services;

public sealed class NamedPipeClient : IDisposable
{
    private readonly string _pipeName;

    public NamedPipeClient(string pipeName)
    {
        _pipeName = pipeName;
    }

    public async Task<T?> RequestAsync<T>(string message, CancellationToken cancellationToken = default)
    {
        using var client = new NamedPipeClientStream(".", _pipeName, PipeDirection.InOut, PipeOptions.Asynchronous);
        try
        {
            await client.ConnectAsync(150, cancellationToken);
        }
        catch (TimeoutException)
        {
            return default;
        }

        await using var writer = new StreamWriter(client, new UTF8Encoding(false), leaveOpen: true) { AutoFlush = true };
        await writer.WriteLineAsync(message.AsMemory(), cancellationToken);

        using var reader = new StreamReader(client, Encoding.UTF8, leaveOpen: true);
        var response = await reader.ReadLineAsync(cancellationToken);
        if (string.IsNullOrWhiteSpace(response))
        {
            return default;
        }

        return JsonSerializer.Deserialize<T>(response);
    }

    public void Dispose()
    {
    }
}
