# scanner.py
import socket

"""
Ejercicio:

Construir una utilidad de red práctica; un escaner de puertos

El objetivo aquí es crear un script que verifique un rango de puertos en un host de destino, como el suyo
 y informar cuales estan abiertos y aceptan conexiones.
 Esta es una herramienta fundamental para el diagnostico de redes y el analisis de seguridad.

 Pequeño consejo para comenzar:

 a_ Querrás crear un socket e intentar conectarte a cada puerto

 b_ Piensa como manejar el caso en el que un puerto este cerrado ( no queremos que nuestro programa se quede colgado para siempre)

 c_ Maneja los tiempos de espera y errores de conexión con elegancia


"""


def scan_port(host, port, timeout=1):
    """Check if a port is open on the given host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
        except OSError:
            return False


def scan_range(host, start_port, end_port):
    """Scan a range of ports and return list of open ports."""
    open_ports = []
    print(f"Scanning {host} from port {start_port} to {end_port}...")
    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            open_ports.append(port)
            print(f"Port {port}: OPEN")

    return open_ports


# Test your scanner
if __name__ == "__main__":
    # Scan common ports on localhost
    open_ports = scan_range("127.0.0.1", 20, 100)
    print(f"Open ports: {open_ports}")
    print(scan_port("host.que.no.existe", 80))
