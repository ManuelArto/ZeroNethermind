# ZeroNethermind

ZeroNethermind is an experimental **Stateless Execution Layer** for Ethereum that leverages **Zero-Knowledge Proofs (ZKPs)** to achieve $O(1)$ block validation. By replacing standard EVM re-execution with cryptographic proof verification, it enables high-throughput execution on consumer-grade hardware, solving the "State Bloat" crisis and the Scalability Trilemma.

This project is the practical implementation of the thesis: *"Engineering a Stateless Execution Layer in Ethereum using Zero-Knowledge Proofs"*.

## 🚀 The "Double Zero" Paradigm

ZeroNethermind operates in what we call **Fort Mode**, a highly efficient state for validators that implements two core principles:

1.  **Zero State:** The node does not maintain a local Merkle Patricia Trie (MPT) database. Disk storage is reduced to nearly 0 GB, as state is treated as ephemeral.
2.  **Zero Knowledge:** Standard EVM execution is bypassed. Instead, the node verifies ZK proofs that attest to the correctness of the state transition. This transforms validation time from $O(N_{\text{gas}})$ to $O(1)$, independent of the block's computational complexity.

## 🏗️ Architecture

ZeroNethermind is built as a modular extension of the [Nethermind](https://github.com/NethermindEth/nethermind) client:

*   **Interceptor (C#):** Hooks into the Engine API (`engine_newPayload`), intercepting blocks before they reach the EVM.
*   **Verifier Orchestrator (C#):** Fetches required ZK proofs from a Prover Network (e.g., `ethproofs.org` or a local prover) and manages the validation lifecycle, including a **Majority Voting** mechanism to ensure block integrity across multiple proofs.
*   **FFI Bridge (Rust):** A high-performance bridge using **Zero-Copy Memory** to invoke native ZK verifiers.
*   **Native Verifiers (Rust):** Support for multiple ZK-VMs and proof systems, ensuring future-proof compatibility.

## 🛠️ Supported ZK-VMs

The system supports a wide range of modern ZK-VM architectures:
*   **Zisk** (Polygon Hermez)
*   **OpenVM**
*   **Pico**
*   **SP1-Hypercube** (Succinct)
*   **Airbender** (Matter Labs / zkSync)

## 📂 Project Structure

*   `nethermind/`: Fork of Nethermind with the `ZkValidation` plugin and stateless configuration.
*   `EthProofValidator/`: The core proof validation engine.
    *   `src/`: C# orchestrator and API client.
    *   `native-zk-verifier/`: Rust implementations of the various ZK verifiers.
*   `zero-prover/`: A mock prover API used for local demos and testing.
*   `demos/`: Data and scripts from experimental evaluations:
    *   `syncing_mainnet/`: Results from live Mainnet L1 validation.
    *   `local_devnet/`: Resource footprint analysis ($O(1)$ vs $O(N)$ comparison).
*   `kurtosis/`: Orchestration packages for launching local ZeroNethermind devnets.

## 🚦 Getting Started

### Prerequisites
*   .NET 10 SDK
*   Rust (Nightly toolchain)
*   Docker & Kurtosis (for devnet demos)

### Running the Local Devnet Demo
To launch a local Ethereum network with standard Nethermind nodes and a ZeroNethermind "Fort" node:

```bash
kurtosis run --enclave zero-demo ./kurtosis --args-file kurtosis/kurtosis-config.yaml
```

### Running Resource Footprint Scenarios
To compare ZeroNethermind against standard nodes under heavy load (500M Gas):

```bash
kurtosis run --enclave s1-footprint ./kurtosis \
    --args-file kurtosis/scenarios/scenario1-footprint.yaml
```

## 📊 Performance Insights

*   **Validation Speed:** ZeroNethermind maintains a constant validation time (~120-150ms) even as gas limits increase, while standard nodes scale linearly with load.
*   **Storage:** ZeroNethermind storage growth is typically **< 5%** of a standard node, as it avoids MPT accumulation.
*   **Hardware Footprint:** RAM usage stays stable under 2GB, and Disk I/O is virtually eliminated.

---
**Author:** Manuel Arto
**Thesis Project** - University of Bologna
