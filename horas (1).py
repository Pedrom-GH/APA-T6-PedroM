"""
Análisis y normalización de expresiones horarias mediante expresiones regulares.

Este módulo proporciona la función 'normalizaHoras', que lee un fichero de texto,
busca en él las expresiones horarias escritas en lenguaje natural (castellano) y
genera un nuevo fichero en el que dichas expresiones se reescriben en el formato
estándar HH:MM. Las expresiones incorrectas se dejan sin modificar.

Autor: Pedro Muñoz Álvarez
"""

import re


def procesar_coincidencia(match):
    """
    Función auxiliar que decide si una coincidencia de la expresión regular
    es una hora válida y, si lo es, la transforma al formato HH:MM. Si la
    expresión es incorrecta, devuelve el texto original sin modificar.
    """
    texto_original = match.group(0)

    # La hora puede haber encajado en cualquiera de las cuatro alternativas
    h_str = (match.group('h1') or match.group('h2')
             or match.group('h3') or match.group('h4'))
    if not h_str:
        return texto_original

    hora = int(h_str)
    hora_original = hora
    minutos = 0

    # 1. Formato con dos puntos (18:30): los minutos deben tener dos dígitos
    if match.group('minutos'):
        minutos = int(match.group('minutos'))
        if minutos > 59 or hora > 23:
            return texto_original

    # 2. Formato con 'h' (8h27m, 17h5m, 8h): los minutos admiten uno o dos dígitos
    elif match.group('minutos_h'):
        minutos = int(match.group('minutos_h'))
        if minutos > 59 or hora > 23:
            return texto_original

    # 3. Formato hablado con partícula (en punto, y cuarto, y media, menos cuarto)
    elif match.group('texto_min'):
        texto_min = match.group('texto_min').lower()
        if 'y cuarto' in texto_min:
            minutos = 15
        elif 'y media' in texto_min:
            minutos = 30
        elif 'menos cuarto' in texto_min:
            minutos = 45
            hora -= 1
        elif 'en punto' in texto_min:
            minutos = 0

        # En lenguaje hablado la hora base debe estar entre 1 y 12
        if not (1 <= hora_original <= 12):
            return texto_original

        # Ajuste al restar (1 menos cuarto -> 12:45, que luego pasa a 00:45)
        if hora == 0:
            hora = 12

    modificador = match.group('mod')

    # 4. Validación y ajuste según el modificador (de la mañana, tarde, etc.)
    if modificador:
        modificador = modificador.lower()

        # Con modificador el reloj siempre es de 1 a 12
        if not (1 <= hora_original <= 12):
            return texto_original

        if 'mañana' in modificador:
            if not (4 <= hora_original <= 12):
                return texto_original
            if hora == 12:
                hora = 0
        elif 'mediodía' in modificador:
            if not (1 <= hora_original <= 3 or hora_original == 12):
                return texto_original
            if hora != 12:
                hora += 12
        elif 'tarde' in modificador:
            if not (3 <= hora_original <= 8):
                return texto_original
            if hora != 12:
                hora += 12
        elif 'noche' in modificador:
            if not (8 <= hora_original <= 12 or 1 <= hora_original <= 4):
                return texto_original
            if hora == 12:
                hora = 0
            elif hora < 12:
                hora += 12
        elif 'madrugada' in modificador:
            if not (1 <= hora_original <= 6):
                return texto_original
    else:
        # Formato hablado sin modificador (8 en punto): rango 00:00 a 11:59
        if match.group('texto_min'):
            if hora == 12:
                hora = 0

    return f"{hora:02d}:{minutos:02d}"


def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero de texto 'ficText', busca en él las expresiones horarias
    mediante expresiones regulares y escribe el fichero 'ficNorm' con dichas
    expresiones reescritas en el formato normalizado HH:MM. Las expresiones
    incorrectas se mantienen tal cual.
    """
    patron = re.compile(
        r'\b(?:'
        r'(?P<h1>\d{1,2}):(?P<minutos>\d{2})\b|'
        r'(?P<h2>\d{1,2})h(?P<minutos_h>\d{1,2})?m?\b|'
        r'(?P<h3>\d{1,2})\s+(?P<texto_min>en punto|y cuarto|y media|menos cuarto)\b|'
        r'(?P<h4>\d{1,2})(?=\s+(?:de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))'
        r')'
        r'(?:\s+(?P<mod>de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))?',
        re.IGNORECASE
    )

    with open(ficText, 'r', encoding='utf-8') as f_in, \
         open(ficNorm, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            linea_mod = patron.sub(procesar_coincidencia, linea)
            f_out.write(linea_mod)


if __name__ == "__main__":
    normalizaHoras('horas.txt', 'horas_normalizadas.txt')
