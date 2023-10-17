def forming_formula(lx, ly, x):
    lx = [i for i in lx if i!=None]
    ly = ly[:len(lx)]
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
def kpd_find(lx, ly, xi, yi):
    import numpy as np
    t = np.poly1d(np.polyfit(lx, ly, 5))
    cx = xi
    cy = f(xi, yi, cx)
    ny = t(cx)
    eps = 10**10
    while eps>1:
        cy = f(xi, yi, cx)
        ny = t(cx)
        my = cy + ((ny - cy) / 2)
        cx = anti_f(xi, yi, my)
        eps = ((f(xi, yi, cx) - t(cx))**2)**.5
    cx = int(round(cx, 0))
    cy = f(xi, yi, cx)
    return [cx, cy]
