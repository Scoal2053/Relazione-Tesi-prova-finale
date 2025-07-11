import pandas as pd
import os

# Carica il file originale
file_path = r'/mnt/c/Users/hp/Desktop/Provider AI/202209-202311_provider_periods.csv'
df = pd.read_csv(file_path)

# Assicurati che le date siano in formato datetime
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

# Crea una cartella di output
output_folder = '/mnt/c/Users/hp/Desktop/Provider AI/split_by_month'
os.makedirs(output_folder, exist_ok=True)

# Lista dove salviamo le righe splittate
rows = []

for _, row in df.iterrows():
    start = row['start_date']
    end = row['end_date']

    # Cicla su tutti i mesi attraversati dal periodo
    current = start
    while current <= end:
        month_start = current.replace(day=1)
        next_month_start = (month_start + pd.DateOffset(months=1))

        period_end = min(end, next_month_start - pd.Timedelta(days=1))

        rows.append({
            **row.drop(['start_date', 'end_date']).to_dict(),  # Altre colonne
            'start_date': current,
            'end_date': period_end
        })

        # Avanza al mese successivo
        current = next_month_start

# Crea DataFrame finale splittato
split_df = pd.DataFrame(rows)

# Salva un file CSV per ogni mese
for year_month, group in split_df.groupby(split_df['start_date'].dt.to_period('M')):
    year_month_str = year_month.strftime('%Y-%m')
    output_file = os.path.join(output_folder, f'{year_month_str}.csv')
    group.to_csv(output_file, index=False)

print(f'File suddivisi per mese salvati in: {output_folder}')