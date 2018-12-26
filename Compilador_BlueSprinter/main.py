import sys
from app.compilador import Compilador



if __name__ == "__main__":
    if len(sys.argv) > 2:
        compilador = Compilador()
        compilador.compilar(sys.argv[1])
        compilador.exportar(sys.argv[2])
    else:
        print("Use: python main.py <fonte> <asm>")
