from datetime import datetime

class ErrorSistemaPersonalizado(Exception):
    """Excepción base para errores personalizados del sistema."""
    pass

class ErrorDatoInvalido(ErrorSistemaPersonalizado):
    """Excepción lanzada cuando un dato ingresado no es válido o no cumple el formato."""
    def __init__(self, mensaje="El dato ingresado no cumple con el formato requerido."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ErrorOperacionNoPermitida(ErrorSistemaPersonalizado):
    """Excepción para operaciones o transacciones no permitidas."""
    def __init__(self, mensaje="La operación solicitada no está permitida."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

def registrar_log(mensaje):
    """Registra eventos, errores y operaciones en el archivo sistema_logs.txt con marca de tiempo."""
    try:
        with open("sistema_logs.txt", "a", encoding="utf-8") as archivo_log:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo_log.write(f"[{timestamp}] {mensaje}\n")
    except Exception as e:
        print(f"Error crítico al escribir en el archivo de logs: {e}")

# Prueba inicial del Módulo 1
if __name__ == "__main__":
    registrar_log("Sistema iniciado correctamente desde el Módulo 1.")
    print("Módulo 1 configurado con éxito. El archivo sistema_logs.txt está listo para registrar eventos.")
