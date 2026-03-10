#!/bin/bash

# 1. Inserisci qui l'orario di inizio e fine del tuo test in formato UTC
# Puoi ricavare questi orari dai log del terminale di quando hai lanciato la demo
START_TIME="2026-03-10T15:40:00.000Z"
END_TIME="2026-03-10T15:41:00.000Z"

# 2. Frequenza di campionamento (1 punto dati ogni 15 secondi)
STEP="15s"
PROMETHEUS_URL="http://localhost:9090/api/v1/query_range"

# 3. Mappatura dei nomi dei file CSV e delle relative query PromQL
declare -A QUERIES=(
    ["zeronethermind_ram"]="container_memory_usage_bytes{name='zeronethermind_node'}"
    ["zeronethermind_cpu"]="rate(container_cpu_usage_seconds_total{name='zeronethermind_node'}[1m]) * 100"
    ["zeronethermind_net_rx"]="rate(container_network_receive_bytes_total{name='zeronethermind_node'}[1m])"
    ["zeronethermind_io_read"]="rate(container_fs_reads_bytes_total{name='zeronethermind_node'}[1m])"
)

# 4. Esecuzione del ciclo per esportare i dati
for KEY in "${!QUERIES[@]}"; do
    echo "Estrazione della metrica: $KEY..."
    
    # Esegue la chiamata HTTP GET a Prometheus e formatta l'array JSON in CSV
    curl -s -G --data-urlencode "query=${QUERIES[$KEY]}" \
              --data-urlencode "start=$START_TIME" \
              --data-urlencode "end=$END_TIME" \
              --data-urlencode "step=$STEP" \
              "$PROMETHEUS_URL" | \
    jq -r '.data.result[0].values[]? | @csv' > "test-1/${KEY}.csv"
    
done

echo "Tutti i file CSV sono stati generati con successo!"