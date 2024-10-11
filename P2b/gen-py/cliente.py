from calculadora import Calculadora
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# Obtiene los arguentos para las operaciones, manejado valores incorrectos o indefinidos
def obtener_numeros(op):
    n1, n2, st = None, None, None
    if op in ['+', '-', '*', '/']:
        n1 = float(input("Introduzca el primer número: "))
        n2 = float(input("Introduzca el segundo número: "))
        if op == '/' and n2 == 0:
            while n2 == 0:
                print("Error. Introduzca un divisor distinto de cero.")
                n2 = float(input("Introduzca el segundo número: "))
    elif op in ['^', 'r']: 
        n1 = float(input("Introduzca la base: "))
        if op == 'r' and n1 < 0:
            while n1 < 0:
                print("Error. Introduzca un valor positivo.")
                n1 = float(input("Introduzca la base: "))
        n2 = float(input("Introduzca el exponente: "))
        if op == 'r' and n2 == 0:
            while n2 == 0:
                print("Error. Introduzca un valor distinto de cero.")
                n2 = float(input("Introduzca el exponente: "))
    elif op == 'l':
        n1 = float(input("Introduzca la base: "))
        if n1 <= 0 or n1 == 1:
            while n1 <= 0 or n1 == 1:
                print("Error. Introduzca un valor mayor de cero y distinto de 1.")
                n1 = float(input("Introduzca la base: "))
        n2 = float(input("Introduzca el número: "))
        if n2 <= 0:
            while n2 <= 0:
                print("Error. Introduzca un valor mayor de cero.")
                n2 = float(input("Introduzca el número: "))
    elif op in ['s', 'c', 't']:
        if op == 't':
            print("NO introducir valores indefinidos como 90, 270")
        n1 = float(input("Introduzca los grados: "))
    elif op == 'v':
        n1 = float(input("Introduzca el número: "))
        st = input("Introduzca las unidades del número anterior (rad o grad): ")
        while st != "grad" and st != "rad":
                print("Error. Introduzca unidades validas.")
                st = input("Introduzca las unidades (rad o grad): ")
    return n1, n2, st

def rellenar_vector(): 
    v = []
    print("Introduce los elementos del vector, separados por espacios:")
    elementos = input().split() 
    elementos_float = [float(elemento) for elemento in elementos]
    v.append(elementos_float)  # Agregar los elementos convertidos al vector
    return v

def rellenar_matriz(): 
    m = [] 
    print("Introduce los elementos de la matriz, separados por espacios. Presiona Enter al finalizar.")
    
    while True:
        fila = input("Introduce una fila (deja vacío para terminar): ").strip()
        if not fila:  # Si la fila está vacía, terminar la entrada
            break
        fila = fila.split()  # Separar los elementos de la fila por espacios
        fila = [int(x) for x in fila]  # Convertir los elementos a enteros
        m.append(fila)  # Agregar la fila a la matriz
        
    return m

def imprimir_vectores(vectores):
    for i, vector in enumerate(vectores):
        if len(vector) == 1 and isinstance(vector[0], list):
            vector_plano = vector[0]
            print(f"Vector {i+1}: {vector_plano}")
        else:
            print(f"Vector {i+1}: {vector}")

def imprimir_matriz(m):
    print(f"Matriz: {m}");

