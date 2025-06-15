disponibilidad = []

def agregar_disponibilidad(dia, hora):
    disponibilidad.append((dia, hora))

def obtener_disponibilidad():
    return disponibilidad


def eliminar_disponibilidad(index):
    if 0 <= index < len(disponibilidad):
        disponibilidad.pop(index)

def eliminar_disponibilidad(indice):
    if 0 <= indice < len(disponibilidad):
        disponibilidad.pop(indice)

