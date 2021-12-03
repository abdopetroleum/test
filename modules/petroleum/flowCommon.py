import math
def cal_dpdz(rho, theta, g, gc):
    dpdz = g / gc * rho * math.sin(theta);
    return dpdz

def cal_dpdzFriction(ff, rho, u, gc, d):
    dpdzf =  2.0 * ff * rho * u * u / (gc * d);
    return  dpdzf

def cal_dpdzKE(rho, q, gc, d1, d2):
    pi = math.pi;
    dpdzKE = 8.0 * rho * q * q / (pi * pi * gc) * (1.0/pow(d2, 4.0)-1.0/pow(d1, 4.0));
    return dpdzKE

def reynoldsNum(rho, u, d, mu):
    Re = rho * u * d / mu;
    return  Re

def colebrookWhite(e, Re):
    ff_new = 0.02;
    err = 1.0;
    tol = 1e-8;
    while err > tol:
        ff_old = ff_new;
        cf = (-4.0 * math.log10(e/3.7065 + 1.2613/(Re * math.sqrt(ff_old))))
        ff_new = 1.0 / (cf * cf);
        err = abs(ff_new - ff_old)/ff_old;

    return ff_new


def XY_TABLE_interpolation(XY_DATA, x):
    y = -10000000.0;
    N = len(XY_DATA);
    if (x <= XY_DATA[0][0]):
        y = XY_DATA[0][1];
    elif (x >= XY_DATA[N - 1][0]):
        y = XY_DATA[N - 1][1];
    elif ((x > XY_DATA[0][0]) and (x <= XY_DATA[math.floor(N / 2)][0])):
        index = 0;
        for i in range (0, math.floor(N / 2)):
            if (x <= XY_DATA[i][0]):
                #y = ax + b
                index = i;
                a = (XY_DATA[i][1] - XY_DATA[i - 1][1]) / (XY_DATA[i][0] - XY_DATA[i - 1][0]);
                b = XY_DATA[i][1] - a * XY_DATA[i][0];
                y = a * x + b;
                break
            elif ((x > XY_DATA[math.floor(N / 2)][0]) and (x < XY_DATA[N - 1][0])):
                index = 0;
                for i in range (math.floor(N / 2) + 1, N):
                    if (x <= XY_DATA[i][0]):
                        #y = ax + b
                        index = i;
                        a = (XY_DATA[i][1] - XY_DATA[i - 1][1]) / (XY_DATA[i][0] - XY_DATA[i - 1][0]);
                        b = XY_DATA[i][1] - a * XY_DATA[i][0];
                        y = a * x + b;
                        break

    return y;

