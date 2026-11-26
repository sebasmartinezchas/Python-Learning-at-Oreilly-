"""
Package and publish a Python Library / Introduing the Python Packaging Ecosystem

Key Topics:
- The Python Packaging Ecosystem(PyPy,pip)
- Standard Package Structure
- Distribution Format (stdis vs wheel)
- Packaging tools like uv


Key Terms:
- Pypy (Python Package Index): The official repository for Python packages, where developers can publish and share their libraries.
- Distribution Format: The format in which Python packages are distributed, such as source distributions (sdist) and built distributions (wheel)
- Package metadatada: Information about your package (name, version, etc)
- Entry Points: A way to make your script runnable as a command-line tool after installation.

"""


# texutils.py: Example Python module for packaging demonstration
def word_count(text):
    """Return the number of words in the given text."""
    return len(text.split()) # ¿Porque lo pasa a una lista de palabras antes de contar? Porque split()
    #divide el texto en palabras separadas, y luego len() cuenta cuántas palabras hay.


def reverse_text(text):
    """Return the given text reversed."""
    return " ".join(text.split()[::-1]) # ¿Por qué lo hace? Porque split() divide el texto en palabras
# y [::-1] invierte el orden de las palabras. Luego join() las une nuevamente en una cadena. El orden siempre es de la operación
# interna a externa, primero se invierte la lista de palabras y luego se unen en una cadena.


# test
if __name__ == "__main__":
    sample_text = "Hello world"
    print("Word count:", word_count(sample_text))
    print("Reversed text:", reverse_text(sample_text))
