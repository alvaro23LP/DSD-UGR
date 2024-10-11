union resultado switch(int errno){
	case 0:
		double resultado; /* Devuelve el resultado correctamente */
	default:
		void; /* error */
};

typedef double vect<>;

program CALCULADORA {
	version CALCULADORA_BASICA {
		resultado suma (double, double) = 1;
		resultado resta (double, double) = 2;
		resultado multiplicacion (double, double) = 3;
		resultado division (double, double) = 4;
		resultado potencia (double, double) = 5;
		resultado logaritmo (double, double) = 6;
		resultado raiz (double, double) = 7;
	} = 1;

	version CALCULADORA_vect {
		vect suma_vectores (vect, vect) = 1;
		vect resta_vectores (vect, vect) = 2;
		resultado producto_escalar (vect, vect) = 3;
		vect producto_vectorial (vect, vect) = 4;
		resultado norma (vect) = 5;
		resultado angulo_vectores (vect, vect) = 6;
		vect comp_ortogonales (vect, vect) = 7;
		resultado producto_mixto (vect, vect, vect) = 8;
	} = 2;
} = 0x20001123;
