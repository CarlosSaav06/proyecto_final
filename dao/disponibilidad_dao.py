disponibilidad = []

def agregar_disponibilidad(dia, hora):
    disponibilidad.append((dia, hora))

def obtener_disponibilidad():
    return disponibilidad

def eliminar_disponibilidad(index):
    if 0 <= index < len(disponibilidad):
        disponibilidad.pop(index)