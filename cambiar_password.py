
import os
import sqlite3
from getpass import getpass
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "planttech.db")

usuario = input("Nombre de usuario: ").strip().lower()
nueva_password = getpass("Nueva contraseña: ")

if len(nueva_password) < 6:
    print("Error: mínimo 6 caracteres.")
    raise SystemExit(1)

con = sqlite3.connect(DATABASE)

try:
    fila = con.execute(
        "SELECT id FROM usuarios WHERE usuario = ?",
        (usuario,)
    ).fetchone()

    if not fila:
        print("Usuario no encontrado.")
    else:
        hash_password = generate_password_hash(nueva_password)

        con.execute(
            "UPDATE usuarios SET password_hash = ? WHERE id = ?",
            (hash_password, fila[0])
        )

        con.commit()
        print("Contraseña actualizada correctamente.")

except sqlite3.Error as error:
    con.rollback()
    print("Error de base de datos:", error)

finally:
    con.close()
