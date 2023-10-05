from parameters_vkop import *
def draw_plot(vkop, zQ, zp):
    from re import findall
    kluch = findall(r"-(\d\d\d-)", vkop)[0]+'Н'+findall(r"(-\d\d\d\d\d/\d)-", vkop)[0]
    import matplotlib.pyplot as plt
    import numpy as np
    from io import BytesIO
    Qs = [item for item in df[kluch] if type(item)==float or type(item)==int]
    list_pk = [list_p[i] for i in range(len(Qs))]
    s = np.array(Qs)
    cht = np.array(list_pk)
    plt.scatter(s, cht, linewidth= 3, color="#26822F")
    plt.plot(s, cht, linewidth=4, color="#26822F")
    plt.scatter(np.array(zQ), np.array(zp-7), color="#FF642B", linewidths=4)
    plt.grid(True)
    plt.xlabel('Расход воздуха, м³/ч')
    plt.ylabel('Статическое давление, Па')
    memfile = BytesIO()
    plt.savefig(memfile)
    return memfile
