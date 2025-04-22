import streamlit as st
import math
import itertools

st.set_page_config(page_title="Confiabilidad K de N", layout="centered")

st.title("Aplicación de Confiabilidad para Sistemas K de N")

st.markdown("""
Este aplicativo permite calcular la **confiabilidad de un sistema K de N**, 
donde el sistema funciona correctamente si al menos **K de N** componentes están operativos.
""")

tasas_input = st.text_input("Ingrese las tasas de falla (λ) separadas por coma", "0.001, 0.002, 0.0015")
k = st.number_input("Ingrese el valor de K (número mínimo de componentes operativos)", min_value=1, step=1, value=2)
t = st.number_input("Ingrese el tiempo de operación (t)", min_value=0.0, step=1.0, value=100.0)

def confiabilidad_individual(lambda_i, t):
    return math.exp(-lambda_i * t)

def confiabilidad_sistema(tasas_falla, k, t):
    n = len(tasas_falla)
    confiabilidad_total = 0

    for i in range(k, n + 1):
        for indices_on in itertools.combinations(range(n), i):
            prob = 1
            for j in range(n):
                if j in indices_on:
                    prob *= confiabilidad_individual(tasas_falla[j], t)
                else:
                    prob *= (1 - confiabilidad_individual(tasas_falla[j], t))
            confiabilidad_total += prob

    return confiabilidad_total

if st.button("Calcular Confiabilidad"):
    try:
        tasas_falla = list(map(float, tasas_input.strip().split(",")))
        if k > len(tasas_falla):
            st.error("El valor de K no puede ser mayor que la cantidad de componentes (N).")
        else:
            resultado = confiabilidad_sistema(tasas_falla, k, t)
            st.success(f"La confiabilidad del sistema es: {resultado:.6f}")
    except Exception as e:
        st.error(f"Error en los datos ingresados: {e}")