# This script file contains functions of oil formation volume factor correlations
import numpy as np
# Oil formation volume factor above the bubble point pressure
def OFVF_func(P, Pb, Rs, T, gammaGas, gammaOil, method, c_value):            # Rs (scf/STB), T (Fahrenheit), P(psi), Pb(psi)
    Bo = 0.0
    if P <= Pb:
        Bo = Bo_bubble(Rs, T, gammaGas, gammaOil, method)
    else:
        Bob = Bo_bubble(Rs, T, gammaGas, gammaOil, method)
        Co = oilCompressibilityVazquez_Beggs(Rs, P, T, gammaGas, gammaOil)
        Bo = Bob * np.exp(Co * (Pb - P))

    return c_value * Bo


# Oil formation volume factor calibration
def OFVF_func_cal(P, Pb, Rs, T, gammaGas, gammaOil, method, Bo_vlaue):            # Rs (scf/STB), T (Fahrenheit), P(psi), Pb(psi)
    Bo = 0.0
    if P <= Pb:
        Bo = Bo_bubble(Rs, T, gammaGas, gammaOil, method)
    else:
        Bob = Bo_bubble(Rs, T, gammaGas, gammaOil, method)
        Co = oilCompressibilityVazquez_Beggs(Rs, P, T, gammaGas, gammaOil)
        Bo = Bob * np.exp(Co * (Pb - P))

    c_value = Bo_vlaue / Bo
    return c_value

# Oil formation volume factor at bubble point pressure

def Bo_bubble(Rs, T, gammaGas, gammaOil, method):   #  Rs (scf/STB), T (Fahrenheit)
    Bob = 0.0
    if method.upper() == "STANDING" :
        Bob = BobStanding(Rs, T, gammaGas, gammaOil)
    elif method.upper() == "VAZQUEZ-BEGGS" :
        Bob = BobVazquez_Beggs(Rs, T, gammaGas, gammaOil)
    elif method.upper() == "GLASO":
        Bob = BobGlaso(Rs, T, gammaGas, gammaOil)
    elif method.upper() == "ALMARHOUN":
        Bob = BobAlMarhoun(Rs, T, gammaGas, gammaOil)
    elif method.upper() == "FARSHAD":
        Bob = BobFarshad(Rs, T, gammaGas, gammaOil)
    elif method.upper() == "DINDORUK-CHRISTMAN":
        Bob = BobDindoruk_Christman(Rs, T, gammaGas, gammaOil)
    else :
        print("No such method was found for gas viscosity model.")

    return  Bob


# Oil formation volume factor at bubble point pressure correlation

def BobStanding(Rs, T, gammaGas, gammaOil):              # Standing correlation,  Rs (scf/STB), T (Fahrenheit)
    A = Rs * np.sqrt(gammaGas / gammaOil) + 1.25 * T
    Bob = 0.9759 + 12 * 1e-5 * pow(A, 1.2)

    return  Bob     # (bbl/STB)

def BobVazquez_Beggs(Rs, T, gammaGas, gammaOil):    # Beggs-Vazquez correlation,  Rs (scf/STB), T (Fahrenheit)
    C1 = 4.677 * 1e-4
    C2 = 1.751*1e-5
    C3 = -1.811 * 1e-8
    API = 141.5 / gammaOil - 131.5
    if API > 30.0:
        C1 = 4.670 * 1e-4
        C2 = 1.100 * 1e-5
        C3 = -1.337 * 1e-9

    Bob = 1.0 + C1 * Rs + C2 * (T - 60.0) * (API / gammaGas) + C3 * Rs * (T - 60.0) * (API / gammaGas)

    return Bob  # (bbl/STB)

def BobGlaso(Rs, T, gammaGas, gammaOil):     # Glaso correlation,  Rs (scf/STB), T (Fahrenheit)
    A = Rs * pow(gammaGas / gammaOil, 0.526) + 0.968 * T
    temp = -6.585 + 2.9133 * np.log10(A) - 0.2768 * np.log10(A) * np.log10(A)
    Bob = pow(10.0, temp) + 1

    return  Bob  # (bbl/STB)

def BobAlMarhoun(Rs, T, gammaGas, gammaOil):     # Al-Marhoun correlation,  Rs (scf/STB), T (Fahrenheit)
    Bob = (1.0 + (0.177342 * 1e-3) * Rs + (0.220163 * 1e-3) * Rs * gammaGas / gammaOil +
    (4.292580 * 1e-6) * Rs * (T - 60.0) * (1.0 - gammaOil) + (0.528707 * 1e-3) * (T - 60.0))

    return Bob   # (bbl/STB)

def BobFarshad(Rs, T, gammaGas, gammaOil):  # Farshad correlation,  Rs (scf/STB), T (Fahrenheit)
    x = pow(Rs, 0.5956) * pow(gammaGas, 0.2369) * pow(gammaOil, -1.3282) + 0.0976 * T
    Bob = 1.0 + pow(10.0, -2.6541 + 0.5576 * np.log10(x) + 0.3331  * np.log10(x) * np.log10(x))

    return  Bob  # (bbl/STB)

def BobDindoruk_Christman(Rs, T, gammaGas, gammaOil):   # Dindoruk-Christman correlation,  Rs (scf/STB), T (Fahrenheit)
    API = 141.5 / gammaOil - 131.5
    a1 = 2.510755
    a2 = -4.852538
    a3 = 1.183500 * 1e+1
    a4 = 1.365428 * 1e+5
    a5 = 2.252880
    a6 = 1.007190 * 1e+1
    a7 = 4.450849 * 1e-1
    a8 = 5.352624
    a9 = -6.309052 * 1e-1
    a10 = 9.000749 * 1e-1
    a11 = 9.871766 * 1e-1
    a12 = 7.865146 * 1e-4
    a13 = 2.689173 * 1e-6
    a14 = 1.100001 * 1e-5
    temp1 = pow(Rs, a1) * pow(gammaGas, a2) / pow(gammaOil, a3) + a4 * pow(T - 60.0, a5) + a6 * Rs
    temp2 = (a8 + 2 * pow(Rs, a9) / pow(gammaGas, a10) * (T - 60.0)) * (a8 + 2 * pow(Rs, a9) / pow(gammaGas, a10) * (T - 60.0))

    A = pow(temp1, a7) / temp2
    Bob = a11 + a12 * A + a13 * A * A + a14 * (T - 60.0) * API / gammaGas

    return Bob  # (bbl/STB)


# Vazquez-Beggs compressibility factor for calculationg oill formation volume factor above bubble point pressure
def oilCompressibilityVazquez_Beggs(Rsb, P, T, gammaGas, gammaOil): # Rs (scf/STB), T (Fahrenheit), P(psi)
    API = 141.5 / gammaOil - 131.5
    Co = 1e-5 * (5 * Rsb + 17.2 * T - 1180.0 * gammaGas + 12.61 * API - 1433.0) / P

    return  Co # C (1.0 / psi)