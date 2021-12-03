# This script file contains functions of dead oil, saturated oil, and undersaturated oil correlations
import numpy as np

# oil viscosity calibration
def oilViscosity_func_cal(Pb, P, T, API, Rs, method1, method2, method3, muo_value):

    muDeadOil =  deadOilViscosity_func(T, P, API, Rs, method1)
    c_val = 1;
    mu =  satOilViscosity_func(muDeadOil, Rs, method2, P, Pb, API, c_val)

    c_value = muo_value/mu
    return c_value

def oilViscosity_func(Pb, P, T, API, Rs, method1, method2, method3, c_value):
    mu = 0.0
    if P <= Pb:
       muDeadOil =  deadOilViscosity_func(T, P, API, Rs, method1)
       mu =  satOilViscosity_func(muDeadOil, Rs, method2, P, Pb, API, c_value)
    else:
        muDeadOil = deadOilViscosity_func(T, P, API, Rs, method1)
        muSat = satOilViscosity_func(muDeadOil, Rs, method2, P, Pb, API, c_value)
        mu = underSatOilViscosity_func(muSat, muDeadOil, P, Pb, Rs, API, method3)

    return mu

# dead oil viscosity functions
def deadOilViscosity_func(T, P, API, Rs, method1):
    muDeadOil = 0.0
    if method1.upper() == "BEAL-STANDING":
        muDeadOil =  muDeadBeal_Standing(T, API)
    elif method1.upper() == "PETROSKY":
        muDeadOil =  muDeadPetrosky(T, API)
    elif method1.upper() == "GLASO":
        muDeadOil =  muDeadGlaso(T, API)
    elif method1.upper() == "LABEDI":
        muDeadOil =  muDeadLabedi(T, API)
    elif method1.upper() == "BEGGS-ROBINSON":
        muDeadOil =  muDeadBeggs_Robinson(T, API)
    elif method1.upper() == "BERGMAN":
        muDeadOil =  muDeadBergman(T, API)
    elif method1.upper() == "DINDORUK-CHRISTMAN":
        muDeadOil =  muDeadDindoruk_Christman(T, P, API, Rs)
    elif method1.upper() == "ALkHAFAJI":
        muDeadOil = muDeadAlKhafaji(T, API)
    elif method1.upper() == "STANDING":
        muDeadOil = muDeadAlKhafaji(T, API)
    else:
        print("No such method was found for dead oil viscosity model.")

    return muDeadOil

# saturated oil viscosity functions P <= Pb
def satOilViscosity_func(muDeadOil, Rs, method2, P, Pb, API, c_value):
    muSat = 0.0
    if method2.upper() == "PETROSKY":
        muSat = muSatPetrosky(muDeadOil, Rs)
    elif method2.upper() == "LABEDI":
        muSat = muSatLabedi(muDeadOil, Pb, API)
    elif method2.upper() == "BEGGS-ROBINSON":
        muSat =  muSatBeggs_Robinson(muDeadOil, Rs)
    elif method2.upper() == "BERGMAN":
        muSat = muSatBergman(muDeadOil, Rs)
    elif method2.upper() == "AZIZ":
        muSat = muSatAziz(muDeadOil, Rs)
    elif method2.upper() == "ALkHAFAJI":
        muSat = muSatAlKhafaji(muDeadOil, Rs)
    elif method2.upper() == "DINDORUK-CHRISTMAN":
        muSat = muSatDindoruk_Christman(muDeadOil, Rs)
    elif method2.upper() == "STANDING":
        muSat = muSatStanding(muDeadOil, Rs)
    else:
        print("No such method was found for saturated oil viscosity model.")

    return  c_value * muSat

# undersaturated oil viscosity functions P > Pb
def underSatOilViscosity_func(muSat, muDeadOil, P, Pb, Rs, API, method3):
    muUnderSat = 0.0
    if method3.upper() == "BEAL-STANDING":
        muUnderSat =  muUnderSatBeal_Standing(muSat, P, Pb)
    elif method3.upper() == "PETROSKY":
        muUnderSat =  muUnderSatPetrosky(muSat, P, Pb)
    elif method3.upper() == "LABEDI":
        muUnderSat =  muUnderSatLabedi(muSat, muDeadOil, P, Pb, API)
    elif method3.upper() == "BEGGS-ROBINSON":
        muUnderSatBeggs_Robinson(muSat, muDeadOil, P, Pb)
    elif method3.upper() == "BERGMAN":
        muUnderSatBergman(muSat, muDeadOil, P, Pb)
    elif method3.upper() == "DINDORUK-CHRISTMAN":
        muUnderSatDindoruk_Christman(muSat, muDeadOil, P, Pb, Rs)
    elif method3.upper() == "ALkHAFAJI":
        muUnderSatAlKhafaji(muSat, muDeadOil, P, Pb, API)
    else:
        print("No such method was found for under saturated oil viscosity model.")

    return muUnderSat

# Dead oil viscosity correlations
def muDeadBeal_Standing(T, API):    # T (Fahrenheit)
    A = pow(10.0, 0.43 + (8.33 / API))
    muDeadOil = (0.32 + (1.8 * 1e+7) / pow(API, 4.53)) * pow(360.0 / (T + 200.0), A)

    return muDeadOil    # viscosity (cP)

