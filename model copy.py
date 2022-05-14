import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

m0=915
h0=0.0
mEnd=m0-650
vx0=0
g=9.81
F=4*10**(2)
beta=5.6*10**(-5)
H=[]
T=[]
V=[]
M=[]
Vx=[]
X=[]
t=0
m=m0
x=0
c=0.045
dt=0.01
burn=10
rho0=1.23
s=0.13
vx=vx0
h=h0
v=0.0
c2=1.28
s2=12
M.append(m)
H.append(h)
V.append(v)
Vx.append(vx)
X.append(x)
print(F)
T.append(t)
fall=False
while True:
    if m>=mEnd:
        m=m0-burn*t
    else:
        fall=True
    if(fall==False):
        k2=c*rho0*10**(-beta*h)*s
        v=v+((F-m*k2*v**2)/m)*dt
    else:
        k2=c2*rho0*10**(-beta*h)*s2
        v=v-(m*g-k2*v**2)*dt/m
    h +=v
    vx = vx - k2*np.sqrt(v**2+vx**2)/m*vx*dt
    x+=vx*dt
    t+=dt
    M.append(m)
    T.append(t)
    H.append(h)
    V.append(v)
    Vx.append(vx0)
    X.append(x)
    if (h<0 or t>200):
        break
plt.plot(T,H)
plt.xlabel('T')
plt.ylabel('H')
plt.show()
plt.plot(T,V)
plt.xlabel('T')
plt.ylabel('V')
plt.show()