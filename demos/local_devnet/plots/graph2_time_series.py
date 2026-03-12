"""
Grafico 1.2 — Impatto dell'Aumento del Carico Transazionale (Time Series con Rette Verticali)
Mostra il validation time nel tempo per i 3 nodi, con 4 rette verticali
che delineano i momenti di aumento del throughput degli spammer.
Evidenzia O(N) vs O(1).
"""
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime
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

def to_dataframe(data, col_name):
    df = pd.DataFrame(data, columns=['Timestamp', col_name])
    df['Time'] = pd.to_datetime(df['Timestamp'], unit='s')
    df.set_index('Time', inplace=True)
    df.drop(columns=['Timestamp'], inplace=True)
    return df

# --- Caricamento dati ---
df_el1 = to_dataframe(load_csv('el-1-standard_time.csv'), 'el1')
df_el2 = to_dataframe(load_csv('el-2-standard_time.csv'), 'el2')
df_el3 = to_dataframe(load_csv('el-3-zeronethermind_time.csv'), 'el3')

# --- Smoothing con rolling average per leggibilità ---
WINDOW = 4  # ~60 secondi (4 campioni x 15s)
df_el1_smooth = df_el1.rolling(window=WINDOW, center=True, min_periods=1).mean()
df_el2_smooth = df_el2.rolling(window=WINDOW, center=True, min_periods=1).mean()
df_el3_smooth = df_el3.rolling(window=WINDOW, center=True, min_periods=1).mean()

# --- Rette verticali (momenti di aumento throughput) ---
# Approssimazioni confermate dall'utente (CET → UTC, -1h)
# Utente: ~18:02, ~18:08, ~18:15, ~18:22 CET
INCREASE_TIMES = [
    datetime(2026, 3, 11, 17, 2, 0),
    datetime(2026, 3, 11, 17, 8, 0),
    datetime(2026, 3, 11, 17, 15, 0),
    datetime(2026, 3, 11, 17, 22, 0),
]

# --- Creazione del grafico ---
fig, ax = plt.subplots(figsize=(14, 7))

# Linee per i 3 nodi
ax.plot(df_el1_smooth.index, df_el1_smooth['el1'], color='#1f77b4', label='el-1 Standard', linewidth=2, alpha=0.85)
ax.plot(df_el2_smooth.index, df_el2_smooth['el2'], color='#d62728', label='el-2 Standard', linewidth=2, alpha=0.85)
ax.plot(df_el3_smooth.index, df_el3_smooth['el3'], color='#2ca02c', label='el-3 ZeroNethermind', linewidth=2.5, alpha=0.95)

# Scatter dei punti raw (trasparenza più bassa per mostrare la distribuzione)
# ax.scatter(df_el1.index, df_el1['el1'], color='#1f77b4', alpha=0.15, s=8, zorder=1)
# ax.scatter(df_el2.index, df_el2['el2'], color='#d62728', alpha=0.15, s=8, zorder=1)
# ax.scatter(df_el3.index, df_el3['el3'], color='#2ca02c', alpha=0.15, s=8, zorder=1)

# Aggiorniamo i limiti Y
ax.set_ylim(0, 1600)

# Rette verticali tratteggiate con etichette
for i, t in enumerate(INCREASE_TIMES):
    ax.axvline(x=t, color='#ff7f0e', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.text(t, 1520, f'↑ #{i+1}', ha='center', va='bottom', fontsize=9, color='#ff7f0e', fontweight='bold')

# --- Annotazione zona ---
ax.axhspan(0, 250, alpha=0.06, color='green')
ax.text(df_el3.index[5], 310, 'Zona O(1) — ZeroNethermind', fontsize=9, color='green', fontstyle='italic', alpha=0.7)

# --- Formattazione ---
ax.set_title("Impatto dell'Aumento del Carico Transazionale (engine_newPayload)", fontsize=16)
ax.set_xlabel('Orario', fontsize=12)
ax.set_ylabel('Tempo di Validazione (ms)', fontsize=12)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.tight_layout()

# --- Salvataggio ---
plt.savefig(os.path.join(os.path.dirname(__file__), 'demo2_graph2_time_series.png'), format='png', dpi=300)
plt.show()
print("Grafico 1.2 salvato.")
