from parameters_vkop import *
from interpolate import forming_formula as ff
def vkop_list(p, Q):
    variants = [[key, Q, ff(df[key], list_p, Q)] for key in df.keys() if 0.8<=(ff(df[key], list_p, Q)/p)**(-1)<=1.05 and 75<=ff(df[key], list_p, Q)<=950]
    return variants