def main():
    vectores = [[], [], []]
    m1 = [[], [], []]
    m2 = [[], [], []]
    try:
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Calculadora.Client(protocol)
        transport.open()

        # Bucle principal
        while True:
            print("Selecione un modo: ")
            print(" 1 : Para calculadora básica")
            print(" 2 : Para calculadora de vectores")
            print(" 3 : Para calculadora de matrices")
            print(" e : Para salir (exit)")

            modo = input("Ingrese su selección: ")
            print("****************************************************")

            if modo == 'e':
                break

            if modo == '1':
                while True:
                    print("Selecione una operación: ")
                    print(" + : Para una suma")
                    print(" - : Para una resta")
                    print(" * : Para una multiplicacion")
                    print(" / : Para una division")
                    print(" ^ : Para una potencia")
                    print(" l : Para un logaritmo")
                    print(" r : Para una raiz de exponente x")
                    print(" s : Para seno (grados)")
                    print(" c : Para coseno (grados)")
                    print(" t : Para tangente (grados)")
                    print(" v : Para una conversion (grados-radianes)")
                    print(" o : Para volver")

                    op = input("Ingrese su selección: ")

                    if op not in ['+', '-', '*', '/', '^', 'r', 'l', 's', 'c', 't', 'v', 'o']:
                        print("Operación no válida.")
                        continue

                    if op == 'o':
                        print("****************************************************")
                        break

                    n1, n2, st = obtener_numeros(op)

                    # Realizar la operación seleccionada
                    if op == '+':
                        resultado = client.suma(n1, n2)
                    elif op == '-':
                        resultado = client.resta(n1, n2)
                    elif op == '*':
                        resultado = client.multiplicacion(n1, n2)
                    elif op == '/':
                        resultado = client.division(n1, n2)
                    elif op == '^':
                        resultado = client.potencia(n1, n2)
                    elif op == 'l':
                        resultado = client.logaritmo(n1, n2)
                    elif op == 'r':
                        resultado = client.raiz(n1, n2)
                    elif op == 's':
                        resultado = client.seno(n1)
                    elif op == 'c':
                        resultado = client.coseno(n1)
                    elif op == 't':
                        resultado = client.tangente(n1)
                    elif op == 'v':
                        resultado = client.conversion(n1, st)

                    print(f"~~ El resultado de la operación {op} es: {resultado} ~~")
                    print("******************************************************")

            elif modo == '2':
                while True:
                    imprimir_vectores(vectores)
                    print("Selecione una operación: ")
                    print(" q : Para modificar algún vector")
                    print(" + : Para una suma de vectores")
                    print(" - : Para una resta de vectores")
                    print(" . : Para producto escalar")
                    print(" x : Para producto vectorial")
                    print(" n : Para norma")
                    print(" a : Para angulo entre vectores")
                    print(" m : Para producto mixto")
                    print(" o : Para volver al modo anterior")

                    op = input("Ingrese su selección: ")

                    if op not in ['q', '+', '-', '.', 'x', 'n', 'a', 'm', 'o']:
                        print("Operación no válida.")
                        continue

                    if op == 'o':
                        print("****************************************************")
                        break

                    if op == 'q':
                        n = int(input("Selecciona un vector a modificar (1, 2 o 3): "))
                        vectores[n - 1] = rellenar_vector()
                    elif op == '+':
                        seleccion = input("Selecciona dos vectores (1, 2 o 3) separados por espacios: ").split()
                        resultado = client.suma_vectores(vectores[int(seleccion[0])-1][0], vectores[int(seleccion[1])-1][0])
                    elif op == '-':
                        seleccion = input("Selecciona dos vectores (1, 2 o 3) separados por espacios: ").split()
                        resultado = client.resta_vectores(vectores[int(seleccion[0])-1][0], vectores[int(seleccion[1])-1][0])
                    elif op == '.':
                        seleccion = input("Selecciona dos vectores (1, 2 o 3) separados por espacios: ").split()
                        resultado = client.producto_escalar(vectores[int(seleccion[0])-1][0], vectores[int(seleccion[1])-1][0])
                    elif op == 'x':
                        print("Los vectores deben tener la misma longitud y ser de dimensión 3")
                        seleccion = input("Selecciona dos vectores (1, 2 o 3) separados por espacios: ").split()
                        resultado = client.producto_vectorial(vectores[int(seleccion[0])-1][0], vectores[int(seleccion[1])-1][0])
                    elif op == 'n':
                        resultado = client.norma(vectores[int(input("Selecciona un vector (1, 2 o 3): "))-1][0])
                    elif op == 'a':
                        seleccion = input("Selecciona dos vectores (1, 2 o 3) separados por espacios: ").split()
                        resultado = client.angulo_vectores(vectores[int(seleccion[0])-1][0], vectores[int(seleccion[1])-1][0])
                    elif op == 'm':
                        print("Los vectores deben tener la misma longitud y ser de dimensión 3")
                        seleccion = input("Selecciona 3 vectores (1, 2 o 3) separados por espacios: ").split()
                        resultado = client.producto_mixto(vectores[int(seleccion[0])-1][0], vectores[int(seleccion[1])-1][0], vectores[int(seleccion[2])-1][0])
                    
                    if op != 'q':
                        print(f"~~ El resultado de la operación {op} es: {resultado} ~~")

                    print("****************************************************")
            
            elif modo == '3':
                while True:
                    imprimir_matriz(m1)
                    imprimir_matriz(m2)
                    print("Selecione una operación: ")
                    print(" q : Para modificar alguna matriz")
                    print(" + : Para suma de matrices (m1 + m2)")
                    print(" - : Para resta de matrices (m1 - m2)")
                    print(" x : Para producto de matrices (m1 x m2)")
                    print(" d : Para determinante (m1)")
                    print(" i : Para inversa (m1)")
                    print(" o : Para volver al modo anterior")

                    op = input("Ingrese su selección: ")

                    if op not in ['q', '+', '-', 'x', 'd', 'i', 'o']:
                        print("Operación no válida.")
                        continue

                    if op == 'o':
                        print("****************************************************")
                        break

                    if op == 'q':
                        n = int(input("Selecciona una matriz a modificar (1 o 2): "))
                        if n == 1:
                            m1 = rellenar_matriz()
                        elif n == 2:
                            m2 = rellenar_matriz() 
                    elif op == '+':
                        resultado = client.suma_matrices(m1,m2)
                    elif op == '-':
                        resultado = client.resta_matrices(m1,m2)
                    elif op == 'x':
                        resultado = client.producto_matrices(m1, m2)
                    elif op == 'd':
                        resultado = client.determinante(m1)
                    elif op == 'i':
                        resultado = client.inversa(m1)
                    
                    if op != 'q':
                        print(f"~~ El resultado de la operación {op} es: {resultado} ~~")

                    print("****************************************************")
            else:
                print("Modo no válido. Por favor, seleccione 1, 2 o 3.")

        transport.close()

    except Thrift.TException as tx:
        print(f"Error al conectarse al servidor: {tx.message}")

if __name__ == '__main__':
    main()