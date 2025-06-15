from modelos.estudiante import Estudiante

estudiantes = []

def registrar_estudiante(nombre, correo):
    estudiante = Estudiante(nombre, correo)
    estudiantes.append(estudiante)
    return estudiante

def obtener_estudiantes():
    return estudiantes
