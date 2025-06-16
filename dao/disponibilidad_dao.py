disponibilidad = []
def agregar_disponibilidad(disponibilidad_obj):
    disponibilidad.append(disponibilidad_obj)

def obtener_disponibilidad():
    return disponibilidad

def eliminar_disponibilidad(indice):
    if 0 <= indice < len(disponibilidad):
        disponibilidad.pop(indice)