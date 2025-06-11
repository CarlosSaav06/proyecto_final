class Cita:
    def __init__(self, estudiante, dia, hora):
        self.estudiante = estudiante  # Objeto Estudiante
        self.dia = dia
        self.hora = hora
        self.estado = "Pendiente"

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.dia} {self.hora} ({self.estado})"
