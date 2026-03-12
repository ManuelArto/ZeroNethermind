"""
Grafico 1.1 — Velocità di Verifica vs Esecuzione (Grouped Bar Chart)
Confronto diretto dei tempi medi di validazione nelle fasi Baseline e Loaded
per i 3 nodi: el-1 (Standard), el-2 (Standard), el-3 (ZeroNethermind).
"""
import csv
import statistics
import matplotlib.pyplot as plt
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_csv(filename):
    rows = []
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath) as fp:
        for r in csv.reader(fp):
            if len(r) == 2:
                rows.append((int(r[0]), float(r[1].strip('"'))))
    return rows

# --- Caricamento dati ---
time_el1 = load_csv('el-1-standard_time.csv')
time_el2 = load_csv('el-2-standard_time.csv')
time_el3 = load_csv('el-3-zeronethermind_time.csv')

# --- Fasi temporali ---
T_BASELINE_END = 1773248400  # 18:00 — prima dell'aumento del throughput

def split_phases(data):
    baseline = [v for t, v in data if t < T_BASELINE_END]
    loaded   = [v for t, v in data if t >= T_BASELINE_END]
    return baseline, loaded

b1, l1 = split_phases(time_el1)
b2, l2 = split_phases(time_el2)
b3, l3 = split_phases(time_el3)

# --- Statistiche ---
means_baseline = [statistics.mean(b1), statistics.mean(b2), statistics.mean(b3)]
means_loaded   = [statistics.mean(l1), statistics.mean(l2), statistics.mean(l3)]

# Deviazione standard per le barre di errore
std_baseline = [statistics.stdev(b1), statistics.stdev(b2), statistics.stdev(b3)]
std_loaded   = [statistics.stdev(l1), statistics.stdev(l2), statistics.stdev(l3)]

# --- Configurazione del grafico ---
labels = ['el-1\n(Standard)', 'el-2\n(Standard)', 'el-3\n(ZeroNethermind)']
x = np.arange(len(labels))
width = 0.32

fig, ax = plt.subplots(figsize=(10, 6))

# Colori coerenti con il tema Demo 1
color_baseline = '#1f77b4'   # Blu — basso carico
color_loaded   = '#d62728'   # Rosso — carico elevato

bars1 = ax.bar(x - width/2, means_baseline, width, label='Baseline (basso carico)',
               color=color_baseline, alpha=0.85, yerr=std_baseline, capsize=5, edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + width/2, means_loaded, width, label='Sotto carico (spamoor)',
               color=color_loaded, alpha=0.85, yerr=std_loaded, capsize=5, edgecolor='white', linewidth=0.5)

# --- Annotazioni valori sopra le barre ---
for bar in bars1:
    h = bar.get_height()
    ax.annotate(f'{h:.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
                xytext=(0, 8), textcoords='offset points', ha='center', va='bottom', fontsize=10, fontweight='bold')
for bar in bars2:
    h = bar.get_height()
    ax.annotate(f'{h:.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
                xytext=(0, 8), textcoords='offset points', ha='center', va='bottom', fontsize=10, fontweight='bold')

# --- Formattazione ---
ax.set_ylabel('Tempo Medio di Validazione (ms)', fontsize=12)
ax.set_title('Velocità di Verifica vs Esecuzione — Demo 2', fontsize=16)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.legend(fontsize=11)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_ylim(0, max(means_loaded) * 1.4)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), 'demo2_graph1_verification_speed.png'), format='png', dpi=300)
plt.show()
print("Grafico 1.1 salvato.")
