def forming_formula(lx, ly, x):
    lx = [i for i in lx if i!=None]
    ly = ly[:len(lx)]
    import numpy as np
    xi = np.array(lx)
    yi = np.array(ly)
    t = np.poly1d(np.polyfit(xi, yi, 5))
    a = t(x)
    return a
def findIntersection(fun1,fun2,x0):
    from scipy.optimize import fsolve
    return fsolve(lambda x : fun1(x) - fun2(x),x0)
def f(x1, y1, x):
    return (y1/(x1**2))*x**2
def anti_f(x1, y1, y):
    return (((x1**2)/y1)*y)**.5
def kpd_find(lx, ly, xi, yi):
    import numpy as np
    
    lx = [i for i in lx if not i is None]
    ly = [ly[li] for li in range(len(lx))]
    rng = np.arange(min(lx), max(lx), 10)
    t = np.poly1d(np.polyfit(lx, ly, 5))
    kt = np.poly1d(np.polyfit([0, xi], [0, yi], 2))
    result = []
    for j in rng:
        result.append(int(findIntersection(t, kt, j)))
    result = set(result)
    cx = min(list(result))
    cy = int(f(xi, yi, cx))
    return [cx, cy]
