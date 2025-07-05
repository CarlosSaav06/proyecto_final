class Cita:
    def __init__(self, estudiante, dia, hora, docente):
        self.estudiante = estudiante
        self.dia = dia
        self.hora = hora
        self.docente = docente
        self.estado = "Pendiente"

    def __str__(self):
        return f"{self.dia} {self.hora} - {self.docente.nombre} ({self.estado})"
