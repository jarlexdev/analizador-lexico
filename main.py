import sys

if len(sys.argv) < 2:
    print("Uso: python main.py <archivo>")
    sys.exit(1)

ruta = sys.argv[1]
print("Voy a leer:", ruta)
