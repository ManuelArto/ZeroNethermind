#!/bin/bash

# ================= IMPOSTAZIONI =================
# Orari di inizio e fine dell'esperimento (UTC)
START_TIME="2026-03-11T14:10:00.000Z"
END_TIME="2026-03-11T14:12:00.000Z"
STEP="15s"


# ================= ESTRAZIONE =================
echo "Inizio estrazione dati Demo 2..."
mkdir -p test-1
cd test-1

# ================= cAdvisor METRICS =================

PROMETHEUS_URL="http://localhost:9090/api/v1/query_range"

# Nomi dei container rilevati da Kurtosis
NODE_STD="el-1-nethermind-lighthouse"
NODE_ZK="el-3-nethermind-lighthouse"

# ================= QUERY PROMQL =================
declare -A QUERIES=(
    # STORAGE (Per il Grafico a Linee)
    ["storage_std"]="container_fs_usage_bytes{name='$NODE_STD'}"
    ["storage_zk"]="container_fs_usage_bytes{name='$NODE_ZK'}"
    
    # RISORSE RADAR CHART (CPU, RAM, IO, BW)
    ["cpu_std"]="rate(container_cpu_usage_seconds_total{name='$NODE_STD'}[1m]) * 100"
    ["cpu_zk"]="rate(container_cpu_usage_seconds_total{name='$NODE_ZK'}[1m]) * 100"
    ["ram_std"]="container_memory_usage_bytes{name='$NODE_STD'}"
    ["ram_zk"]="container_memory_usage_bytes{name='$NODE_ZK'}"
    ["io_std"]="rate(container_fs_reads_bytes_total{name='$NODE_STD'}[1m])"
    ["io_zk"]="rate(container_fs_reads_bytes_total{name='$NODE_ZK'}[1m])"
    ["bw_std"]="rate(container_network_receive_bytes_total{name='$NODE_STD'}[1m])"
    ["bw_zk"]="rate(container_network_receive_bytes_total{name='$NODE_ZK'}[1m])"
)

for KEY in "${!QUERIES[@]}"; do
    TMP_FILE="$(mktemp)"
    curl -s -G --data-urlencode "query=${QUERIES[$KEY]}" \
              --data-urlencode "start=$START_TIME" \
              --data-urlencode "end=$END_TIME" \
              --data-urlencode "step=$STEP" \
              "$PROMETHEUS_URL" | \
    jq -r '.data.result[0].values[]? | @csv' > "$TMP_FILE"

    if [ -s "$TMP_FILE" ]; then
        echo "Estrazione: $KEY"
        mv "$TMP_FILE" "${KEY}.csv"
    else
        rm -f "$TMP_FILE"
    fi
done


# ================= KURTOSIS METRICS =================

# Sostituisci con l'URL di Prometheus fornito da Kurtosis
KURTOSIS_PROMETHEUS_URL="http://127.0.0.1:32806/api/v1/query_range"

# ================= QUERY PROMQL =================
declare -A QUERIES_KURTOSIS=(
    # TEMPI DI ESECUZIONE / VERIFICA (Per il Grafico a Barre O(N) vs O(1))
    ["time_std"]="nethermind_block_processing_time_micros{job='nethermind', instance=~'.*$NODE_STD.*'}"
    ["time_zk"]="nethermind_block_processing_time_micros{job='nethermind', instance=~'.*$NODE_ZK.*'}"
)

for KEY in "${!QUERIES_KURTOSIS[@]}"; do
    TMP_FILE="$(mktemp)"
    curl -s -G --data-urlencode "query=${QUERIES_KURTOSIS[$KEY]}" \
              --data-urlencode "start=$START_TIME" \
              --data-urlencode "end=$END_TIME" \
              --data-urlencode "step=$STEP" \
              "$KURTOSIS_PROMETHEUS_URL" | \
    jq -r '.data.result[0].values[]? | @csv' > "$TMP_FILE"

    if [ -s "$TMP_FILE" ]; then
        echo "Estrazione: $KEY"
        mv "$TMP_FILE" "${KEY}.csv"
    else
        rm -f "$TMP_FILE"
    fi
done