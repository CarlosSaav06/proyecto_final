class Cita:
    def __init__(self, estudiante, dia, hora):
        self.estudiante = estudiante
        self.dia = dia
        self.hora = hora
        self.estado = "Pendiente"

    def __str__(self):
        return f"{self.dia} {self.hora} - {self.estudiante.nombre} ({self.estado})"
