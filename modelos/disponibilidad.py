class Disponibilidad:
    def __init__(self, dia, hora, docente):
        self.dia = dia
        self.hora = hora
        self.docente = docente

    def __str__(self):
        return f"{self.dia} a las {self.hora} con {self.docente.nombre}"