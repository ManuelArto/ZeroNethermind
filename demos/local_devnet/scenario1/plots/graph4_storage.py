"""
Grafico 2.2 — Crescita dello Storage nel Tempo (Time Series)
Confronto dell'accumulo di stato su disco tra nodi Standard e ZeroNethermind.
Dimostra materialmente il paradigma "Zero State": lo storage di ZeroNethermind
non cresce significativamente, risolvendo il problema dello State Bloat.
"""
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
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

# --- Caricamento dati (bytes → MB) ---
df_el1 = to_dataframe([(t, v / 1e6) for t, v in load_csv('el-1-standard_storage.csv')], 'el1')
df_el2 = to_dataframe([(t, v / 1e6) for t, v in load_csv('el-2-standard_storage.csv')], 'el2')
df_el3 = to_dataframe([(t, v / 1e6) for t, v in load_csv('el-3-zeronethermind_storage.csv')], 'el3')

# --- Creazione del grafico ---
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(df_el1.index, df_el1['el1'], color='#1f77b4', label='el-1 Standard', linewidth=2, alpha=0.85)
ax.plot(df_el2.index, df_el2['el2'], color='#d62728', label='el-2 Standard', linewidth=2, alpha=0.85)
ax.plot(df_el3.index, df_el3['el3'], color='#2ca02c', label='el-3 ZeroNethermind', linewidth=2.5, alpha=0.95)

# --- Annotazioni di crescita ---
# el-1 crescita
growth_el1 = df_el1['el1'].iloc[-1] - df_el1['el1'].iloc[0]
growth_el3 = df_el3['el3'].iloc[-1] - df_el3['el3'].iloc[0]

ax.annotate(f'+{growth_el1:.0f} MB', xy=(df_el1.index[-1], df_el1['el1'].iloc[-1]),
            xytext=(10, 10), textcoords='offset points', fontsize=11, fontweight='bold',
            color='#1f77b4', arrowprops=dict(arrowstyle='->', color='#1f77b4', lw=1.5))

ax.annotate(f'+{growth_el3:.1f} MB', xy=(df_el3.index[-1], df_el3['el3'].iloc[-1]),
            xytext=(10, -20), textcoords='offset points', fontsize=11, fontweight='bold',
            color='#2ca02c', arrowprops=dict(arrowstyle='->', color='#2ca02c', lw=1.5))

# --- Zona "Zero State" ---
ax.axhspan(df_el3['el3'].min() - 5, df_el3['el3'].max() + 5, alpha=0.06, color='green')

# --- Formattazione ---
ax.set_title('Crescita dello Storage nel Tempo — Demo 2', fontsize=16)
ax.set_xlabel('Orario', fontsize=12)
ax.set_ylabel('Storage Occupato (MB)', fontsize=12)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.5)

# Y-axis: mostra l'intero range con margine
y_min = min(df_el1['el1'].min(), df_el3['el3'].min()) - 20
y_max = max(df_el1['el1'].max(), df_el2['el2'].max()) + 30
ax.set_ylim(y_min, y_max)

plt.xticks(rotation=45)
plt.tight_layout()

# --- Salvataggio ---
plt.savefig(os.path.join(os.path.dirname(__file__), 'demo2_graph4_storage.pdf'), format='pdf', dpi=500)
plt.savefig(os.path.join(os.path.dirname(__file__), 'demo2_graph4_storage.png'), format='png', dpi=300)
plt.show()
print("Grafico 2.2 (Storage) salvato.")
