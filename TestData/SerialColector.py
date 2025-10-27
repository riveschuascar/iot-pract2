import serial
import csv
import time
import os # Necesario para la función os.path.exists

# Configuración del puerto serial
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
TIMEOUT = 1

CSV_FILE = "Resultados/datos_serial.csv"

def post_process_csv(filename):
    """
    Lee el archivo CSV, separa los datos de la columna 'data_raw'
    en 'data_raw', 'data_sqr' y 'data_lin', y sobrescribe el archivo.
    """
    print(f"\nIniciando post-procesamiento de '{filename}'...")
    
    if not os.path.exists(filename):
        print(f"Error: El archivo '{filename}' no fue encontrado.")
        return

    # 1. Leer todas las filas existentes
    rows_to_process = []
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            header = next(reader) # Leer y guardar el encabezado
            
            # Verificar que el encabezado es el esperado para evitar errores
            if header != ["timestamp", "data_raw", "data_sqr", "data_lin"]:
                 # Si el encabezado no es el de captura inicial, leemos todo el contenido
                 # Para este caso específico, el encabezado se escribe correctamente,
                 # solo necesitamos leer los datos. Asumiremos que el encabezado está en la primera fila.
                 rows_to_process.append(header) 

            for row in reader:
                if len(row) >= 2: # Asegurarse de que al menos tiene timestamp y data_raw
                    rows_to_process.append(row)
    except Exception as e:
        print(f"Error al leer el archivo para procesamiento: {e}")
        return

    # Si no hay datos (solo el encabezado o está vacío), salimos.
    if not rows_to_process:
        print("El archivo CSV está vacío o solo contiene el encabezado.")
        return
        
    new_rows = []
    
    # El encabezado final
    new_header = ["timestamp", "data_raw", "data_sqr", "data_lin"]
    new_rows.append(new_header)
    
    # 2. Procesar las filas de datos (saltando el encabezado si ya está en new_rows)
    # Si rows_to_process tiene más de 1 elemento (encabezado + datos), procesamos a partir del índice 1
    # Si solo tiene 1 elemento (el encabezado), no hacemos nada con la iteración.
    
    start_index = 1 if rows_to_process[0] == new_header else 0 # Comprobar si ya se añadió el encabezado

    for row in rows_to_process[start_index:]:
        # row[0] es el 'timestamp', row[1] es el string "5.593000,4.773310,4.644007"
        timestamp = row[0]
        data_string = row[1]
        
        try:
            # Separar el string de datos por la coma
            # Esto produce una lista: ["5.593000", "4.773310", "4.644007"]
            data_parts = data_string.split(',')
            
            # Se crea la nueva fila con el timestamp y los datos separados
            # Se usan los nombres de las columnas en el orden del encabezado:
            # timestamp, data_raw, data_sqr, data_lin
            new_row = [timestamp] + data_parts
            
            # Si el número de partes es incorrecto (ej. 2 o más de 3), aún se guarda, pero la fila tendrá más/menos columnas
            # En el ejemplo dado, se esperan 3 valores:
            if len(data_parts) == 3:
                new_rows.append(new_row)
            else:
                print(f"Advertencia: Datos inesperados en la línea. No se procesa: {data_string}")
                # Si deseas mantener la fila original en caso de error, descomenta la siguiente línea:
                # new_rows.append([timestamp, data_string, "", ""]) # Mantiene el original y deja las otras columnas vacías
                
        except Exception as e:
            print(f"Error al procesar la línea '{row}': {e}")
            new_rows.append(row) # Si hay un error, mantiene la fila original
            
    # 3. Sobrescribir el archivo CSV con los datos separados
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerows(new_rows)
        print(f"Post-procesamiento completado. Datos separados en '{filename}'. 🎉")
    except Exception as e:
        print(f"Error al escribir el archivo post-procesado: {e}")


def main():
    try:
        # Intenta abrir el puerto serial
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Conectado al puerto {SERIAL_PORT} ({BAUD_RATE} bps) 🔌")
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
        # Si el puerto serial no se puede abrir, aún intentamos el post-procesamiento si hay un archivo.
        if os.path.exists(CSV_FILE) and input("¿Desea intentar el post-procesamiento con el archivo existente? (s/n): ").lower() == 's':
            post_process_csv(CSV_FILE)
        return

    # La sección de escritura de datos permanece igual
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Escribir encabezado solo si el archivo está vacío
        if file.tell() == 0:
            writer.writerow(["timestamp","data_raw","data_sqr","data_lin"])

        print(f"Guardando datos en '{CSV_FILE}' (Ctrl+C para detener la captura)")

        try:
            while True:
                if ser.in_waiting:
                    # Lee, decodifica y limpia la línea
                    line = ser.readline().decode(errors="ignore").strip()
                    if line:
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        
                        # **IMPORTANTE:** Aquí se escribe el 'timestamp' y el 'line' (el string completo)
                        # El resto de columnas ('data_sqr', 'data_lin') se dejan vacías temporalmente.
                        # El número de elementos debe coincidir con el encabezado.
                        # ['timestamp', 'data_raw', 'data_sqr', 'data_lin'] -> 4 elementos
                        # ['timestamp', line, '', ''] -> 4 elementos
                        writer.writerow([timestamp, line, "", ""])
                        
                        print(f"{timestamp} -> {line}")
                        file.flush() # Asegura que los datos se escriban en el disco
        except KeyboardInterrupt:
            print("\nCaptura detenida por el usuario.")
        finally:
            ser.close()
            print("Puerto serial cerrado. 🚪")
    
    # Nuevo paso: Llama a la función de post-procesamiento después de cerrar el serial y el archivo
    post_process_csv(CSV_FILE)


if __name__ == "__main__":
    main()