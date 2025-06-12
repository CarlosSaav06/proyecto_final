from modelos.cita import Cita

citas = []

def agregar_cita(cita: Cita):
    citas.append(cita)

def obtener_citas():
    return citas

def eliminar_cita(index):
    if 0 <= index < len(citas):
        citas.pop(index)