using System.Text.Json.Serialization;

namespace ZeroProver.Models;

public class ProofMetadata
{
    [JsonPropertyName("proof_id")]
    public long ProofId { get; set; }

    [JsonPropertyName("block_number")]
    public long BlockNumber { get; set; }

    [JsonPropertyName("proof_status")]
    public string Status { get; set; } = "proved";

    [JsonPropertyName("cluster_id")]
    public string ClusterId { get; set; } = "mock-cluster";

    [JsonPropertyName("cluster_version")]
    public Cluster Cluster { get; set; } = new();
}

public class ProofResponse
{
    [JsonPropertyName("rows")]
    public List<ProofMetadata> Rows { get; set; } = [];
}

public class Cluster
{
    [JsonPropertyName("cluster_id")]
    public string ClusterId { get; set; } = "mock-cluster";

    [JsonPropertyName("zkvm_version")]
    public ZkvmVersion ZkvmVersion { get; set; } = new();
}

public class ZkvmVersion
{
    [JsonPropertyName("zkvm")]
    public ZkVm ZkVm { get; set; } = new();
}

public class ZkVm
{
    [JsonPropertyName("slug")]
    public string Type { get; set; } = "risc0";
}

public class ClusterVerifier
{
    [JsonPropertyName("cluster_id")]
    public string Id { get; set; } = string.Empty;

    [JsonPropertyName("zkvm")]
    public string ZkType { get; set; } = string.Empty;

    [JsonPropertyName("vk_path")]
    public string VkPath { get; set; } = string.Empty;

    [JsonPropertyName("vk_binary")]
    public string VkBinary { get; set; } = string.Empty;
}
