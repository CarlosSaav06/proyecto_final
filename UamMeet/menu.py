from dao import citas_dao, disponibilidad_dao, estudiante_dao
from modelos.cita import Cita
from modelos.docente import Docente
from modelos.disponibilidad import Disponibilidad


def ejecutar_menu():  # ciclo principal que pregunta si el usuario ingresa como Estudiante, Docente o si quiere salir
    while True:
        rol = input("\n¿Ingresas como Estudiante, Docente o quieres Salir? (E/D/S): ").strip().upper()
        if rol == "D":  # Si es docente, se llama al menu de docente
            menu_docente()
        elif rol == "E":  # Si es estudiante, se llama al menu de estudiante
            menu_estudiante()
        elif rol == "S":
            print("Programa finalizado")
            break
        else:
            print("Rol no válido. Intente de nuevo.")

def menu_docente(correo):  # Menu para que el docente realice diferentes acciones
    while True:
        print("\n--- Menú Docente ---")
        print("1. Registrar disponibilidad")
        print("2. Ver disponibilidad")
        print("3. Ver y gestionar citas")
        print("4. Salir")

        opc = input("Opción: ")
        if opc == "1":  # registrar nueva disponibilidad de horario para citas
            print("\n Registrar nueva disponibilidad")
            nombre = input("Nombre del docente: ")
            correo = input("Correo del docente: ")
            docente = Docente(nombre, correo)

            dia = input("Día disponible: ")
            hora = input("Hora disponible: ")

             # Crear objeto disponibilidad y agregarlo a la base de datos (DAO)
            disponibilidad = Disponibilidad(dia, hora, docente)
            disponibilidad_dao.agregar_disponibilidad(disponibilidad)

            print(" Disponibilidad registrada correctamente.")

        elif opc == "2": # Mostrar las disponibilidades que se han registrado
           disponibilidad = disponibilidad_dao.obtener_disponibilidad()
           if not disponibilidad:
               print("No hay horarios disponibles en este momento.")
           else:
                # Listar las disponibilidades con numeración
               for i, disp in enumerate(disponibilidad_dao.obtener_disponibilidad(), 1):
                print(f"{i}. {disp.dia} {disp.hora}")

        elif opc == "3":  # Ver y gestionar citas pendientes, ya sea aceptarlas o rechazarlas
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
                elif decision == "R": # Eliminar cita rechazada de la base de datos
                    citas_dao.eliminar_cita(citas_dao.obtener_citas().index(pendientes[i]))
            except Exception:
                print("Entrada inválida.")

        elif opc == "4": # Salir del menú de los docentes
            print("Saliendo del menú docente.")
            break
        else:
            print("Opción no válida.")

def menu_estudiante(correo):  # Menu para que el estudiante pueda realizar diferentes acciones
    while True:
        print("\n--- Menú Estudiante ---")
        print("1. Ver disponibilidad")
        print("2. Agendar cita")
        print("3. Ver mis citas")
        print("4. Cancelar cita")
        print("5. Salir")

        opc = input("Opción: ")
        if opc == "1": # Mostrar horarios disponibles para agendar
            disponibilidad = disponibilidad_dao.obtener_disponibilidad()
            if not disponibilidad:
                print("No hay horarios disponibles en este momento.")
            else:
                for i, disp in enumerate(disponibilidad_dao.obtener_disponibilidad(), 1):
                     print(f"{i}. {disp.dia} {disp.hora}")

                    
        elif opc == "2": # Agendar una cita en un horario disponible
            nombre = input("Nombre: ")
            correo = input("Correo: ")
             # Registrar estudiante o recuperar existente
            estudiante = estudiante_dao.registrar_estudiante(nombre, correo)
            disp = disponibilidad_dao.obtener_disponibilidad()
            if not disp:
                     print(" No hay horarios disponibles. Intenta más tarde o consulta con tu docente.")
                     continue

            else:  # Mostrar horarios disponibles para elegir
                for i, disponibilidad in enumerate(disp, 1):
                    print(f"{i}. {disponibilidad}")
                try:
                    i = int(input("Elija horario: ")) - 1
                    
                     # seleccionar dia y hora escogidos
                    seleccion = disp[i]
                    # Crear nueva cita con estudiante y horario seleccionado
                    cita = Cita(estudiante, seleccion.dia, seleccion.hora)
                    citas_dao.agregar_cita(cita)  # Guardar cita

                    # Eliminar la disponibilidad porque ya fue usada
                    disponibilidad_dao.eliminar_disponibilidad(i)
                    citas_dao.agregar_cita(cita)

                    disponibilidad_dao.eliminar_disponibilidad(i)
                    print(" Cita agendada.")
                except Exception:
                    print(" Entrada inválida.")

        elif opc == "3":
            # Mostrar todas las citas del estudiante con ese correo
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


    
        elif opc == "4":  # Cancelar una cita existente
            
            citas = [c for c in citas_dao.obtener_citas() if c.estudiante.correo == correo]
            if not citas:
                print("No tiene citas.")
            else:
                for i, c in enumerate(citas, 1):
                    print(f"{i}. {c}")
                try:
                    i = int(input("Cancelar cita #: ")) - 1
                     # Eliminar la cita seleccionada de la base de datos

                    citas_dao.eliminar_cita(citas_dao.obtener_citas().index(citas[i]))

                    citas_dao.eliminar_cita(citas_dao.obtener_citas().index(citas[i]))

                    print(" Cita cancelada.")
                except Exception:
                    print(" Datos inválidos.")
        elif opc == "5":  # Salir del menú estudiante
            break
        else:
            print("Opción no válida.")
