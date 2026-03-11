#!/usr/bin/env bash
# ============================================================
#  run_scenario.sh — Run a Kurtosis Demo 2 scenario
# ============================================================
#  Usage:
#    ./run_scenario.sh <scenario_number> [gas_limit]
#
#  Examples:
#    ./run_scenario.sh 1               # Scenario 1: Resource Footprint (30M Gas)
#    ./run_scenario.sh 2               # Scenario 2: Sync Time
#    ./run_scenario.sh 3               # Scenario 3: Gas Limit (default 30M)
#    ./run_scenario.sh 3 60000000      # Scenario 3: Gas Limit = 60M
#    ./run_scenario.sh 3 120000000     # Scenario 3: Gas Limit = 120M
#    ./run_scenario.sh 3 250000000     # Scenario 3: Gas Limit = 250M
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KURTOSIS_DIR="$SCRIPT_DIR"
KURTOSIS_BIN="/home/manuel/Downloads/kurtosis-cli_1.15.2_linux_amd64/kurtosis"

SCENARIO="${1:?Usage: $0 <1|2|3> [gas_limit]}"
GAS_LIMIT="${2:-}"

case "$SCENARIO" in
  1)
    ENCLAVE="s1-footprint"
    CONFIG="scenarios/scenario1-footprint.yaml"
    echo "🔬 Running Scenario 1: Resource Footprint (30M Gas)"
    ;;
  2)
    ENCLAVE="s2-synctime"
    CONFIG="scenarios/scenario2-synctime.yaml"
    echo "🕐 Running Scenario 2: Sync Time"
    echo "   After the enclave is ready, wait N minutes, then run:"
    echo "     kurtosis service start $ENCLAVE el-3-nethermind-lighthouse"
    echo "     kurtosis service start $ENCLAVE el-4-zero-nethermind-lighthouse"
    ;;
  3)
    if [[ -n "$GAS_LIMIT" ]]; then
      GAS_M=$((GAS_LIMIT / 1000000))
      ENCLAVE="s3-${GAS_M}m"
    else
      ENCLAVE="s3-30m"
    fi
    CONFIG="scenarios/scenario3-gaslimit.yaml"
    echo "📈 Running Scenario 3: Gas Limit Scaling"
    ;;
  *)
    echo "❌ Invalid scenario: $SCENARIO (expected 1, 2, or 3)"
    exit 1
    ;;
esac

# Destroy previous enclave if it exists
echo "🧹 Cleaning up previous enclave '$ENCLAVE' (if any)..."
kurtosis enclave rm -f "$ENCLAVE" 2>/dev/null || true

# Build/tag the required Docker images
echo "🐳 Ensuring Docker images are available..."

# Check if zero-nethermind:latest exists
if ! docker image inspect zero-nethermind:latest &>/dev/null; then
  echo "⚠️  Image 'zero-nethermind:latest' not found. Build it first:"
  echo "   cd nethermind && docker build -t zero-nethermind:latest -f src/Nethermind/Nethermind.Runner/Dockerfile ."
  exit 1
fi

# Check if zero-prover:local exists
if ! docker image inspect zero-prover:local &>/dev/null; then
  echo "⚠️  Image 'zero-prover:local' not found. Build it first:"
  echo "   cd zero-prover && docker build -t zero-prover:local ."
  exit 1
fi

# Run Kurtosis
echo "🚀 Starting enclave '$ENCLAVE'..."
CMD="$KURTOSIS_BIN run --enclave $ENCLAVE $KURTOSIS_DIR/kurtosis.yml --args-file $KURTOSIS_DIR/$CONFIG"

if [[ "$SCENARIO" == "3" && -n "$GAS_LIMIT" ]]; then
  CMD="$CMD --args '{\"network_params\":{\"genesis_gaslimit\":$GAS_LIMIT}}'"
fi

echo "   Command: $CMD"
eval "$CMD"

echo ""
echo "✅ Enclave '$ENCLAVE' is running!"
echo ""
echo "📊 Useful commands:"
echo "   kurtosis enclave inspect $ENCLAVE           # See all services"
echo "   kurtosis service logs $ENCLAVE <service>    # View logs"
echo "   kurtosis enclave rm -f $ENCLAVE             # Tear down"
