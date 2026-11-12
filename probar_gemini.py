"""Prueba de conexion con Gemini, paso a paso y con tiempos.
Uso (en la carpeta del proyecto):  .\\.venv\\Scripts\\python.exe probar_gemini.py
No muestra tu clave."""
import json, os, socket, sys, time, urllib.error, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
HOST = "generativelanguage.googleapis.com"
URL = os.environ.get("PLANTTECH_IA_URL", f"https://{HOST}/v1beta").rstrip("/")

def paso(txt): print(f"\n== {txt}")

# 1) Clave
paso("1. Clave")
clave = ""
try:
    clave = open(os.path.join(BASE, "clave_gemini.txt"), encoding="utf-8-sig").read().strip().strip('"').strip("'")
except OSError:
    pass
if not clave:
    clave = os.environ.get("GEMINI_API_KEY", "").strip()
print(f"Largo de la clave: {len(clave)}  | empieza con: {clave[:3]!r}")
if not clave:
    sys.exit("No encontre la clave (falta clave_gemini.txt).")

# 2) DNS y conexion a cada direccion
paso("2. Conexion con Google")
if os.environ.get("PLANTTECH_IA_URL"):
    infos = []
    print("(omitido: se usa una URL personalizada)")
else:
  try:
      t = time.time()
      infos = socket.getaddrinfo(HOST, 443, type=socket.SOCK_STREAM)
      print(f"DNS ok en {time.time()-t:.1f}s")
  except OSError as e:
      sys.exit(f"No se pudo resolver {HOST}: {e}\n-> Problema de internet/DNS.")
vistos = set()
for fam, tipo, proto, _, addr in infos:
    if addr[0] in vistos:
        continue
    vistos.add(addr[0])
    nombre = "IPv6" if fam == socket.AF_INET6 else "IPv4"
    t = time.time()
    try:
        s = socket.create_connection(addr[:2], timeout=8); s.close()
        print(f"  {nombre} {addr[0]}: conecta en {time.time()-t:.1f}s")
    except OSError as e:
        print(f"  {nombre} {addr[0]}: FALLA tras {time.time()-t:.1f}s ({e})")

# 3) Llamada real a la API
paso("3. Llamada a Gemini")
modelos = [os.environ.get("PLANTTECH_MODELO_IA") or "gemini-flash-latest",
           "gemini-3.8-flash", "gemini-3.5-flash-lite",
           "gemini-2.5-flash", "gemini-2.5-flash-lite"]
cuerpo = {"contents": [{"role": "user", "parts": [{"text": "Responde solo: ok"}]}],
          "generationConfig": {"maxOutputTokens": 200}}
for m in dict.fromkeys(modelos):
    req = urllib.request.Request(
        f"{URL}/models/{m}:generateContent", data=json.dumps(cuerpo).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": clave}, method="POST")
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            datos = json.loads(r.read().decode())
        partes = (datos.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
        print(f"  {m}: FUNCIONA en {time.time()-t:.1f}s -> {''.join(p.get('text','') for p in partes).strip()[:40]!r}")
        break
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", "replace")[:300].replace("\n", " ")
        print(f"  {m}: error HTTP {e.code} en {time.time()-t:.1f}s -> {detalle}")
        if e.code not in (404, 429, 500, 503):
            break
    except Exception as e:
        print(f"  {m}: sin respuesta tras {time.time()-t:.1f}s -> {type(e).__name__}: {e}")
        break
print("\nListo. Copia todo este resultado y pegalo en el chat.")
