def forming_formula(lx, ly, x):
    lx = [i for i in lx if i!=None]
    ly = ly[:len(lx)]
    lx = sum([[lx[i], (lx[i]+lx[i])/2] for i in range(len(lx)-1)], [])+ [lx[-1]]
    ly = sum([[ly[i], (ly[i]+ly[i])/2] for i in range(len(ly)-1)], [])+ [ly[-1]]
    lx = sum([[lx[i], (lx[i]+lx[i])/2] for i in range(len(lx)-1)], [])+ [lx[-1]]
    ly = sum([[ly[i], (ly[i]+ly[i])/2] for i in range(len(ly)-1)], [])+ [ly[-1]]
    lx = sum([[lx[i], (lx[i]+lx[i])/2] for i in range(len(lx)-1)], [])+ [lx[-1]]
    ly = sum([[ly[i], (ly[i]+ly[i])/2] for i in range(len(ly)-1)], [])+ [ly[-1]]
    import numpy as np
    xi = np.array(lx)
    yi = np.array(ly)
    t = np.polyfit(xi, yi, 7)
    formula = ''
    for i in range(len(t)):
        formula+=f"(({t[i]})*(x**{len(t)-i-1}))+"
    formula = formula[:-1]
    import streamlit as st
    st.write(a)
    a = round(eval(formula), 2)
    return a
