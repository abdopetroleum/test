import numpy as np


# gas molecular weight function
def gasMolecularWeight_func(gammaGas):
    return 28.97 * gammaGas #1bm/bmol

# gas critical properties
def GasCriticalProperties_func(gammaGas):
    Tpc = 169.2 + 349.5 * gammaGas - 74.0 * gammaGas * gammaGas
    Ppc = 756.8 - 131.0 * gammaGas - 3.6 * gammaGas * gammaGas
    return [Tpc, Ppc] # Tpc (Rankine), Ppc (psi)

# gas comprissibility factor calibration
def GasCompressibilityFactor(P, T, Ppc, Tpc, Z_value):   # P(psi), T(Rankine), Ppc (psi), Tpc (Rankine)
    Tpr = T / Tpc
    t = 1.0 / Tpr
    Ppr = P / Ppc
    y = 0.0001
    fy = 1.0

    while (abs(fy) > 1e-8) :
        fy = (-0.06125 * Ppr * t * np.exp(-1.2 * (t - 1.0) * (t - 1.0)) + (y + y * y + y * y * y - y * y * y * y) / (
            (1.0 - y) * (1.0 - y) * (1.0 - y)) - (14.76 * t - 9.76 * t * t + 4.58 * t * t * t) * y * y
             + (90.7 * t - 242.2 * t * t + 42.4 * t * t * t) * pow(y, 2.18 + 2.82 * t))
        dfy = ((1 + 4 * y + 4 * y * y - 4 * y * y * y + y * y * y * y) / ((1 - y) * (1 - y) * (1 - y) * (1 - y)) -
                (29.52 * t - 19.52 * t * t + 9.16 * t * t * t) * y + (2.18 + 2.82 * t) * (
                    90.7 * t - 242.2 * t * t + 42.4 * t * t * t) * pow(y, 1.18 + 2.82 * t))
        ynew = y - fy / dfy
        y = ynew

    Z = 0.06125 * Ppr * t * np.exp(-1.2 * (1 - t) * (1 - t)) / y

    c_value = Z_value / Z
    return  c_value


# gas comprissibility factor
def GasCompressibilityFactor(P, T, Ppc, Tpc, c_value):   # P(psi), T(Rankine), Ppc (psi), Tpc (Rankine)
    Tpr = T / Tpc
    t = 1.0 / Tpr
    Ppr = P / Ppc
    y = 0.0001
    fy = 1.0

    while (abs(fy) > 1e-8) :
        fy = (-0.06125 * Ppr * t * np.exp(-1.2 * (t - 1.0) * (t - 1.0)) + (y + y * y + y * y * y - y * y * y * y) / (
            (1.0 - y) * (1.0 - y) * (1.0 - y)) - (14.76 * t - 9.76 * t * t + 4.58 * t * t * t) * y * y
             + (90.7 * t - 242.2 * t * t + 42.4 * t * t * t) * pow(y, 2.18 + 2.82 * t))
        dfy = ((1 + 4 * y + 4 * y * y - 4 * y * y * y + y * y * y * y) / ((1 - y) * (1 - y) * (1 - y) * (1 - y)) -
                (29.52 * t - 19.52 * t * t + 9.16 * t * t * t) * y + (2.18 + 2.82 * t) * (
                    90.7 * t - 242.2 * t * t + 42.4 * t * t * t) * pow(y, 1.18 + 2.82 * t))
        ynew = y - fy / dfy
        y = ynew

    Z = 0.06125 * Ppr * t * np.exp(-1.2 * (1 - t) * (1 - t)) / y

    return  c_value * Z   # dimensionless

# gas density
def GasDensity_func(P,T, MwGas, Z):     # P (psi), T(Fahrenheit), Mw (1bm/bmol)
    R = 10.731
    T = T + 460
    gasDensity = P * MwGas / (Z * R * T)

    return  gasDensity # 1bm/ft3

# gas formation volume factor
def GFVF_func(P, T, Z): # P (psi), T(Fahrenheit)
    T = T + 460
    Psc = 14.65
    Tsc = 520
    Bg = Psc / Tsc * T / P * Z;

    return Bg # ft3/scf

# gas viscosity calibration
def GasViscosity_func_cal(P, T, gammaGas, method, mug_value):  # P (psi), T(Fahrenheit)
    muGas = 0.0
    if method.upper() == 'DEMPSEY':
        muGas = GasViscosity_Dempsey(P, T, gammaGas)
    elif method.upper() == 'LGE':
        muGas = GasViscosity_LeeGunzalez(P, T, gammaGas)
    elif method.upper() == 'LUCAS':
        muGas = GasViscosity_Lucas(P, T, gammaGas)
    else :
        print("No such method was found for gas viscosity model.")

    c_value = mug_value / muGas
    return c_value    # viscosity (cp)


