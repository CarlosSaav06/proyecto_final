from dao import cita_dao, disponibilidad_dao, estudiante_dao
from modelos.cita import Cita

def ejecutar_menu():
    while True:
        print("\n--- UAMeet ---")
        print("1. Registrar disponibilidad")
        print("2. Ver disponibilidad")
        print("3. Agendar cita")
        print("4. Ver citas")
        print("5. Cancelar cita")
        print("6. Salir")
