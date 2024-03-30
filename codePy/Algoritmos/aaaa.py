import pandas as pd

# Cargar el archivo XLSX
archivo_xlsx = './csv/LIST WORDS FROM Concreteness ratings for 40 thousand generally known English word lemmas.xlsx'  # Reemplaza 'ruta/a/tu/archivo.xlsx' con la ubicación real de tu archivo

# Leer el archivo XLSX
datos_xlsx = pd.read_excel(archivo_xlsx)

# Guardar los datos en un archivo CSV
archivo_csv = 'palabras_abstractas.csv'  # Nombre del archivo CSV de salida
datos_xlsx.to_csv(archivo_csv, index=False, header=False)  # Guardar sin índices ni encabezados

print("El archivo XLSX se ha convertido exitosamente a CSV:", archivo_csv)
