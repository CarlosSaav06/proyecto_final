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

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            dia = input("Día: ")
            hora = input("Hora: ")
            disponibilidad_dao.agregar_disponibilidad(dia, hora)

        elif opcion == "2":
            for i, (dia, hora) in enumerate(disponibilidad_dao.obtener_disponibilidad(), start=1):
                print(f"{i}. {dia} {hora}")

        elif opcion == "3":
            nombre = input("Nombre del estudiante: ")
            correo = input("Correo institucional: ")
            estudiante = estudiante_dao.registrar_estudiante(nombre, correo)

            disponibles = disponibilidad_dao.obtener_disponibilidad()
            if not disponibles:
                print("❌ No hay disponibilidad registrada.")
                continue

            for i, (dia, hora) in enumerate(disponibles, start=1):
                print(f"{i}. {dia} {hora}")
            indice = int(input("Elija una disponibilidad: ")) - 1
            if 0 <= indice < len(disponibles):
                dia, hora = disponibles[indice]
                cita = Cita(estudiante, dia, hora)
                cita_dao.agregar_cita(cita)
                disponibilidad_dao.eliminar_disponibilidad(indice)
                print("✅ Cita agendada.")