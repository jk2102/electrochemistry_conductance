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

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

st.title("Electrochemistry - Conductance - Mark I")

voltage = st.number_input("Voltage [V]:", value = 1.0)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read the measurements excel file 
    df = pd.pandas.read_excel(uploaded_file)

    measurements = df.to_numpy()
    time = measurements[:,0]
    current = measurements[:,1]

    # plot the measurements
    fig, ax = plt.subplots()
    ax.plot(time, current*1e9, 'b^', label="Measurements")
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Current [nA]')
    ax.grid()

    # determine the curve
    popt, pcov = curve_fit(func, time, current)

    ax.plot(time, func(time, *popt)*1e9, 'r--', label="Fitted Curve")


    st.pyplot(fig)

    # Write the fitting parameters
    #st.latex(st.latex(r'''I(t) = \Delta I \cdot e^{-\frac{t}{\tau}} + I_{DC}'''))

    st.text('Fitted the equation: I(t) = Delta_I exp(-t/tau) + I_DC')
    st.text('Fitted parameters:')
    st.text(f'Delta_I: {popt[0]*1e9:.2f} nA')
    st.text(f'tau: {1/popt[1]:.2f} s')
    st.text(f'I_DC: {popt[2]*1e9:.2f} nA')

    # Calculatea and write conductance
    st.text('Finally, resistance and conductance are:')
    st.markdown(f'__Resistance:__ R = {voltage/popt[2]:.4e} Ohm')
    st.markdown(f'__Conductance:__ G = {popt[2]/voltage:.4e} S')