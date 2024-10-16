/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "calculadora.h"
#include <math.h>
#define M_PI 3.14159265358979323846

/* Funciones básicas */

resultado *
suma_1_svc(double arg1, double arg2,  struct svc_req *rqstp) {
	static resultado  result;
	result.resultado_u.resultado = (arg1 + arg2);
	return &result;
}

resultado *
resta_1_svc(double arg1, double arg2,  struct svc_req *rqstp) {
	static resultado  result;
	result.resultado_u.resultado = (arg1 - arg2);
	return &result;
}

resultado *
multiplicacion_1_svc(double arg1, double arg2,  struct svc_req *rqstp) {
	static resultado  result;
	result.resultado_u.resultado = (arg1 * arg2);
	return &result;
}

resultado *
division_1_svc(double arg1, double arg2,  struct svc_req *rqstp) {
	static resultado  result;	
	result.resultado_u.resultado = (arg1 / arg2);
	return &result;
}

resultado *
potencia_1_svc(double arg1, double arg2,  struct svc_req *rqstp) {
	static resultado  result;
	result.resultado_u.resultado = pow(arg1, arg2);
	return &result;
}

double log_base_x(double x, double y) { return log(y) / log(x); }

resultado *
logaritmo_1_svc(double arg1, double arg2,  struct svc_req *rqstp) {
	static resultado  result;
	result.resultado_u.resultado = log_base_x(arg1, arg2);
	return &result;
}

double raiz_exponente_x(double base, double exponente) { return pow(base, 1/exponente); }

resultado *
raiz_1_svc(double arg1, double arg2,  struct svc_req *rqstp) {
	static resultado  result;
	result.resultado_u.resultado = raiz_exponente_x(arg1, arg2);
	return &result;
}

/* Funciones vectores */

vect *
suma_vectores_2_svc(vect arg1, vect arg2,  struct svc_req *rqstp) {
	static vect  result;
	result.vect_len = arg1.vect_len;
    result.vect_val = (double *)malloc(arg1.vect_len * sizeof(double));
    if (result.vect_val == NULL) {
        printf("Error: no se pudo asignar memoria para el vector.\n");
        exit(1);
    }

    for (unsigned int i = 0; i < arg1.vect_len; i++) {
        result.vect_val[i] = arg1.vect_val[i] + arg2.vect_val[i];
    }
	return &result;
}

vect *
resta_vectores_2_svc(vect arg1, vect arg2,  struct svc_req *rqstp)
{
	static vect  result;
	result.vect_len = arg1.vect_len;
    result.vect_val = (double *)malloc(arg1.vect_len * sizeof(double));
    if (result.vect_val == NULL) {
        printf("Error: no se pudo asignar memoria para el vector.\n");
        exit(1);
    }

    for (unsigned int i = 0; i < arg1.vect_len; i++) {
        result.vect_val[i] = arg1.vect_val[i] - arg2.vect_val[i];
    }
	return &result;
}

// Función para calcular el producto escalar de dos vectores
double prod_escalar(vect v1, vect v2) {
    double resultado = 0.0;
    for (unsigned int i = 0; i < v1.vect_len; i++) {
        resultado += v1.vect_val[i] * v2.vect_val[i];
    }
    return resultado;
}

resultado *
producto_escalar_2_svc(vect arg1, vect arg2,  struct svc_req *rqstp)
{
	static resultado  result;
    result.resultado_u.resultado = prod_escalar(arg1, arg2);
	return &result;
}

// Función para calcular el producto vectorial de dos vectores
vect prod_vectorial(vect v1, vect v2) {
    static vect  resultado;
    resultado.vect_len = 3;
    resultado.vect_val = (double *)malloc(3 * sizeof(double));
    if (resultado.vect_val == NULL) {
        printf("Error: No se pudo asignar memoria para el vector.\n");
        exit(1);
    }
    resultado.vect_val[0] = v1.vect_val[1] * v2.vect_val[2] - v1.vect_val[2] * v2.vect_val[1];
    resultado.vect_val[1] = v1.vect_val[2] * v2.vect_val[0] - v1.vect_val[0] * v2.vect_val[2];
    resultado.vect_val[2] = v1.vect_val[0] * v2.vect_val[1] - v1.vect_val[1] * v2.vect_val[0];
	return resultado;
}

