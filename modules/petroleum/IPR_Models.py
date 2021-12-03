import numpy as np
import matplotlib.pyplot as plt

def IPRMODELS_func(Pave, Pb, J, method, fw): # Pave (psi), Pb (psi), J (STB/psi), fw (fraction)
    if method.upper() == "VOGEL":
        [Qoil, Pwf_array, Ql, Qw] = IPR_Vogel(Pave, Pb, J)
    elif method.upper() == "MODIFIEDVOGEL":
        [Qoil, Pwf_array, Ql, Qw] = IPR_Vogel_modified(Pave,Pb, J, fw)
    else:
        print("Wring method for IPR.")
        exit()
    return [Qoil, Pwf_array, Ql, Qw]   # Qoil (STB/day), Pwf_array (psi), Ql (STB/day), Qw (STB/day)






def IPR_Vogel(Pave,Pb, J):  # Pave (psi), Pb (psi), J (STB/psi)
    Pwf_array = np.arange(start=0, stop=Pave + 0.1, step=0.1)
    Qoil = np.zeros(Pwf_array.size)

    Qmax = J * Pave

    if Pave <  Pb:
        for i in range(0, Pwf_array.size):
            Qoil[i] = Qmax * (1.0 - 0.2 * (Pwf_array[i]/Pave) - 0.8 * (Pwf_array[i]/Pave) * (Pwf_array[i]/Pave))
    else:
        Qob = J * (Pave - Pb)
        for i in range(0, Pwf_array.size):
            if Pwf_array[i] >= Pb:
                Qoil[i] = J * (Pave - Pwf_array[i])

            else:
                Qoil[i] = Qob + J * Pb / 1.8 * (1.0 - 0.2 * (Pwf_array[i] / Pb) - 0.8 * (Pwf_array[i] / Pb) * (Pwf_array[i] / Pb))



    Ql = np.zeros(Pwf_array.size)
    Qw = np.zeros(Pwf_array.size)
    return [Qoil, Pwf_array, Ql, Qw]   # Qoil (STB/day), Pwf_array (psi), Ql (STB/day), Qw (STB/day)


def IPR_Vogel_modified(Pave,Pb, J, fw):



    Qb = J * (Pave - Pb)
    Qomax = Qb + J * Pb / 1.8
    term1 = fw * 0.001 * Qomax / J
    term2 = 0.125 * (1.0 - fw) * Pb * (-1.0 + np.sqrt(81.0 - (80.0 * (0.999 * Qomax - Qb)/ (Qomax - Qb))))
    slope = (term1 + term2) / (0.001 * Qomax)
    Qlmax = Qomax + (1.0 - fw) * (Pave - Qomax/J) / slope
    Ql = np.arange(start=0, stop=Qlmax + 0.1, step=0.5)
    Pwf_array = np.zeros(Ql.size)
    for i in range(0, Ql.size):
        if (Ql[i] <  Qb) or (fw == 100):
            Pwf_array[i] = Pave - Ql[i] / J
        elif (fw < 100) and (Ql[i] < Qomax):
            term1 = fw * (Pave - Ql[i] / J)
            term2 = 0.125 * (1.0 - fw) * Pb * (-1.0 + np.sqrt((81.0 - 80.0 * (Ql[i] - Qb) / (Qomax - Qb))))
            if (81.0 - 80.0 * (Ql[i] - Qb) / (Qomax - Qb)) < 0:
                print("stop")

            Pwf_array[i] = term1 + term2
        elif (fw < 100) and (Ql[i] > Qomax):
            Pwf_array[i] = fw * (Pave - Qomax / J) - (Ql[i] - Qomax) * slope

    Qoil = np.zeros(Ql.size)
    Qw = np.zeros(Ql.size)
    for i in range(0, Ql.size):
        Qoil[i] = (1.0 - fw) * Ql[i]
        Qw[i] = fw * Ql[i]

    return [Qoil, Pwf_array, Ql, Qw]   # Qoil (STB/day), Pwf_array (psi), Ql (STB/day), Qw (STB/day)