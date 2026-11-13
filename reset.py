import sqlite3
from werkzeug.security import generate_password_hash

con = sqlite3.connect("planttech.db")

for (tabla,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    columnas = [c[1] for c in con.execute(f"PRAGMA table_info({tabla})")]
    print(tabla, columnas)

try:
    cur = con.execute(
        "UPDATE usuarios SET password = ? WHERE username = ?",
        (generate_password_hash("Pecas7824"), "orlandoar78"),
    )
    con.commit()
    print("Filas actualizadas:", cur.rowcount)
except Exception as e:
    print("Error:", e)

con.close()
