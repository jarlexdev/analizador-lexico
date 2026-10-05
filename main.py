import sys
from lexer import Lexer, Token

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

resultados = tokens + errores
resultados.sort(key=lambda r: (r.line, r.column))

for r in resultados:
    if isinstance(r, Token):
        lexema = f"'{r.value}'"
        print(f"[TOKEN] Tipo: {r.type:<16} | Lexema: {lexema:<12} | Posición: [Línea {r.line}, Col {r.column}]")
    else:
        print(f"[ERROR LÉXICO] {r.message} '{r.char}' en Posición: [Línea {r.line}, Col {r.column}]")
