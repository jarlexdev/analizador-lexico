import sys
from lexer import Lexer

if len(sys.argv) < 2:
    print("Uso: python main.py <archivo>")
    sys.exit(1)

ruta = sys.argv[1]
try:
    with open(ruta, 'r', encoding='utf-8') as archivo:
        codigo = archivo.read()
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{ruta}'")
    sys.exit(1)

lexer = Lexer(codigo)
tokens, errores = lexer.tokenize()

for t in tokens:
    print(t)
for e in errores:
    print(e) 