def GasViscosity_func(P, T, gammaGas, method, c_value):  # P (psi), T(Fahrenheit)
    muGas = 0.0
    if method.upper() == 'DEMPSEY':
        muGas = GasViscosity_Dempsey(P, T, gammaGas)
    elif method.upper() == 'LGE':
        muGas = GasViscosity_LeeGunzalez(P, T, gammaGas)
    elif method.upper() == 'LUCAS':
        muGas = GasViscosity_Lucas(P, T, gammaGas)
    else :
        print("No such method was found for gas viscosity model.")

    return c_value * muGas    # viscosity (cp)


def GasViscosity_Dempsey(P, T, gammaGas):   # P (psi), T(Fahrenheit)
    Tpr = (T + 460) /  (175.59 + 307.97 * gammaGas)
    Ppr = P / (700.55 - 47.44 * gammaGas)
    MwGas = 28.97 * gammaGas
    a = np.array([-2.46211820, 2.97054714, 2.86264054*1e-1, 8.05420533*1e-3, 2.80860949, -3.49803305,  3.60373020*1e-1,
                  -1.04432413 * 1e-2, -7.93385684*1e-1, 1.39643306,-1.49144925*1e-1, 4.41015512*1e-3,8.39387178*1e-2,
                  -1.86408848*1e-1, 2.03367881*1e-2,  -6.09579263*1e-4])
    temp1 = (a[0] + a[1] * Ppr + a[2] * Ppr * Ppr + a[3] * Ppr * Ppr * Ppr +
        Tpr * (a[4] + a[5] * Ppr + a[6] * Ppr * Ppr + a[7] * Ppr * Ppr * Ppr))

    temp2 = (Tpr * Tpr * (a[8] + a[9] * Ppr + a[10] * Ppr * Ppr + a[11] * Ppr * Ppr * Ppr) +
        Tpr * Tpr * Tpr * (a[12] + a[13] * Ppr + a[14] * Ppr * Ppr + a[15] * Ppr * Ppr * Ppr))

    lnf = temp1 + temp2

    b = np.array([1.11231913*1e-2, 1.67726604*1e-5, 2.11360496 * 1e-9, -1.09485050*1e-4, -6.40316395*1e-8,
                  -8.99374533*1e-11, 4.57735189*1e-7, 2.12903390*1e-10, 3.97732249*1e-13])
    temp3 = (b[0] + b[1] * T + b[2] * T * T + b[3] * MwGas + b[4] * T * MwGas + b[5] * T * T * MwGas
    + b[6] * MwGas * MwGas + b[7] * T * MwGas * MwGas + b[8] * T * T * MwGas * MwGas)
    muGas = (temp3 / Tpr) * np.exp(lnf);

    return  muGas   # viscosity (cp)

def GasViscosity_LeeGunzalez(P, T, gammaGas):    # P (psi), T(Fahrenheit)
    MwGas = 28.97 * gammaGas
    criticalProps = GasCriticalProperties_func(gammaGas)
    Tpc = criticalProps[0]
    Ppc = criticalProps[0]
    Z = GasCompressibilityFactor(P, T + 460, Ppc, Tpc)
    T = T + 460
    R = 10.731
    rhog = P * MwGas / (Z * R * T)
    rhog = rhog / 62.4
    MwGas = 28.97 * gammaGas
    A1 = (9.379 + 0.01607 * MwGas) * pow(T, 1.5) / (209.2 + 19.26 * MwGas + T)
    A2 = 3.448 + 986.6 / T + 0.01009 * MwGas
    A3 = 2.447 - 0.2224 * A2
    muGas = (A1 * 1e-4) * np.exp(A2 * pow(rhog, A3))

    return muGas     # viscosity (cp)

def GasViscosity_Lucas(P, T,gammaGas):   # P (psi), T(Fahrenheit)
    MwGas = 28.97 * gammaGas
    criticalProps = GasCriticalProperties_func(gammaGas)
    Tpc = criticalProps[0]
    Ppc = criticalProps[0]
    T = T + 460
    Tpr = T / Tpc
    Ppr = P / Ppc
    A1 = (1.245 * 1e-3) * np.exp(5.1726 * pow(Tpr, -0.3286)) / Tpr
    A2 = A1 * (1.6553 * Tpr - 1.2723)
    A3 = 0.4489 * np.exp(3.0578 * pow(Tpr, -37.7332)) / Tpr
    A4 = 1.7368 * np.exp(2.2310 * pow(Tpr, -7.6351)) / Tpr
    A5 = 0.9425 * np.exp(-0.1853 * pow(Tpr, 0.4489))
    sai = 9490.0 * pow(Tpc / (MwGas * MwGas * MwGas * Ppc * Ppc * Ppc * Ppc), 1.0 / 6.0)
    eta_gsc = (0.807 * pow(Tpr, 0.618) - 0.357 * np.exp(-0.449 * Tpr) + 0.340 * np.exp(-4.058 * Tpr) + 0.018) / sai
    muGas = eta_gsc * (1 + A1 * pow(Ppr, 1.3088) / (A2 * pow(Ppr, A5) + 1.0 / (1 + A3 * pow(Ppr, A4))))

    return muGas    # viscosity (cp)



