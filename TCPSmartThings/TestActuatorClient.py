import socket
import threading

# Configuración del servidor
SERVER_IP = "192.168.118.34"  # Cambiar por la IP real del servidor
SERVER_PORT = 10000

def escuchar_servidor(sock):
    """Recibir paquetes del servidor"""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("Conexión cerrada por el servidor.")
                break

            # Validar paquete 0x04 0x01 0x0y
            if len(data) == 3 and data[0] == 0x04 and data[1] == 0x01:
                y = data[2] & 0x0F
                print(f"Notificación recibida: y = {y}")
            else:
                print(f"Paquete desconocido recibido: {[hex(b) for b in data]}")
    except Exception as e:
        print("Error recibiendo datos:", e)

def registrar_actuador():
    """Se conecta al servidor y registra el actuador"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            # Enviar paquete REGISTER CMD=0x03
            register_packet = bytes([0x03])
            s.sendall(register_packet)
            print("Registrado en el servidor.")

            # Iniciar hilo para recibir notificaciones
            listener_thread = threading.Thread(target=escuchar_servidor, args=(s,), daemon=True)
            listener_thread.start()

            # Mantener el programa vivo mientras se reciben notificaciones
            while True:
                pass

        except ConnectionRefusedError:
            print("No se pudo conectar al servidor.")

if __name__ == "__main__":
    registrar_actuador()
