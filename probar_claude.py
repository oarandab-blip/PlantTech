"""Prueba rápida de la conexión con Claude (no muestra tu clave).
Uso (en la carpeta del proyecto):  .\\.venv\\Scripts\\python.exe probar_claude.py"""
import json, os, sys, time, urllib.error, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
clave = os.environ.get("ANTHROPIC_API_KEY", "").strip()
if not clave:
    try:
        clave = open(os.path.join(BASE, "clave_claude.txt"), encoding="utf-8-sig").read().strip()
    except OSError:
        pass
print(f"Largo de la clave: {len(clave)} | empieza con: {clave[:7]!r}")
if not clave:
    sys.exit("No encontré la clave (falta clave_claude.txt o ANTHROPIC_API_KEY).")

modelo = os.environ.get("PLANTTECH_MODELO_IA") or "claude-haiku-5-5"
cuerpo = {"model": modelo, "max_tokens": 60,
          "messages": [{"role": "user", "content": "Responde solo: conexión OK"}]}
peticion = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps(cuerpo).encode(),
    headers={"Content-Type": "application/json", "x-api-key": clave,
             "anthropic-version": "2023-06-01"},
    method="POST")
t = time.time()
try:
    with urllib.request.urlopen(peticion, timeout=40) as r:
        datos = json.loads(r.read().decode())
    print(f"Modelo {modelo} respondió en {time.time()-t:.1f}s:",
          "".join(b.get("text", "") for b in datos["content"]))
except urllib.error.HTTPError as e:
    print("Error HTTP", e.code, e.read().decode("utf-8", "replace")[:400])
except Exception as e:
    print("Error de conexión:", e)
