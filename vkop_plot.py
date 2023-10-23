from parameters_vkop import *
from interpolate import forming_formula as ff
from interpolate import f, kpd_find, anti_f
import time
def draw_plot(vkop, zQ, zp):
    time.sleep(.02)
    from re import findall
    kluch = findall(r"-(\d\d\d-)", vkop)[0]+'Н'+findall(r"(-\d\d\d\d\d/\d)-", vkop)[0]
    import matplotlib.pyplot as plt
    import numpy as np
    from io import BytesIO
    Qs = [item for item in df[kluch] if type(item)==float or type(item)==int]
    list_pk = [list_p[i] for i in range(len(Qs))]
    Qq = Qs[:]
    Qq = np.array(Qq)
    ip = np.array([ff(Qs, list_pk, i) for i in Qq])
    s = np.array(Qs)
    cht = np.array(list_pk)
    # plt.scatter(s, cht, linewidth= 3, color="#26822F")
    plt.plot(Qq, ip, linewidth=4, color="#26822F")
    Qse = sum([[Qs[i], (Qs[i]+Qs[i])/2] for i in range(len(Qs)-1)], [])+ [Qs[-1]]
    kpd_p = [f(zQ, zp, i) for i in Qse]
    kpd_p = [k for k in kpd_p if k<=900]
    Qsn = [anti_f(zQ, zp, i) for i in kpd_p]
    dot = kpd_find(Qs, list_pk, zQ, zp)
    plt.plot(np.array(Qsn), np.array(kpd_p), linewidth=1, color="#48B454")
    plt.scatter([dot[0]], [dot[1]], linewidth=4, color="#48B454")
    plt.scatter(np.array(zQ), np.array(zp), color="#FF642B", linewidths=4)
    plt.grid(True)
    plt.xlabel('Расход воздуха, м³/ч')
    plt.ylabel('Статическое давление, Па')
    plt.ylim(min(Qs), max(Qs))
    memfile = BytesIO()
    plt.savefig(memfile)
    return memfile
