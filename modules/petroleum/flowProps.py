import numpy as np



def sperfacialVelocity(qa, A):
    usa = qa / A;
    return A

def slipvelocity(ua, ub):
    us = ua - ub;
    return us

def rhoRverage(rhog, rhol, yl):
    rho = (1.0 - yl) * rhog + yl * rhol;
    return rho

# def velocity()

