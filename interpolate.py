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
    t = np.poly1d(np.polyfit(xi, yi, 3))
    a = t(x)
    return a
