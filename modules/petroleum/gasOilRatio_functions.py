# This script file contains functions of gas/oil ratio correlations
import numpy as np

# gas oil ratio at bubble point pressure
def RsAtPb(P, Pb, T, gammaGas, API,method, c_value):       # Rs (scf/STB), T (Fahrenheit)
    Rs = 0.0
    if P > Pb:      # if pressure is greater than the bubble point pressure
        P = Pb

    if method.upper() == "STANDING":
        Rs = RsStanding(P, T, gammaGas, API)
    elif method.upper() == "VAZQUEZ-BEGGS":
        Rs = RsBeggs_Vazquez(P, T, gammaGas, API)
    elif method.upper() == "GLASO":
        Rs = RsGlaso(P, T, gammaGas, API)
    elif method.upper() == "ALMARHOUN":
        Rs = RsAlMarhoun1988(P, T, gammaGas, API)
    elif method.upper() == "DINDORUK-CHRISTMAN":
        Rs = RsDindoruk_Christman(P, T, gammaGas, API)
    elif method.upper() == "LASATER":
        Rs = RsLasater(P, T, gammaGas, API)
    else:
        print("No such method was found for gas viscosity model.")

    return c_value * Rs       # Rs (scf/STB)

def RsAtPb_cal(P, Pb, T, gammaGas, API,method, Rs_value):       # Rs (scf/STB), T (Fahrenheit)
    Rs = 0.0
    if P > Pb:      # if pressure is greater than the bubble point pressure
        P = Pb

    if method.upper() == "STANDING":
        Rs = RsStanding(P, T, gammaGas, API)
    elif method.upper() == "VAZQUEZ-BEGGS":
        Rs = RsBeggs_Vazquez(P, T, gammaGas, API)
    elif method.upper() == "GLASO":
        Rs = RsGlaso(P, T, gammaGas, API)
    elif method.upper() == "ALMARHOUN":
        Rs = RsAlMarhoun1988(P, T, gammaGas, API)
    elif method.upper() == "DINDORUK-CHRISTMAN":
        Rs = RsDindoruk_Christman(P, T, gammaGas, API)
    elif method.upper() == "LASATER":
        Rs = RsLasater(P, T, gammaGas, API)
    else:
        print("No such method was found for gas viscosity model.")
    c_value = Rs_value / Rs
    return c_value       # Rs (scf/STB)



def RsStanding(P, T, gammaGas, API):     # Standing correlation, P(psi)  , T (Fahrenheit)
    temp = ((1.0 / 18.0) * P) * pow(10.0, 0.0125 * API) / pow(10, 0.00091 * T)
    Rs = gammaGas * pow(temp, 1.0 / 0.83)

    return  Rs  # Rs (scf/STB)

def RsBeggs_Vazquez(P, T, gammaGas, API):   # Vazquez-Beggs correlation, P(psi)  , T (Fahrenheit)
    C1 = 0.0362
    C2 = 1.0937
    C3 = 25.724

    if API > 30.0:
        C1 = 0.0178
        C2 = 1.1870
        C3 = 23.931

    Rs = C1 * gammaGas * pow(P, C2) * np.exp((C3 * API) / (T + 460.0))

    return Rs   # Rs (scf/STB)

def RsGlaso(P, T, gammaGas, API):   # Glaso correlation, P(psi)  , T (Fahrenheit)
    temp1 = (-1.7447 + np.sqrt(3.044 + 1.20872 * (1.7669 - np.log10(P)))) / -0.60436
    temp1 = pow(10, temp1)
    temp2 = pow(T, 0.172) / pow(API, 0.989)
    Rs = gammaGas * pow(temp1 / temp2, 1.0 / 0.816)

    return Rs   # Rs (scf/STB)

def RsAlMarhoun1988(P, T, gammaGas, API):   # Al-Marhoun (1988) middle east oil correlation, P(psi)  , T (Fahrenheit)
    T = T + 460  # Fahrenheit to Rankine
    gammaOil = 141.5 / (API + 131.5)
    a1 = 0.00538088
    a2 = 0.715082
    a3 = -1.877840
    a4 = 3.143700
    a5 = 1.326570

    Rs = pow(P / (a1 * pow(gammaGas, a3) * pow(gammaOil, a4) * pow(T, a5)),1.0/a2)

    return Rs   # Rs (scf/STB)

def RsDindoruk_Christman(P, T, gammaGas, API):  # Dindoruk-Christman correlation, P(psi)  , T (Fahrenheit)
    a1 = 4.86996 * 1e-6
    a2 = 5.730982539
    a3 = 9.92510 * 1e-3
    a4 = 1.776179364
    a5 = 44.25002680
    a6 = 2.702889206
    a7 = 0.744335673
    a8 = 3.359754970
    a9 = 28.10133245
    a10 = 1.579050160
    a11 = 0.928131344
    temp1 = a1 * pow(API, a2) + a3 * pow(T, a4)
    temp2 = (a5 + 2 * pow(API, a6) / pow(P, a7)) * (a5 + 2 * pow(API, a6) / pow(P, a7))
    A = temp1 / temp2
    Rs = pow(((P / a8 + a9) * pow(gammaGas, a10) * pow(10, A)), a11)

    return Rs    # Rs (scf/STB)


def RsLasater(P, T, gammaGas, API): # Lasater correlation, P(psi)  , T (Fahrenheit)
    T = T + 460.0   #   Fahrenheit to Rankine
    gammaOil = 141.5 / (131.5 + API)
    gammaOil = 141.5 / (131.5 + API)
    MwOil = 0.0
    if API <= 40.0:
        MwOil = 630.0 - 10.0 * API
    else:
        MwOil = 73.110 * pow(API, -1.562)
    T = T + 460
    yg = 0.0
    if (P * gammaGas / T) < 3.29:
        yg = 0.359 * np.log(1.473 * P * gammaGas / T + 0.476)
    else:
        yg = pow((0.121 * P * gammaGas / T - 0.236), 0.281)
    Rs = 132755 * gammaOil * yg / (MwOil * (1 - yg))
    return Rs       # Rs (scf/STB)
