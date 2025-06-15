citas = []

def agregar_cita(cita):
    citas.append(cita)

def obtener_citas():
    return citas

def eliminar_cita(indice):
    if 0 <= indice < len(citas):
        citas.pop(indice)
