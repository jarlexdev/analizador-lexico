"""
MÓDULO: lexer.py
PROYECTO FINAL: COMPILADORES - FASE 1
Analizador léxico implementado con expresiones regulares (módulo nativo 're').
"""

import re
from typing import List, Tuple, NamedTuple

# ==============================================================================
# 1. ESTRUCTURAS DE DATOS
# ==============================================================================

class Token(NamedTuple):
    """Estructura para representar un Token detectado."""
    type: str
    value: str
    line: int
    column: int

class LexicalError(NamedTuple):
    """Estructura para representar un error léxico detectado."""
    message: str
    char: str
    line: int
    column: int

# ==============================================================================
# 2. CLASE PRINCIPAL DEL ANALIZADOR LÉXICO
# ==============================================================================

class Lexer:
    """
    Analizador Léxico (Scanner).
    Transforma una cadena de código fuente en una lista de Tokens y Errores Léxicos.
    """

    # Patrones en ORDEN DE PRIORIDAD: la expresión regular se queda con la
    # primera alternativa que coincide. Por eso los patrones más largos o
    # específicos van antes (ej. FLOAT antes que INT, '==' antes que '=').
    # Formato: ('NOMBRE_DEL_TOKEN', r'expresion_regular')
    TOKEN_SPECIFICATION = [
        # --- ELEMENTOS A IGNORAR / ESPACIOS ---
        ('NEWLINE',              r'\n'),
        ('SKIP',                 r'[ \t\r]+'),
        
        # --- COMENTARIOS ---
        # Van antes que los operadores para que '//' y '/*' no se lean como '/'.
        ('COMMENT_SINGLE',       r'//.*'),
        ('COMMENT_MULTI',        r'/\*[\s\S]*?\*/'),
        ('UNTERMINATED_COMMENT', r'/\*[\s\S]*'),

        # --- LITERALES ---
        ('FLOAT_LITERAL',        r'\d+\.\d+'),
        ('INT_LITERAL',          r'\d+'),
        ('STRING_LITERAL',       r'"[^"\n]*"'),

        # --- IDENTIFICADORES Y PALABRAS RESERVADAS ---
        # Las palabras reservadas se reconocen como ID y luego se buscan en
        # KEYWORD_MAP; así 'interes' no se confunde con 'int'.
        ('ID',                   r'[a-zA-Z_][a-zA-Z0-9_]*'),

        # --- OPERADORES RELACIONALES Y ASIGNACIÓN ---
        ('OP_EQ',                r'=='),
        ('OP_NEQ',               r'!='),
        ('OP_LE',                r'<='),
        ('OP_GE',                r'>='),
        ('OP_LT',                r'<'),
        ('OP_GT',                r'>'),
        ('OP_ASSIGN',            r'='),

        # --- OPERADORES ARITMÉTICOS ---
        ('OP_PLUS',              r'\+'),
        ('OP_MINUS',             r'-'),
        ('OP_TIMES',             r'\*'),
        ('OP_DIVIDE',            r'/'),

        # --- DELIMITADORES ---
        ('DELIM_LPAREN',         r'\('),
        ('DELIM_RPAREN',         r'\)'),
        ('DELIM_LBRACE',         r'\{'),
        ('DELIM_RBRACE',         r'\}'),
        ('DELIM_COMMA',          r','),
        ('DELIM_SEMICOLON',      r';'),

        # --- CAPTURA DE ERRORES ---
        ('UNTERMINATED_STRING',  r'"[^"\n]*'),      # '"' sin cierre en la línea
        ('MISMATCH',             r'.'),             # cualquier otro carácter
    ]

    # Palabras reservadas del lenguaje y su tipo de token
    KEYWORD_MAP = {
        'int': 'PR_INT',
        'float': 'PR_FLOAT',
        'if': 'PR_IF',
        'else': 'PR_ELSE',
        'while': 'PR_WHILE',
        'for': 'PR_FOR',
        'return': 'PR_RETURN',
        'void': 'PR_VOID',
    }

    def __init__(self, code: str):
        self.code = code
        # Une todos los patrones en una sola expresión con grupos con nombre
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKEN_SPECIFICATION)
        self.regex = re.compile(tok_regex)

    def tokenize(self) -> Tuple[List[Token], List[LexicalError]]:
        """
        Procesa el código fuente completo y retorna una tupla con:
        - Lista de Tokens válidos
        - Lista de Errores Léxicos encontrados
        """
        tokens: List[Token] = []
        errors: List[LexicalError] = []

        line_num = 1        # línea actual
        line_start = 0      # posición (en todo el texto) donde empieza la línea actual

        for mo in self.regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            position = mo.start()
            col_num = position - line_start + 1

            if kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue

            elif kind == 'SKIP':
                continue

            elif kind == 'COMMENT_SINGLE':
                continue

            elif kind == 'COMMENT_MULTI':
                # El comentario puede contener saltos de línea que NEWLINE no ve:
                # se cuentan aquí para mantener correctas la línea y la columna.
                saltos = value.count('\n')
                if saltos > 0:
                    line_num += saltos
                    line_start = position + value.rfind('\n') + 1
                continue

            elif kind == 'ID' and value in self.KEYWORD_MAP:
                # Palabra reservada: se usa tipo específico (PR_INT, PR_IF, ...)
                tokens.append(Token(self.KEYWORD_MAP[value], value, line_num, col_num))

            # Errores léxicos: se registran y el análisis continúa
            elif kind == 'UNTERMINATED_STRING':
                errors.append(LexicalError("Cadena sin cerrar", value, line_num, col_num))

            elif kind == 'UNTERMINATED_COMMENT':
                # Se reporta solo '/*' porque value contiene el resto del archivo
                errors.append(LexicalError("Comentario sin cerrar", '/*', line_num, col_num))

            elif kind == 'MISMATCH':
                errors.append(LexicalError("Carácter no reconocido", value, line_num, col_num))

            else:
                # Token válido: ID, literal, operador o delimitador
                tokens.append(Token(kind, value, line_num, col_num))

        return tokens, errors
