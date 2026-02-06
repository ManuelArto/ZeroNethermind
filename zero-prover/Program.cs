using System.Reflection;
using ZeroProver.Models;

var builder = WebApplication.CreateBuilder(args);

// Configure to listen on all interfaces
builder.WebHost.UseUrls("http://0.0.0.0:5000");

var app = builder.Build();

// Load embedded proof binary once at startup
var assembly = Assembly.GetExecutingAssembly();
var proofBytes = LoadEmbeddedResource(assembly, "ZeroProver.Resources.matter-labs_cb06e41d-6666-4a7c-be76-ac626fb19313_7576570.bin");

Console.WriteLine($"[ZeroProver] Loaded proof binary: {proofBytes.Length} bytes");
Console.WriteLine("[ZeroProver] Starting mock prover API on http://0.0.0.0:5000");

// GET /api/v0/verification-keys/active
// Returns empty list (no VK needed for this demo)
app.MapGet("/api/v0/verification-keys/active", () =>
{
    Console.WriteLine("[ZeroProver] GET /api/v0/verification-keys/active -> []");
    return Results.Json(new List<ClusterVerifier>());
});

// GET /api/verification-keys/download/{proofId}
// Returns 404 (no VK needed)
app.MapGet("/api/verification-keys/download/{proofId}", (long proofId) =>
{
    Console.WriteLine($"[ZeroProver] GET /api/verification-keys/download/{proofId} -> 404");
    return Results.NotFound();
});

// GET /api/blocks/{blockId}/proofs
// Returns hardcoded proof metadata for any block
app.MapGet("/api/blocks/{blockId}/proofs", (long blockId, int? page_size) =>
{
    Console.WriteLine($"[ZeroProver] GET /api/blocks/{blockId}/proofs -> returning mock proof");
    
    var response = new ProofResponse
    {
        Rows =
        [
            new ProofMetadata
            {
                ProofId = 1,
                BlockNumber = blockId,
                Status = "proved",
                ClusterId = "mock-cluster",
                Cluster = new Cluster
                {
                    ClusterId = "mock-cluster",
                    ZkvmVersion = new ZkvmVersion
                    {
                        ZkVm = new ZkVm { Type = "airbender" }
                    }
                }
            }
        ]
    };
    
    return Results.Json(response);
});

// GET /api/proofs/download/{proofId}
// Returns the hardcoded proof binary
app.MapGet("/api/proofs/download/{proofId}", (long proofId) =>
{
    Console.WriteLine($"[ZeroProver] GET /api/proofs/download/{proofId} -> returning {proofBytes.Length} bytes");
    return Results.File(proofBytes, "application/octet-stream", "proof.bin");
});

// Health check endpoint
app.MapGet("/health", () => Results.Ok("healthy"));

app.Run();

static byte[] LoadEmbeddedResource(Assembly assembly, string resourceName)
{
    using var stream = assembly.GetManifestResourceStream(resourceName);
    if (stream == null)
    {
        throw new InvalidOperationException($"Embedded resource '{resourceName}' not found. Available: {string.Join(", ", assembly.GetManifestResourceNames())}");
    }
    
    using var ms = new MemoryStream();
    stream.CopyTo(ms);
    return ms.ToArray();
}
