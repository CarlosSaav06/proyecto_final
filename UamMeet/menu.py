from dao import citas_dao, disponibilidad_dao, estudiante_dao
from modelos.cita import Cita
from modelos.docente import Docente
from modelos.disponibilidad import Disponibilidad


def ejecutar_menu():
    while True:
        rol = input("\n¿Ingresas como Estudiante, Docente o quieres Salir? (E/D/S): ").strip().upper()
        if rol == "D":
            menu_docente()
        elif rol == "E":
            menu_estudiante()
        elif rol == "S":
            print("Programa finalizado")
            break
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
            print("\n Registrar nueva disponibilidad")
            nombre = input("Nombre del docente: ")
            correo = input("Correo del docente: ")
            docente = Docente(nombre, correo)

            dia = input("Día disponible: ")
            hora = input("Hora disponible: ")

            disponibilidad = Disponibilidad(dia, hora, docente)
            disponibilidad_dao.agregar_disponibilidad(disponibilidad)

            print(" Disponibilidad registrada correctamente.")
        elif opc == "2":
           disponibilidad = disponibilidad_dao.obtener_disponibilidad()
           if not disponibilidad:
               print("No hay horarios disponibles en este momento.")
           else:
               for i, (dia, hora) in enumerate(disponibilidad, 1):
                   print(f"{i}. {dia} a las {hora}")

        elif opc == "3":
            pendientes = [c for c in citas_dao.obtener_citas() if c.estado == "Pendiente"]
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
                    citas_dao.eliminar_cita(citas_dao.obtener_citas().index(pendientes[i]))
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
            disponibilidad = disponibilidad_dao.obtener_disponibilidad()
            if not disponibilidad:
                print("No hay horarios disponibles en este momento.")
            else:
                for i, (dia, hora) in enumerate(disponibilidad, 1):
                    print(f"{i}. {dia} a las {hora}")
                    
        elif opc == "2":
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            estudiante = estudiante_dao.registrar_estudiante(nombre, correo)
            disp = disponibilidad_dao.obtener_disponibilidad()
            if not disp:
                     print(" No hay horarios disponibles. Intenta más tarde o consulta con tu docente.")
                     continue

            else:
                for i, disponibilidad in enumerate(disp, 1):
                    print(f"{i}. {disponibilidad}")
                try:
                    i = int(input("Elija horario: ")) - 1

                    d, h = disp[i]
                    cita = Cita(estudiante, d, h)
                    citas_dao.agregar_cita(cita)

                    seleccion = disp[i]
                    cita = Cita(estudiante, seleccion.dia, seleccion.hora)
                    cita_dao.agregar_cita(cita)
                    disponibilidad_dao.eliminar_disponibilidad(i)
                    cita_dao.agregar_cita(cita)

                    disponibilidad_dao.eliminar_disponibilidad(i)
                    print(" Cita agendada.")
                except Exception:
                    print(" Entrada inválida.")
        elif opc == "3":
            correo = input("Ingrese su correo para filtrar: ").strip().lower()
            citas_usuario = [

            c for c in citas_dao.obtener_citas()

        
            if c.estudiante.correo.strip().lower() == correo
            ]
    
            if not citas_usuario:
              print(" No se encontraron citas asociadas a este correo.")
            else:
              print(" Tus citas:")
            for i, c in enumerate(citas_usuario, 1):
              print(f"{i}. {c}")


    
        elif opc == "4":
            correo = input("Ingrese su correo: ")
            citas = [c for c in citas_dao.obtener_citas() if c.estudiante.correo == correo]
            if not citas:
                print("No tiene citas.")
            else:
                for i, c in enumerate(citas, 1):
                    print(f"{i}. {c}")
                try:
                    i = int(input("Cancelar cita #: ")) - 1

                    citas_dao.eliminar_cita(citas_dao.obtener_citas().index(citas[i]))

                    cita_dao.eliminar_cita(cita_dao.obtener_citas().index(citas[i]))

                    print(" Cita cancelada.")
                except Exception:
                    print(" Datos inválidos.")
        elif opc == "5":
            break
        else:
            print("Opción no válida.")
