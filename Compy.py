import sys
import yacc as hola

sys.tracebacklimit = 0
from MaquinaVitual import MaquinaVirtual

if(len(sys.argv) < 2):
    print("¡Bienvenido a Compy!.")
    print("Recuerda que el comando para ejecutar es:")
    print("Compy.py (Funcion:)Compilar o Ejecutar (Archivo:)Nombre.txt")

if(len(sys.argv) == 3):
    if(str(sys.argv[1])== "Compilar" or str(sys.argv[1]) == "Ejecutar"):
        try:
            archivo = open(sys.argv[2],"r")
            contenido = archivo.read()
            archivo.close()
            if(hola.parser.parse(contenido, tracking=True) == 'PROGRAM COMPILED'):
                print("SINTAXIS VÁLIDA")
                MaquinaVirtual(hola.tabla,hola.quads)
            else:
                print("ERRORES EN LA SINTAXIS")
        except EOFError:
            print(EOFError)
    else:
        print("Funcion Incorrecta. Recuerda utilizar Compilar o Ejecutar")
