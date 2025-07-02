import pwinput

def cargar_usuarios():
    usuarios = {}
    try:
        with open("usuarios.txt", "r") as archivo:
            for linea in archivo:
                usuario, contraseña, rol = linea.strip().split(",")
                usuarios[usuario] = {"contraseña": contraseña, "rol": rol}
    except FileNotFoundError:
        pass  # Si no existe, simplemente regresamos un dict vacío
    return usuarios

def guardar_usuario(usuario, contraseña, rol):
    with open("usuarios.txt", "a") as archivo:
        archivo.write(f"{usuario},{contraseña},{rol}\n")

def registrar_usuario(usuarios):
    print("\n--- Registro de nuevo usuario ---")
    while True:
        nuevo_usuario = input("Correo institucional: ").strip().lower()
        if nuevo_usuario in usuarios:
            print("Ese correo ya está registrado.")
        else:
            nueva_contraseña = pwinput.pwinput("Contraseña: ", mask="*")
            rol = input("Rol (E=Estudiante / D=Docente): ").strip().upper()
            if rol in ("E", "D"):
                guardar_usuario(nuevo_usuario, nueva_contraseña, rol)
                print(" Usuario registrado exitosamente.\n")
                return nuevo_usuario, rol
            else:
                print("Rol no válido.")

def login(usuarios):
    while True:
        print("\n--- Inicio de sesión ---")
        opcion = input("¿Deseás (I)niciar sesión o (R)egistrarte? ").strip().upper()
        if opcion == "R":
            return registrar_usuario(usuarios)
        elif opcion == "I":
            intentos = 3
            while intentos > 0:
                usuario = input("Correo institucional: ").strip().lower()
                contraseña = pwinput.pwinput("Contraseña: ", mask="*")
                if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
                    print(" Inicio de sesión exitoso.\n")
                    return usuario, usuarios[usuario]["rol"]
                else:
                    intentos -= 1
                    print(f" Credenciales incorrectas. Intentos restantes: {intentos}")
            print(" Demasiados intentos fallidos.")
            return None, None
        else:
            print("Opción inválida. Usa I o R.")
