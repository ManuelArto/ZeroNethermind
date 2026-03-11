"""
Grafico 2.1 — Radar Chart: Confronto Footprint Hardware
Confronto normalizzato di CPU, RAM, I/O Read, Bandwidth
tra Nethermind Standard (media el-1/el-2) e ZeroNethermind (el-3).
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

def mean_vals(data):
    return statistics.mean([v for _, v in data])

# --- Caricamento e calcolo medie ---
# CPU (percentuale)
cpu_std = (mean_vals(load_csv('el-1-standard_cpu.csv')) + mean_vals(load_csv('el-2-standard_cpu.csv'))) / 2
cpu_zk  = mean_vals(load_csv('el-3-zeronethermind_cpu.csv'))

# RAM (bytes → MB)
ram_std = (mean_vals(load_csv('el-1-standard_ram.csv')) + mean_vals(load_csv('el-2-standard_ram.csv'))) / 2 / 1e6
ram_zk  = mean_vals(load_csv('el-3-zeronethermind_ram.csv')) / 1e6

# IO Read (bytes/s → KB/s)
io_std = (mean_vals(load_csv('el-1-standard_io_read.csv')) + mean_vals(load_csv('el-2-standard_io_read.csv'))) / 2 / 1e3
io_zk  = mean_vals(load_csv('el-3-zeronethermind_io_read.csv')) / 1e3

# Net RX (bytes/s → KB/s)
bw_std = (mean_vals(load_csv('el-1-standard_net_rx.csv')) + mean_vals(load_csv('el-2-standard_net_rx.csv'))) / 2 / 1e3
bw_zk  = mean_vals(load_csv('el-3-zeronethermind_net_rx.csv')) / 1e3

# --- Valori assoluti per le etichette ---
categories = ['CPU (%)', 'RAM (MB)', 'I/O Read (KB/s)', 'Bandwidth RX (KB/s)']
values_std_abs = [cpu_std, ram_std, io_std, bw_std]
values_zk_abs  = [cpu_zk, ram_zk, io_zk, bw_zk]

# --- Normalizzazione (max di ciascun asse = 1) ---
maxvals = [max(s, z) for s, z in zip(values_std_abs, values_zk_abs)]
values_std_norm = [s / m if m > 0 else 0 for s, m in zip(values_std_abs, maxvals)]
values_zk_norm  = [z / m if m > 0 else 0 for z, m in zip(values_zk_abs, maxvals)]

# --- Radar Chart ---
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

# Chiudi il poligono
values_std_norm += values_std_norm[:1]
values_zk_norm  += values_zk_norm[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Standard
ax.plot(angles, values_std_norm, 'o-', linewidth=2, color='#d62728', label='Nethermind Standard', markersize=6)
ax.fill(angles, values_std_norm, alpha=0.15, color='#d62728')

# ZeroNethermind
ax.plot(angles, values_zk_norm, 'o-', linewidth=2, color='#2ca02c', label='ZeroNethermind', markersize=6)
ax.fill(angles, values_zk_norm, alpha=0.15, color='#2ca02c')

# --- Etichette con valori assoluti ---
ax.set_xticks(angles[:-1])
label_texts = []
for i, cat in enumerate(categories):
    label_texts.append(f'{cat}\nStd: {values_std_abs[i]:.1f}  |  ZK: {values_zk_abs[i]:.1f}')
ax.set_xticklabels(label_texts, fontsize=9)

ax.set_yticklabels([])  # Nascondi i valori radiali (normalizzati, non significativi)
ax.set_ylim(0, 1.15)

ax.set_title('Confronto Footprint Hardware — Demo 2', fontsize=15, pad=25)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), 'demo2_graph3_radar.pdf'), format='pdf', dpi=500)
plt.savefig(os.path.join(os.path.dirname(__file__), 'demo2_graph3_radar.png'), format='png', dpi=300)
plt.show()
print("Grafico 2.1 (Radar) salvato.")