vect *
producto_vectorial_2_svc(vect arg1, vect arg2,  struct svc_req *rqstp)
{
	static vect  result;
    result = prod_vectorial(arg1, arg2);
	return &result;
}

// Función para calcular la norma de un vector
double norma_vect(vect v) {
    double suma_cuadrados = 0.0;
    for (unsigned int i = 0; i < v.vect_len; i++) {
        suma_cuadrados += v.vect_val[i] * v.vect_val[i];
    }
    double resultado = sqrt(suma_cuadrados);

    return resultado;
}

resultado *
norma_2_svc(vect arg1,  struct svc_req *rqstp)
{
	static resultado  result;
	result.resultado_u.resultado = norma_vect(arg1);
	return &result;
}

// Función para calcular el ángulo entre dos vectores en radianes
double angulo_vect(vect v1, vect v2) {
    double producto = prod_escalar(v1, v2);
    double n_v1 = norma_vect(v1);
    double n_v2 = norma_vect(v2);
    double coseno_angulo = producto / (n_v1 * n_v2);
    double angulo_radianes = acos(coseno_angulo);
    return (angulo_radianes * (180.0 / M_PI));
}

resultado *
angulo_vectores_2_svc(vect arg1, vect arg2,  struct svc_req *rqstp)
{
	static resultado  result;
	result.resultado_u.resultado = angulo_vect(arg1, arg2);
	return &result;
}

// Función para las componentes ortogonales de un vector v1 respecto v2
vect comp_ortog(vect v1, vect v2) {
    // Producto escalar
    double producto = prod_escalar(v1, v2);
    // Norma de v2 ^ 2
    double norma_cuadrado_v2 = norma_vect(v2) * norma_vect(v2);
    // Proyección ortogonal de v1 sobre v2
    vect proyeccion_ortogonal;
    proyeccion_ortogonal.vect_len = v1.vect_len;
    proyeccion_ortogonal.vect_val = (double *)malloc(v1.vect_len * sizeof(double));
    if (proyeccion_ortogonal.vect_val == NULL) {
        printf("Error: No se pudo asignar memoria para el vector.\n");
        exit(1);
    }
    for (unsigned int i = 0; i < v1.vect_len; i++)
        proyeccion_ortogonal.vect_val[i] = (producto / norma_cuadrado_v2) * v2.vect_val[i];

    // Calcular las componentes ortogonales de v1 respecto a v2
    vect componentes_ortogonales;
    componentes_ortogonales.vect_len = v1.vect_len;
    componentes_ortogonales.vect_val = (double *)malloc(v1.vect_len * sizeof(double));
    if (componentes_ortogonales.vect_val == NULL) {
        printf("Error: No se pudo asignar memoria para el vector.\n");
        exit(1);
    }
    for (unsigned int i = 0; i < v1.vect_len; i++) 
        componentes_ortogonales.vect_val[i] = v1.vect_val[i] - proyeccion_ortogonal.vect_val[i];

    free(proyeccion_ortogonal.vect_val);

    return componentes_ortogonales;
}

vect *
comp_ortogonales_2_svc(vect arg1, vect arg2,  struct svc_req *rqstp)
{
	static vect result;
	result = comp_ortog(arg1, arg2);
	return &result;
}

// Función para calcular el producto mixto de tres vectores
double prod_mixto(vect v1, vect v2, vect v3) {
    vect producto_v2v3 = prod_vectorial(v2, v3);
    double resultado = prod_escalar(v1, producto_v2v3);
    free(producto_v2v3.vect_val);
    return resultado;
}

resultado *
producto_mixto_2_svc(vect arg1, vect arg2, vect arg3,  struct svc_req *rqstp) {
	static resultado result;
	result.resultado_u.resultado = prod_mixto(arg1, arg2, arg3);
	return &result;
}
