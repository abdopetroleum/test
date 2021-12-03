# This script file contains functions of bubble point pressure correlations
import numpy as np


def bubblePoint_func(Rs, T, gammaGas, API,method):  # Rs (scf/STB), T (Fahrenheit)
    Pb = 0.0
    if method.upper() == "STANDING":
        Pb = PbStanding(Rs, T, gammaGas, API)
    elif method.upper() == "VAZQUEZ-BEGGS":
        Pb = PbBeggs_Vazquez(Rs, T, gammaGas, API)
    elif method.upper() == "GLASO":
        Pb = PbGlaso(Rs, T, gammaGas, API)
    elif method.upper() == "ALMARHOUN":
        Pb = PbAlMarhoun1988(Rs, T, gammaGas, API)
    elif method.upper() == "FARSHAD":
        Pb = PbFarshad(Rs, T, gammaGas, API)
    elif method.upper() == "DINDORUK-CHRISTMAN":
        Pb = PbDindoruk_Christman(Rs, T, gammaGas, API)
    elif method.upper() == "PETROSKY FARSHAD":
        Pb = PbPetroskyFarshad(Rs, T, gammaGas, API)
    elif method.upper() == "LASATER":
        Pb = PbLasater(Rs, T, gammaGas, API)
    else:
        print("No such method was found for gas viscosity model.")

    return Pb   # P(psi)

# def bubblePoint_func(Rs, T, gammaGas, API,method, value):  # Rs (scf/STB), T (Fahrenheit)
#     Pb = 0.0
#     if method.upper() == "STANDING":
#         Pb = PbStanding(Rs, T, gammaGas, API)
#     elif method.upper() == "VAZQUEZ-BEGGS":
#         Pb = PbBeggs_Vazquez(Rs, T, gammaGas, API)
#     elif method.upper() == "GLASO":
#         Pb = PbGlaso(Rs, T, gammaGas, API)
#     elif method.upper() == "ALMARHOUN":
#         Pb = PbAlMarhoun1988(Rs, T, gammaGas, API)
#     elif method.upper() == "FARSHAD":
#         Pb = PbFarshad(Rs, T, gammaGas, API)
#     elif method.upper() == "DINDORUK-CHRISTMAN":
#         Pb = PbDindoruk_Christman(Rs, T, gammaGas, API)
#     elif method.upper() == "PETROSKY FARSHAD":
#         Pb = PbPetroskyFarshad(Rs, T, gammaGas, API)
#     elif method.upper() == "LASATER":
#         Pb = PbLasater(Rs, T, gammaGas, API)
#     else:
#         print("No such method was found for gas viscosity model.")
#     c_ = value / Pb
#     return c_   # P(psi)

def PbStanding(Rs, T, gammaGas, API):   # Standing correlation,  Rs (scf/STB), T (Fahrenheit)
    A = pow((Rs / gammaGas), 0.83) * pow(10.0, 0.00091 * T - 0.0125 * API)
    Pb = 18.2 * (A - 1.4)
    return Pb   # P(psi)

def PbLasater(Rs, T, gammaGas, API):     # Lasater correlation,  Rs (scf/STB), T (Fahrenheit)
    T = T + 460     #   Fahrenheit to Rankine
    gammaOil = 141.5 / (131.5 + API)
    MwOil = 0.0
    if API <= 40.0 :
        MwOil = 630.0 - 10.0 * API
    else :
        MwOil = 73.110 * pow(API, -1.562)

    yg = (Rs / 379.3) / (Rs / 379.3 + 350 * gammaOil / MwOil)

    if yg <= 0.6 :
        A = (0.679 * np.exp(2.786 * yg) - 0.323)
    else :
        A = 8.26 * pow(yg, 3.56) + 1.95

    Pb = (T / gammaGas) * A

    return Pb   # P(psi)


def PbGlaso(Rs, T, gammaGas, API):      # Glaso correlation,  Rs (scf/STB), T (Fahrenheit)
    A = pow(Rs / gammaGas, 0.816) * (pow(T, 0.172) / pow(API, 0.989))
    temp = 1.7669 + 1.7447 * np.log10(A) - 0.30218 * np.log10(A) * np.log10(A)
    Pb = pow(10, temp)

    return  Pb  # P(psi)

def PbBeggs_Vazquez(Rs, T, gammaGas, API):  # Beggs-Vazquez correlation,  Rs (scf/STB), T (Fahrenheit)
    Pb = 0.0
    if API <= 10.0 :
        C1 = 0.0362
        C2 = 1.0937
        C3 = 25.724
        temp = Rs / (C1 * gammaGas * np.exp(C3 * (API / (T + 459.67))))
        Pb = pow(temp, 1 / C2)
    else :
        C1 = 0.0178
        C2 = 1.1870
        C3 = 23.9310
        temp = Rs / (C1 * gammaGas * np.exp(C3 * (API / (T + 459.67))))
        Pb = pow(temp, 1 / C2)

    return Pb   # P(psi)

def PbDindoruk_Christman(Rs, T, gammaGas, API): # Dindoruk-Christman correlation,  Rs (scf/STB), T (Fahrenheit)
    a1 = 1.42828 * 1e-10
    a2 = 2.844591797
    a3 = -6.74896 * 1e-4
    a4 = 1.225226436
    a5 = 0.033383304
    a6 = -0.272945957
    a7 = -0.084226069
    a8 = 1.869979257
    a9 = 1.221486524
    a10 = 1.370508349
    a11 = 0.011688308
    temp1 = a1 * pow(T, a2) + a3 * pow(API, a4)
    temp2 = (a5 + 2 * pow(Rs, a6) / pow(gammaGas, a7)) * (a5 + 2 * pow(Rs, a6) / pow(gammaGas, a7))
    A = temp1 / temp2
    Pb = a8 * ((pow(Rs, a9) / pow(gammaGas, a10)) * pow(10, A) + a11)

    return  Pb  # P(psi)

def PbFarshad(Rs, T, gammaGas, API):    # Farshad correlation,  Rs (scf/STB), T (Fahrenheit)
    A = pow(gammaGas, -1.378) * pow(Rs, 1.053) * pow(10.0, 0.00069 * T - 0.0208 * API)
    Pb = pow(10.0, 0.3058 + 1.9013 * np.log10(A) - 0.26* np.log10(A)* np.log10(A))

    return  Pb  # P(psi)

def PbAlMarhoun1988(Rs, T, gammaGas, API):  # Al-Marhoun (1988) middle east oil correlation,  Rs (scf/STB), T (Fahrenheit)
    T = T + 460         # Fahrenheit to Rankine
    gammaOil = 141.5/(API + 131.5)
    a1 = 0.00538088
    a2 = 0.715082
    a3 = -1.877840
    a4 = 3.143700
    a5 = 1.326570

    Pb = a1 * pow(Rs, a2) * pow(gammaGas, a3) * pow(gammaOil, a4) * pow(T, a5)

    return Pb   # P(psi)

def PbPetroskyFarshad(Rs, T, gammaGas, API):    # Petrosky-Farshad correlation,  Rs (scf/STB), T (Fahrenheit)
    x = 0.0007916 * pow(API, 1.541) - 0.00004561 * pow(T, 1.3911)
    Pb = (112.727 * pow(Rs, 0.577421) / (pow(gammaGas, 0.8439) * pow(10.0, x))) - 1391.051

    return  Pb  # P(psi)



