import numpy as np

def oilAPI(gammaoil):
    API = 141.5/gammaoil - 131.5;
    return  API

def oilSG(API):
    SG = 141.5 / (API + 131.5)
    return  SG

def oilDensityBubble(gammaOil, Rsb, gammaGas, Bob):
	dOil = (62.4 * gammaOil + 0.01357 * Rsb * gammaGas) / Bob
	return dOil

def surfaceTensionOilGas(P, T, API):
	sigmaO = (37.7 - 0.05 * (T - 100.0) - 0.26 * API) * \
             (1.0 - (7.1 * 1e-4) * P + (2.1 * 1e-7) * P * P + (2.37 * 1e-11) * P * P * P);

	return 1000.0 * sigmaO