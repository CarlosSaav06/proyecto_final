from UamMeet.menu import menu_estudiante, menu_docente
from UamMeet import autenticacion

def main():
    # Carga usuarios existentes desde el archivo usuarios.txt
    usuarios = autenticacion.cargar_usuarios()

    # Pide iniciar sesión o registrarse
    while True:
         correo, rol = autenticacion.login(usuarios)
   

         if correo and rol:
            if rol == "E":
               menu_estudiante(correo)  # Le pasa el correo al menú del estudiante
            elif rol == "D":
               menu_docente(correo)     # Le pasa el correo al menú del docente
            else:
               print(" Rol desconocido. No se puede continuar.")
         else:
           print(" No se pudo iniciar sesión.")

         salir = input("¿Deseas cerrar el programa? (S/N): ").strip().upper()
         if salir == "S":
            print("Cerrando UAMeet...")
            break

if __name__ == "__main__":
    main()
