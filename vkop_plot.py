from parameters_vkop import *
from interpolate import forming_formula as ff
from interpolate import f, kpd_find, anti_f
import time
from io import BytesIO
def draw_plot(vkop, zQ, zp):
    memfile = BytesIO()
    time.sleep(0.01)
    from re import findall
    kluch = findall(r"-(\d\d\d-)", vkop)[0]+'Н'+findall(r"(-\d\d\d\d\d/\d)-", vkop)[0]
    import matplotlib.pyplot as plt
    import numpy as np
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
    dot = kpd_find(Qs, list_pk, zQ, zp)
    # kpd_p = [k for k in kpd_p if dot[1]-150<=k<=dot[1]+150 and dot[0]-5000<=anti_f(zQ, zp, k)<=dot[0]+5000]
    # Qsn = [anti_f(zQ, zp, i) for i in kpd_p]
    Qsn = [-dot[0], -zQ, 0, zQ, dot[0]]
    kpd_p = [dot[1],zp,0, zp, dot[1]]
    pol_kpd = np.poly1d(np.ployfit(Qsn, kpd_p, 2))
    ab_d  = ((zQ-dot[0])**2)**.5
    pQsn = [zQ-ab_d, zQ, dot[0], dot[0] + ab_d]
    pkpd_p = [pol_kpd(qwe) for qwe in p_Qsn]
    # dot = kpd_find(Qs, list_pk, zQ, zp)
    plt.plot(np.array(pQsn), np.array(pkpd_p), linewidth=1, color="#48B454")
    plt.scatter([dot[0]], [dot[1]], linewidth=4, color="#48B454")
    plt.scatter(np.array(zQ), np.array(zp), color="#FF642B", linewidths=4)
    plt.grid(True)
    plt.xlabel('Расход воздуха, м³/ч')
    plt.ylabel('Статическое давление, Па')
    plt.ylim(0, max(list_pk)+20)
    plt.savefig(memfile)
    return memfile
