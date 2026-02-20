
import pandas as pd
import os

try:
    print("Reading CSV in chunks...")
    unique_types = set()
    sample_g4 = []
    
    for chunk in pd.read_csv("DataBase/archivo_modificado.csv", chunksize=1000):
        unique_types.update(chunk['tipo_gasto'].unique())
        
        g4_rows = chunk[chunk['tipo_gasto'] == 'G4']
        if not g4_rows.empty and len(sample_g4) < 5:
            sample_g4.extend(g4_rows.to_dict('records'))
            
        if len(sample_g4) >= 5 and 'G4' in unique_types:
            break
            
    print("Unique values in tipo_gasto:", unique_types)
    print("\nSample G4 rows:")
    for row in sample_g4[:5]:
        print(row)

except Exception as e:
    print(f"Error: {e}")
