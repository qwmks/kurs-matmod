from numpy import pi
import numpy as np

G=6.67430*10**(-11)
MEarth=5.9722*10**(24)
r0=6378137
h=10000
print(G*MEarth/r0**2)
print(G*MEarth/(r0+h)**2)