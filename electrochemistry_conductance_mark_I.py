# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 12:52:44 2021

@author: juric
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, b, c, d, e):
    return a * np.exp(- x / b) + c * np.exp(- x / d) + e

st.title("Electrochemistry - Conductance - Mark I")

voltage = st.number_input("Voltage [V]:", value = 1.0)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read the measurements excel file 
    df = pd.pandas.read_excel(uploaded_file)

    measurements = df.to_numpy()
    time = measurements[:,1]
    current = measurements[:,3]

    # plot the measurements
    fig, ax = plt.subplots()
    ax.plot(time, current*1e9, 'b^', label="Measurements")
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Current [nA]')
    ax.grid()

    # determine the curve
    popt, pcov = curve_fit(func, time, current, p0 = [1e-9, 1, 1e-9, 100, 1e-9], bounds=([1e-9, 1, 1e-9, 1, 1e-9],[1e-7, 1000, 1e-7, 1000, 1e-7]), method='dogbox')

    ax.plot(time, func(time, *popt)*1e9, 'r--', label="Fitted Curve")


    st.pyplot(fig)

    # Write the fitting parameters
    #st.latex(st.latex(r'''I(t) = \Delta I \cdot e^{-\frac{t}{\tau}} + I_{DC}'''))

    st.text('Fitted the equation: I(t) = Delta_I_1 exp(-t/tau_1) + Delta_I_2 exp(-t/tau_2) + I_DC')
    st.text('Fitted parameters:')
    st.text(f'Delta_I_1: {popt[0]*1e9:.2f} nA')
    st.text(f'tau_1: {popt[1]:.2f} s')
    st.text(f'Delta_I_2: {popt[2]*1e9:.2f} nA')
    st.text(f'tau_2: {popt[3]:.2f} s')
    st.text(f'I_DC: {popt[4]*1e9:.2f} nA')

    # Calculatea and write conductance
    st.text('Finally, resistance and conductance are:')
    st.markdown(f'__Resistance:__ R = {voltage/popt[4]:.4e} Ohm')
    st.markdown(f'__Conductance:__ G = {popt[4]/voltage:.4e} S')