def muDeadPetrosky(T, API): # T (Fahrenheit)
    J = 4.59388 * np.log10(T) - 22.82792
    muDeadOil = 2.3511 * 1e+7 * pow(T, -2.10255) * J * np.log10(API)

    return  muDeadOil    # viscosity (cP)

def muDeadGlaso(T, API):    # T (Fahrenheit)
    A = pow(10.0, 0.43 + (8.33 / API))
    muDeadOil = (3.141 * 1e+10) * pow(T, -3.444) * pow(np.log10(API), (10.313 * np.log10(T) - 36.447))

    return  muDeadOil   # viscosity (cP)

def muDeadLabedi(T, API):   # T (Fahrenheit)
    muDeadOil = pow(10.0, 9.224) / (pow(API, 4.7013) * pow(T, 0.6739))
    return  muDeadOil   # viscosity (cP)

def muDeadBeggs_Robinson(T, API):   # T (Fahrenheit)
    muDeadOil = 0.0
    A = pow(10.0, 0.43 + (8.33 / API))
    if T >= 70.0:
        muDeadOil = -1 + pow(10, pow(T, -1.163) * np.exp(6.9824 - 0.04658 * API))
    else:
        A0 = 22.33 - 0.194 * API + 0.00033 * API * API
        A1 = -3.20 + 0.0185 * API
        muDeadOil = np.exp(A0 + A1 * np.log(T + 310.0)) - 1.0

    return  muDeadOil   # viscosity (cP)

def muDeadBergman(T, API):  # T (Fahrenheit)
    x = np.exp(22.33 -0.194 * API + 0.00033 * API * API - (3.2 - 0.0185 * API) * np.log(T + 310.0))
    muDeadOil = np.exp(x) - 1.0

    return muDeadOil    # viscosity (cP)

def muDeadDindoruk_Christman(T, P, API, Rs):     # T (Fahrenheit), Rs (scf/STB), P(psi)
    a1 = 14.505357625
    a2 = -44.868655416
    a3 = 9.36579 * 1e+9
    a4 = -4.194017808
    a5 = 3.1461171 * 1e-9
    a6 = 1.517652716
    a7 = 0.010433654
    a8 = -0.000776880
    A = a1 * np.log10(T) + a2
    muDeadOil = a3 * pow(T, a4) * pow(np.log10(API), A) / (a5 * pow(P, a6) + a7 * pow(Rs, a8))

    return muDeadOil    # viscosity (cP)

def muDeadAlKhafaji(T, API):     # T (Fahrenheit)
    muDeadOil = pow(10.0, 4.9563 - 0.00488 * T) / pow(API + T / 30.0 - 14.29, 2.709)
    return  muDeadOil   # viscosity (cP)

def muDeadStanding(T, API):  # T (Fahrenheit)
    A = pow(10.0, 0.43 + 8.33/API)
    B = pow(360.0/(T+200.0), A)
    muDeadOil = (0.32 + 1.8*1e7/pow(API, 4.53)) * B
    return  muDeadOil   # viscosity (cP)

# saturated oil viscosity correlations

def muSatPetrosky(muDeadOil, Rs):       # Rs (scf/STB), viscosity (cP)
    A = 0.1651 + 0.6165 / (pow(10.0, 6.0866 * 1e-4 * Rs))
    B = 0.5131 + 0.5109 / (pow(10.0, 1.1831 * 1e-3 * Rs))
    muSat = A * pow(muDeadOil, B)
    return  muSat # viscosity (cP)

def muSatLabedi(muDeadOil, Pb, API):     # P (psi), viscosity (cP)
    muSat = pow(10.0, 2.344 - 0.03542 * API) * pow(muDeadOil, 0.6447) / pow(Pb, 0.426)

    return  muSat   # viscosity (cP)


def muSatBeggs_Robinson(muDeadOil, Rs):  # Rs (scf/STB), viscosity (cP)
    A1 = 10.715 * pow((Rs + 100.0), -0.515)
    A2 = 5.44 * pow((Rs + 150.0), -0.338)
    muSatOil = A1 * pow(muDeadOil, A2)
    return  muSatOil     # viscosity (cP)

def muSatBergman(muDeadOil, Rs):    # Rs (scf/STB), viscosity (cP)
    A1 = np.exp(4.768 - 0.8359 * np.log10(Rs + 300.0))
    A2 = 0.555 + 133.5 / (Rs + 300.0)
    muSatOil = A1 * pow(muDeadOil, A2)
    return  muSatOil    # viscosity (cP)


def muSatAziz(muDeadOil, Rs):    # Rs (scf/STB), viscosity (cP)
    A1 = 0.20 + (0.80 * pow(10.0, -0.00081 * Rs))
    A2 = 0.43 + (0.57 * pow(10.0, -0.00072 * Rs))
    muSatOil = A1 * pow(muDeadOil, A2)
    return  muSatOil     # viscosity (cP)

