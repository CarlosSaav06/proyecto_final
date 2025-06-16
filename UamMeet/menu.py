from dao import cita_dao, disponibilidad_dao, estudiante_dao
from modelos.cita import Cita

def ejecutar_menu():
    while True:
        rol = input("\n¿Ingresas como Estudiante o Docente? (E/D): ").strip().upper()
        if rol == "D":
            menu_docente()
        elif rol == "E":
            menu_estudiante()
        else:
            print("Rol no válido. Intente de nuevo.")

def menu_docente():
    while True:
        print("\n--- Menú Docente ---")
        print("1. Registrar disponibilidad")
        print("2. Ver disponibilidad")
        print("3. Ver y gestionar citas")
        print("4. Salir")

        opc = input("Opción: ")
        if opc == "1":
            disponibilidad_dao.agregar_disponibilidad(input("Día: "), input("Hora: "))
        elif opc == "2":
            for i, (d, h) in enumerate(disponibilidad_dao.obtener_disponibilidad(), 1):
                print(f"{i}. {d} {h}")
        elif opc == "3":
            pendientes = [c for c in cita_dao.obtener_citas() if c.estado == "Pendiente"]
            if not pendientes:
                print("No hay citas pendientes.")
                continue
            for i, c in enumerate(pendientes, 1):
                print(f"{i}. {c}")
            try:
                i = int(input("Seleccione cita: ")) - 1
                decision = input("Aceptar o Rechazar (A/R): ").strip().upper()
                if decision == "A":
                    pendientes[i].estado = "Confirmada"
                elif decision == "R":
                    cita_dao.eliminar_cita(cita_dao.obtener_citas().index(pendientes[i]))
            except Exception:
                print("Entrada inválida.")
        elif opc == "4":
            break
        else:
            print("Opción no válida.")

def menu_estudiante():
    while True:
        print("\n--- Menú Estudiante ---")
        print("1. Ver disponibilidad")
        print("2. Agendar cita")
        print("3. Ver mis citas")
        print("4. Cancelar cita")
        print("5. Salir")

        opc = input("Opción: ")
        if opc == "1":
            for i, (d, h) in enumerate(disponibilidad_dao.obtener_disponibilidad(), 1):
                print(f"{i}. {d} {h}")
        elif opc == "2":
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            estudiante = estudiante_dao.registrar_estudiante(nombre, correo)
            disp = disponibilidad_dao.obtener_disponibilidad()
            if not disp:
                     print("❌ No hay horarios disponibles. Intenta más tarde o consulta con tu docente.")
                     continue

            else:
                for i, (d, h) in enumerate(disp, 1):
                    print(f"{i}. {d} {h}")
                try:
                    i = int(input("Elija horario: ")) - 1
                    d, h = disp[i]
                    cita = Cita(estudiante, d, h)
                    cita_dao.agregar_cita(cita)
                    disponibilidad_dao.eliminar_disponibilidad(i)
                    print("✅ Cita agendada.")
                except Exception:
                    print("❌ Entrada inválida.")
        elif opc == "3":
            correo = input("Ingrese su correo para filtrar: ").strip().lower()
            citas_usuario = [
            c for c in cita_dao.obtener_citas()
            if c.estudiante.correo.strip().lower() == correo
            ]
    
            if not citas_usuario:
              print("📭 No se encontraron citas asociadas a este correo.")
            else:
              print("📅 Tus citas:")
            for i, c in enumerate(citas_usuario, 1):
              print(f"{i}. {c}")


    
        elif opc == "4":
            correo = input("Ingrese su correo: ")
            citas = [c for c in cita_dao.obtener_citas() if c.estudiante.correo == correo]
            if not citas:
                print("No tiene citas.")
            else:
                for i, c in enumerate(citas, 1):
                    print(f"{i}. {c}")
                try:
                    i = int(input("Cancelar cita #: ")) - 1
                    cita_dao.eliminar_cita(cita_dao.obtener_citas().index(citas[i]))
                    print("🗑️ Cita cancelada.")
                except Exception:
                    print("❌ Datos inválidos.")
        elif opc == "5":
            break
        else:
            print("Opción no válida.")
