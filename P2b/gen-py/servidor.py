import glob
import sys
import math
from calculadora import Calculadora

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import logging

logging.basicConfig(level=logging.DEBUG)

class CalculadoraHandler :
    def __init__(self):
        self.log = {}

    def ping(self):
        print('Me han hecho ping()')

    def suma(self, n1, n2):
        print(f"suma({n1}, {n2})")
        return n1 + n2

    def resta(self, n1, n2):
        print(f"resta({n1}, {n2})")
        return n1 - n2

    def multiplicacion(self, n1, n2):
        print(f"multiplicacion({n1}, {n2})")
        return n1 * n2

    def division(self, n1, n2):
        print(f"division({n1}, {n2})")
        if n2 == 0 :
            raise ValueError("No se puede dividir por 0")
        return n1 / n2

    def potencia(self, base, exponente):
        print(f"potencia({base}, {exponente})")
        return base ** exponente

    def logaritmo(self, base, num):
        print(f"logaritmo({base}, {num})")
        if base <= 0 or base == 1:
            raise ValueError("La base no puede ser <= 0 ni 1")
        return math.log(num, base)

    def raiz(self, base, exponente):
        print(f"raiz({base}, {exponente})")
        return base ** (1/exponente)
    
    def seno(self, n1):
        print(f"seno({n1})")
        return round(math.sin(math.radians(n1)),5)
    
    def coseno(self, n1):
        print(f"coseno({n1})")
        return round(math.cos(math.radians(n1)),5)
    
    def tangente(self, n1):
        print(f"tangente({n1})")
        return round(math.tan(math.radians(n1)),5)
    
    def conversion(self, n1, strn):
        print(f"conversion({n1}, {strn})")
        if strn == 'rad':
            return math.degrees(n1)
        elif strn == 'grad':
            return math.radians(n1)
        else:
            raise ValueError("La cadena strn debe ser 'rad' o 'grad'")

    # VECTORES
    def suma_vectores(self, vect1, vect2):
        print(f"suma_vectores({vect1}, {vect2})")
        suma = []
        for i in range(len(vect1)):
            suma.append(vect1[i] + vect2[i])
        return suma
    
    def resta_vectores(self, vect1, vect2):
        print(f"resta_vectores({vect1}, {vect2})")
        resta = []
        for i in range(len(vect1)):
            resta.append(vect1[i] - vect2[i])
        return resta
    
    def producto_escalar(self, vect1, vect2):
        print(f"producto_escalar({vect1}, {vect2})")
        if len(vect1) != len(vect2):
            raise ValueError("Los vectores deben tener la misma longitud")
        prod = 0
        for i in range(len(vect1)):
            prod += vect1[i] * vect2[i]
        return prod
    
    def producto_vectorial(self, vect1, vect2):
        print(f"producto_vectorial({vect1}, {vect2})")
        if len(vect1) != len(vect2) or len(vect1) != 3 or len(vect2) != 3:
            raise ValueError("Los vectores deben tener la misma longitud y ser de dimensión 3")        
        prod = [ vect1[1] * vect2[2] - vect1[2] * vect2[1],
            vect1[2] * vect2[0] - vect1[0] * vect2[2],
            vect1[0] * vect2[1] - vect1[1] * vect2[0] ]
        return prod
    
    def norma(self, vect1):
        print(f"norma({vect1})")
        norma = math.sqrt(sum(x**2 for x in vect1))
        return norma
    
    def angulo_vectores(self, vect1, vect2):
        print(f"angulo_vectores({vect1}, {vect2})")
        producto_escalar = sum(v1 * v2 for v1, v2 in zip(vect1, vect2))
        norma_vect1 = math.sqrt(sum(v**2 for v in vect1))
        norma_vect2 = math.sqrt(sum(v**2 for v in vect2))
        coseno_angulo = producto_escalar / (norma_vect1 * norma_vect2)
        angulo_rad = math.acos(coseno_angulo)
        angulo_grados = math.degrees(angulo_rad)
        return angulo_grados
    
    def producto_mixto(self, vect1, vect2, vect3):
        print(f"producto_mixto({vect1}, {vect2}, {vect3})")
        if len(vect1) != 3 or len(vect2) != 3 or len(vect3) != 3:
            raise ValueError("Todos vectores deben ser de dimensión 3")
        
        prod = ( vect1[0] * (vect2[1] * vect3[2] - vect2[2] * vect3[1]) +
            vect1[1] * (vect2[2] * vect3[0] - vect2[0] * vect3[2]) +
            vect1[2] * (vect2[0] * vect3[1] - vect2[1] * vect3[0]) )
        return prod

    def suma_matrices(self, m1, m2):
        print(f"suma_matrices({m1}, {m2})")
        if len(m1) != len(m2) or any(len(row1) != len(row2) for row1, row2 in zip(m1, m2)):
            raise ValueError("Error: Las matrices deben tener las mismas dimensiones.")
        
        suma = [[m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]
        return suma
    
    def resta_matrices(self, m1, m2):
        print(f"resta_matrices({m1}, {m2})")
        if len(m1) != len(m2) or any(len(row1) != len(row2) for row1, row2 in zip(m1, m2)):
            raise ValueError("Error: Las matrices deben tener las mismas dimensiones.")
        
        resta = [[m1[i][j] - m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]
        return resta
    
    def producto_matrices(self, m1, m2):
        print(f"producto_matrices({m1}, {m2})")
        if len(m1[0]) != len(m2):
            print("Error: El número de columnas de la primera matriz debe ser igual al de filas de la segunda.")
            return None

        prod = [[0 for _ in range(len(m2[0]))] for _ in range(len(m1))]

        for i in range(len(m1)):
            for j in range(len(m2[0])):
                for k in range(len(m2)):
                    prod[i][j] += m1[i][k] * m2[k][j]
        return prod
    
    def determinante(self, m1):
        print(f"determinante({m1})")
        if len(m1) != len(m1[0]):
            raise ValueError("Error: La matriz no es cuadrada.")
        if len(m1) == 2:
            det = m1[0][0] * m1[1][1] - m1[0][1] * m1[1][0]
            return det
        if len(m1) == 3:
            det = (m1[0][0] * m1[1][1] * m1[2][2] + 
                m1[0][1] * m1[1][2] * m1[2][0] +
                m1[0][2] * m1[1][0] * m1[2][1] -
                m1[0][2] * m1[1][1] * m1[2][0] -
                m1[0][0] * m1[1][2] * m1[2][1] -
                m1[0][1] * m1[1][0] * m1[2][2])
        if len(m1) != 2 and len(m1) != 3:
            raise ValueError("Error: La matriz tiene que ser de rango 2 o 3.")
        return det


    def inversa3x3(self, m):
        if len(m) != len(m[0]):
            print("Error: La matriz no es cuadrada.")
            return None
        det = (m[0][0] * m[1][1] * m[2][2] + 
                m[0][1] * m[1][2] * m[2][0] +
                m[0][2] * m[1][0] * m[2][1] -
                m[0][2] * m[1][1] * m[2][0] -
                m[0][0] * m[1][2] * m[2][1] -
                m[0][1] * m[1][0] * m[2][2])
        if det == 0:
            print("Error: La matriz no tiene inversa porque su determinante es cero.")
            return None
        
        adjunta = [[
                m[1][1] * m[2][2] - m[1][2] * m[2][1],
                m[0][2] * m[2][1] - m[0][1] * m[2][2],
                m[0][1] * m[1][2] - m[0][2] * m[1][1]
            ],
            [
                m[1][2] * m[2][0] - m[1][0] * m[2][2],
                m[0][0] * m[2][2] - m[0][2] * m[2][0],
                m[0][2] * m[1][0] - m[0][0] * m[1][2]
            ],
            [
                m[1][0] * m[2][1] - m[1][1] * m[2][0],
                m[0][1] * m[2][0] - m[0][0] * m[2][1],
                m[0][0] * m[1][1] - m[0][1] * m[1][0]
            ]]
        inversa = [[adjunta[i][j] / det for j in range(len(m))] for i in range(len(m))]
        return inversa

    def inversa2x2(self, m):
        if len(m) != len(m[0]):
            print("Error: La matriz no es cuadrada.")
            return None
        det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
        if det == 0:
            print("Error: La matriz no tiene inversa porque su determinante es cero.")
            return None
        inversa = [[m[1][1] / det, -m[0][1] / det], [-m[1][0] / det, m[0][0] / det]]
        return inversa
    
    def inversa(self, m1):
        print(f"inversa({m1})")
        if len(m1) != len(m1[0]):
            raise ValueError("Error: La matriz no es cuadrada.")
        if len(m1) == 2:
            return self.inversa2x2(m1)
        elif len(m1) == 3:
            return self.inversa3x3(m1)
        else:
            raise ValueError("Error: No se puede calcular la inversa.")    

if __name__ == "__main__":
    handler = CalculadoraHandler()
    processor = Calculadora.Processor(handler)
    transport = TSocket.TServerSocket(host="127.0.0.1", port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("Iniciando servidor...")
    server.serve()
    print("Fin")



    