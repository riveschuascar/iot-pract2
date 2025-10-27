import socket

# Configuración del servidor
SERVER_IP = "192.168.118.34"  # Cambiar por IP real si quieres
SERVER_PORT = 10000

def enviar_paquete(valor):
    # Validar valor
    if valor not in [0, 1, 2]:
        print("Valor inválido. Debe ser 0, 1 o 2.")
        return

    # Construir paquete CMD | LEN | VAL
    CMD = 0x01
    LEN = 0x01
    VAL = 0x00 | valor  # 0x0y
    paquete = bytes([CMD, LEN, VAL])
    
    # Enviar paquete
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(paquete)
            print(f"Paquete enviado: {[hex(b) for b in paquete]}")
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor. ¿Está corriendo?")

if __name__ == "__main__":
    while True:
        try:
            valor = int(input("Ingrese valor (0, 1 o 2) para enviar: "))
            enviar_paquete(valor)
        except ValueError:
            print("Por favor ingrese un número válido.")