def muSatAlKhafaji(muDeadOil, Rs):   # Rs (scf/STB), viscosity (cP)
    A0 = np.log10(Rs)
    A1 = 0.247 + 0.2824 * A0 + 0.5657 * A0 * A0 - 0.4065 * A0 * A0 * A0 + 0.0631 * A0 * A0 * A0 * A0
    A2 = 0.894 + 0.0546 * A0 + 0.07667 * A0 * A0 - 0.0736 * A0 * A0 * A0 + 0.01008 * A0 * A0 * A0 * A0
    muSatOil = A1 * pow(muDeadOil, A2)
    return  muSatOil    # viscosity (cP)


def muSatDindoruk_Christman(muDeadOil, Rs): # Rs (scf/STB), viscosity (cP)
    a1 = 1.0
    a2 = 4.740729 * 1e-4
    a3 = -1.023451 * 1e-2
    a4 = 6.600358 * 1e-1
    a5 = 1.075080 * 1e-3
    a6 = 1.0
    a7 = -2.191172 * 1e-5
    a8 = -1.660981 * 1e-2
    a9 = 4.233179 * 1e-1
    a10 = -2.273945 * 1e-4
    A1 = a1 / np.exp(a2 * Rs) + a3 * pow(Rs, a4) / np.exp(a5 * Rs)
    A2 = a6 / np.exp(a7 * Rs) + a8 * pow(Rs, a9) / np.exp(a10 * Rs)
    muSatOil = A1 * pow(muDeadOil, A2)

    return muSatOil # viscosity (cP)

def muSatStanding(muDeadOil, Rs):   # Rs (scf/STB), viscosity (cP)
    temp1 = (-7.4 * 1e-4) * Rs + (2.2 * 1e-7) * Rs * Rs
    A1 = pow(10.0, temp1)
    A2 = 0.68 / pow(10.0, (8.62 * 1e-5) * Rs) + 0.25 / pow(10.0, (1.1 * 1e-3) * Rs) + 0.062 / pow(10.0, (3.74 * 1e-3) * Rs)
    muSatOil = A1 * pow(muDeadOil, A2)
    return  muSatOil   # viscosity (cP)




# undersaturated oil viscosity correlations

def muUnderSatBeal_Standing(muSat, P, Pb):
    muUnderSat = muSat + (0.001 * (P - Pb)) *(0.024 * pow(muSat, 1.6) + 0.038 * pow(muSat, 0.56))
    return  muUnderSat  # viscosity (cP)


def muUnderSatPetrosky(muSat, P, Pb):   # viscosity (cP), P(psi)
    x1 = np.log10(muSat)
    x2 = -1.0146 + 1.3322 * x1 -0.4876 * x1 * x1 - 1.15036 * x1 * x1 * x1
    muUnderSat = muSat + 1.3449 * 1e-3 * (P - Pb) * pow(10.0, x2)

    return muUnderSat    # viscosity (cP)

def muUnderSatLabedi(muSat, muDeadOil, P, Pb, API): # viscosity (cP), P(psi)
    Mmua = pow(10.0, -2.488) * pow(muDeadOil, 0.9036) * pow(Pb, 0.6151) / pow(10.0, 0.0197 * API)
    muUnderSat = muSat - Mmua * (1.0 - P / Pb)
    return  muUnderSat  # viscosity (cP)

def muUnderSatBeggs_Robinson(muSat, muDeadOil, P, Pb):  #no correlation was found
    C1 = 2.6
    C2 = 1.187
    C3 = -11.513
    C4 = -8.98 * 1e-5
    B = C1 * pow(P, C2) * np.exp(C3 + C4 * P);
    muUnderSat = muSat * pow(P / Pb, B);
    return muUnderSat

def muUnderSatBergman(muSat, muDeadOil, P, Pb): # viscosity (cP), P(psi)
    alpha = 6.5698 * 1e-7 * np.log(muSat * muSat) - 1.48211 * 1e-5 * np.log(muSat) + 2.27877 * 1e-4
    beta = 2.24623 * 1e-2 * np.log(muSat) + 0.873204
    muUnderSat = muSat * np.exp(alpha * pow(P - Pb, beta))
    return  muUnderSat  # viscosity (cP)

def muUnderSatDindoruk_Christman(muSat, muDeadOil, P, Pb, Rs):   # viscosity (cP), P(psi)
    a1 = 0.776644115
    a2 = 0.987658646
    a3 = -0.190564677
    a4 = 0.009147711
    a5 = -0.000019111
    a6 = 0.000063340

    X = a1 + a2 * np.log10(muSat) + a3 * np.log10(Rs) + a4 * muSat * np.log10(Rs) + a5 * (P - Pb)
    muUnderSat = muSat + a6 * (P - Pb) * pow(10.0, X)

    return  muUnderSat   # viscosity (cP)

def muUnderSatAlKhafaji(muSat, muDeadOil, P, Pb, API):    # viscosity (cP), P(psi)
    X = -0.3806 - 0.1845 * API + 0.004034 * API * API - 3.716 * 1e-5 * API * API * API
    muUnderSat = muSat + pow(10.0, X + 1.11 * np.log10(0.07031 * (P - Pb)))

    return  muUnderSat   # viscosity (cP)
