"""
MÓDULO: lexer.py
PROYECTO FINAL: COMPILADORES - FASE 1
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

    # TODO: Definir los patrones de expresiones regulares en orden de prioridad.
    # Formato: ('NOMBRE_DEL_TOKEN', r'expresion_regular')
    TOKEN_SPECIFICATION = [
        # --- ELEMENTOS A IGNORAR / ESPACIOS ---
        ('NEWLINE',        r'\n'),
        ('SKIP',           r'[ \t\r]+'),
        
        # TODO: Agregar patrones para comentarios (única línea y multilínea)
        ('COMMENT_SINGLE', r'//.*'),
        ('COMMENT_MULTI',  r'/\*[\s\S]*?\*/'),

        # --- LITERALES ---
        # TODO: Agregar patrones para números enteros, flotantes y strings
        ('FLOAT_LITERAL',  r'\d+\.\d+'),
        ('INT_LITERAL',    r'\d+'),
        ('STRING_LITERAL', r'"[^"\n]*"'),

        # --- PALABRAS RESERVADAS E IDENTIFICADORES ---
        # TODO: Agregar patrones para palabras clave e identificadores
        # ('KEYWORD',        r'...'),
        ('ID',             r'[a-zA-Z_]\w*'),

        # --- OPERADORES Y DELIMITADORES ---
        # TODO: Agregar patrones para operadores (+, -, ==, =, etc.) y delimitadores ((, ), {, }, ;, etc.)
        # Relacionales
        ('OP_EQ',      r'=='),
        ('OP_NEQ',     r'!='),
        ('OP_LE',      r'<='),
        ('OP_GE',      r'>='),
        ('OP_LT', r'<'),
        ('OP_GT', r'>'),
        ('OP_ASSIGN', r'='),

        # Aritmeticos
        ('OP_PLUS',    r'\+'),
        ('OP_MINUS',   r'-'),
        ('OP_TIMES',   r'\*'),
        ('OP_DIVIDE',  r'/'),

        # Delimitadores
        ('DELIM_LPAREN',  r'\('),
        ('DELIM_RPAREN',  r'\)'),
        ('DELIM_LBRACE',  r'\{'),
        ('DELIM_RBRACE',  r'\}'),
        ('DELIM_COMMA',   r','),
        ('DELIM_SEMICOLON', r';'),

        # --- CAPTURA DE ERRORES ---
        # TODO: Patrón para detectar cadenas sin cerrar
        # ('UNTERMINATED_STRING', r'...'),

        # Comodín para capturar cualquier otro carácter no reconocido (Error Léxico)
        ('MISMATCH',       r'.'),
    ]

    # TODO: Completar el mapeo de palabras reservadas a su tipo de Token exacto
    KEYWORD_MAP = {
        'int': 'PR_INT',
        'float': 'PR_FLOAT',
        'if': 'PR_IF',
        'else': 'PR_ELSE',
        'while': 'PR_WHILE',
        'for': 'PR_FOR',
        'return': 'PR_RETURN',
        'void': 'PR_VOID',
        # ... agregar las demás palabras reservadas necesarias
    }

    def __init__(self, code: str):
        self.code = code
        # Compila la expresión regular combinando todos los grupos etiquetados
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

        line_num = 1
        line_start = 0

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

            # TODO: Manejar la lógica de actualización de líneas para comentarios multilínea
            elif kind == 'COMMENT_MULTI':
                saltos = value.count('\n')
                if saltos > 0:
                    line_num += saltos
                    line_start = position + value.rfind('\n') + 1
                continue

            # TODO: Convertir tipo KEYWORD al token específico usando KEYWORD_MAP
            # elif kind == 'KEYWORD':
            #     ...
            elif kind == 'ID' and value in self.KEYWORD_MAP:
                tokens.append(Token(self.KEYWORD_MAP[value], value, line_num, col_num))

            # TODO: Manejar casos de errores léxicos
            elif kind == 'MISMATCH':
                errors.append(LexicalError("Carácter no reconocido", value, line_num, col_num))

            # TODO: Guardar los tokens válidos restantes en la lista 'tokens'
            else:
                tokens.append(Token(kind, value, line_num, col_num))

        return tokens, errors
