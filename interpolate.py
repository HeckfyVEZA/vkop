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
    t = np.poly1d(np.polyfit(xi, yi, 5))
    a = t(x)
    return a
def f(x1, y1, x):
    return (y1/(x1**2))*x**2
def anti_f(x1, y1, y):
    return (((x1**2)/y1)*y)**.5
def kpd_find(rx, ry, xi, yi):
    import numpy as np
    t = np.poly1d(np.polyfit(rx, ry, 5))
    cx = xi
    cy = f(xi, yi, cx)
    ny = t(cx)
    eps = 10
    while eps>0.1:
        cy = f(xi, yi, cx)
        ny = t(cx)
        my = cy + ((ny - cy) / 2)
        cx = anti_f(xi, yi, my)
        eps = ((f(xi, yi, cx) - t(cx))**2)**.5
    cx = int(round(cx, 0))
    cy = f(xi, yi, cx)
    return [cx, cy]
