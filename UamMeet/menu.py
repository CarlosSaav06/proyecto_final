from dao import citas_dao, disponibilidad_dao, estudiante_dao
from modelos.cita import Cita
from modelos.docente import Docente
from modelos.disponibilidad import Disponibilidad


def ejecutar_menu():  # ciclo principal que pregunta si el usuario ingresa como Estudiante, Docente o si quiere salir
    while True:
        rol = input("\n¿Ingresas como Estudiante, Docente o quieres Salir? (E/D/S): ").strip().upper()
        if rol in ("D", "E"):
            correo = input("Correo: ").strip().lower()
            contrasena = input("Contraseña: ").strip()
            if validar_usuario(rol, correo, contrasena):
                if rol == "D":
                    menu_docente(correo)
                else:
                    menu_estudiante(correo)
            else:
                print("Correo o contraseña incorrectos.")
        elif rol == "S":
            print("!Hasta luego!")
            break
        else:
            print("Rol no válido. Intente de nuevo.")


def validar_usuario(rol, correo, contrasena):
    # Ejemplo si tienes un archivo usuarios.txt con líneas: correo,contrasena,rol
    try:
        with open("usuarios.txt", "r") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) == 3:
                    c, p, r = datos
                    if c.strip().lower() == correo and p == contrasena and r.upper() == rol:
                        return True
    except FileNotFoundError:
        pass
    return False

def menu_docente(correo):  # Menu para que el docente realice diferentes acciones
    while True:
        print("\n--- Menú Docente ---")
        print("1. Registrar disponibilidad")
        print("2. Ver disponibilidad")
        print("3. Ver y gestionar citas")
        print("4. Volver al menú principal")

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
            # Filtrar solo las citas pendientes del docente actual
            pendientes = [
                c for c in citas_dao.obtener_citas()
                if c.estado == "Pendiente" and hasattr(c, "estudiante") and c.docente.correo == correo
            ]
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
            return
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
            estudiante = estudiante_dao.registrar_estudiante(nombre, correo)
            disp = disponibilidad_dao.obtener_disponibilidad()
            if not disp:
                print(" No hay horarios disponibles. Intenta más tarde o consulta con tu docente.")
                continue

            for idx, disponibilidad in enumerate(disp, 1):
                print(f"{idx}. {disponibilidad.dia} {disponibilidad.hora} - Docente: {disponibilidad.docente.nombre}")
        
            try:
                i = int(input("Elija horario: ")) - 1
                seleccion = disp[i]
                docente = seleccion.docente
                cita = Cita(estudiante, seleccion.dia, seleccion.hora, docente)
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

        elif opc == "4":  # Cancelar una cita
            citas = [c for c in citas_dao.obtener_citas() if c.estudiante.correo.strip().lower() == correo]
            if not citas:
                print(" No tienes citas agendadas.")
                
            else:
                for i, c in enumerate(citas, 1):
                    print(f"{i}. {c}")
                try:
                    i = int(input("Seleccione cita a cancelar: ")) - 1
                    citas_dao.eliminar_cita(citas_dao.obtener_citas().index(citas[i]))
                    print("Cita cancelada.")
                except Exception:
                    print("Datos invalidos")

        elif opc == "5":  # Salir del menú de los estudiantes
            print("Saliendo del menú estudiante.")
            break    
        
        else:
            print("Opción no válida.")