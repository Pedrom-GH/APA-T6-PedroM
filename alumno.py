"""
Tratamiento de ficheros de notas de alumnos mediante expresiones regulares.

Este módulo define la clase 'Alumno', que almacena el número de identificación,
el nombre y la lista de notas de cada alumno, y la función 'leeAlumnos', que lee
un fichero de texto con los datos de varios alumnos y devuelve un diccionario
indexado por el nombre de cada uno.

Autor: Pedro Muñoz Álvarez
"""

import re
import doctest


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con los datos de todos los alumnos y devuelve un
    diccionario en el que la clave es el nombre de cada alumno y su contenido
    el objeto Alumno correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171	Blanca Agirrebarrenetse	9.5
    23	Carles Balcell de Lara	4.9
    68	David Garcia Fuster	7.0
    """
    patron = re.compile(r'^\s*(\d+)\s+([A-Za-zÀ-ÿ\s]+?)\s+([\d\.\s]+)$')
    diccionario_alumnos = {}

    with open(ficAlum, 'r', encoding='utf-8') as fichero:
        for linea in fichero:
            linea = linea.strip()
            if not linea:
                continue

            match = patron.match(linea)
            if match:
                numIden = int(match.group(1))
                nombre = match.group(2).strip()

                notas_str = match.group(3).split()
                notas = [float(nota) for nota in notas_str]

                diccionario_alumnos[nombre] = Alumno(nombre, numIden, notas)

    return diccionario_alumnos


if __name__ == "__main__":
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
