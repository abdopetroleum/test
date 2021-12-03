
import bubblePoint_functions
import GasProperties_functions
import gasOilRatio_functions
import OFVF_functions
import oilViscosity_functions
import numpy as np
import IPR_Models
import matplotlib.pyplot as plt
import oilprops
import  flowProps
import multiphase
import math

# T = 255;
# Pb = 1900;
# gammaGas = 1.2276;
# API = 22.05;
# gammaOil = oilprops.oilSG(API)
# Rs_at_bubble = 466.78;
#
# #above bubble point
# Bo_AboveBubble_vlaue = 1.3885;
# P_Bo_AboveBubble = 2315;
# method = "STANDING"
# C_Bo_AboveBubble = OFVF_functions.OFVF_func_cal(P_Bo_AboveBubble, Pb, Rs_at_bubble, T, gammaGas, gammaOil, method, Bo_AboveBubble_vlaue)
#
# Bo = OFVF_functions.OFVF_func(3019, Pb,Rs_at_bubble, T, gammaGas, gammaOil, method, C_Bo_AboveBubble)
#
# # at bubble point
# Bo_AtBubble_vlaue = 1.3526;
# P_Bo_belowBubble = 1514;
# #Rs_below_bubble = 392.31;
# method = "DINDORUK-CHRISTMAN"
# c_Rs_atAtBubble = gasOilRatio_functions.RsAtPb_cal(Pb, Pb, T, gammaGas, API, method, Rs_at_bubble)
# Rs_below_bubble = gasOilRatio_functions.RsAtPb(P_Bo_belowBubble, Pb, T, gammaGas, API, method, c_Rs_atAtBubble)
# method = "STANDING"
# C_Bo_AtBubble = OFVF_functions.OFVF_func_cal(Pb, Pb, Rs_at_bubble, T, gammaGas, gammaOil, method, Bo_AtBubble_vlaue)
# Bo = OFVF_functions.OFVF_func(P_Bo_belowBubble, Pb,Rs_below_bubble, T, gammaGas, gammaOil, method, C_Bo_AtBubble)
#
# # bwlow bubble point
#
#
# method1 = "STANDING";
# method2 = "STANDING";
# method3 = "";
# oil_vis_value = 1.6839
#
# c_oil_satviscosity = oilViscosity_functions.oilViscosity_func_cal(Pb, P_Bo_belowBubble, T, API, 392.31, method1, method2, method3, oil_vis_value)
# P_Bo_belowBubble = 1212;
# sat_oil_vis = oilViscosity_functions.oilViscosity_func(Pb, P_Bo_belowBubble, T, API, 335.08, method1, method2, method3, c_oil_satviscosity)
#
# end = 10
# # mug = GasProperties_functions.GasViscosity_func(2000, 160, 0.9, "LUCAS", mug_value)
# # Rs = gasOilRatio_functions.RsAtPb(2000, 1800, 160, 0.8, 25,"STANDING", Rs_value)
# # muo = oilViscosity_functions.deadOilViscosity_func(160, 14.7, 20, 0, "STANDING", muo_value)
e = 0.001;
Re = 35700;
rho = 65.5;
u = 2.33;
gc = 32.17;
L = 1000.0;
d = 2.259 / 12.0;
# ff = flowProps.colebrookWhite(e, Re);
# dp = flowProps.dpFriction(ff,rho, u, L, gc, d)
qo = 2000
qw = 0.0
Bw = 1.0
rhoW = 62.4
muW = 1.0
iftW = 60
qg = 1000000
T2 = 175
T1 = 175
d1 = 2.875/12.0;
d2 = 2.875/12.0;
Pb = 1500.0;
c_val_Rs = 1.0
Rs_method = "STANDING"
gammaGas = 0.8
gammaOil = 0.8
OFVF_method = "STANDING"
c_OFVF = 1.0
gacc =  32.2
gc = 32.17
dL = 50
theta = math.pi/2
tttt = np.sin(theta)
e = 0.0006
Ppc =  717
Tpc = 374
c_val_Z = 1
P1 = 850
muO_method1 = "BEAL-STANDING"
muO_method2 =  "STANDING"
muO_method3 = "BEAL-STANDING"
c_val_muO = 1
c_val_mug = 1


dp1 = multiphase.modifiedHagedornBrown(qo, qw, Bw, rhoW, muW, iftW, T2, P1, T1, d2, d1, Pb,
                          c_val_Rs, Rs_method, gammaGas, gammaOil, OFVF_method,c_OFVF,
                          gacc, gc, dL, theta, e, Ppc, Tpc, c_val_Z,
                          muO_method1, muO_method2, muO_method3, c_val_muO, c_val_mug)

print("modifiedHagedornBrown executed successfully, result: ", dp1)

dp2 = multiphase.BeggsAndBrill(qo, qw, Bw, rhoW, muW, iftW, T2, P1, T1, d2, d1, Pb,
                          c_val_Rs, Rs_method, gammaGas, gammaOil, OFVF_method,c_OFVF,
                          gacc, gc, dL, theta, e, Ppc, Tpc, c_val_Z,
                          muO_method1, muO_method2, muO_method3, c_val_muO, c_val_mug)

print("BeggsAndBrill executed successfully, result: ", dp2)

endP = 1