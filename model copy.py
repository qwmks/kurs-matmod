import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

m0=915
h0=0
mEnd=m0-650
vx0=0
g=9.81
F=4*10**(4)+9000
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
dt=0.05
burn=5
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
T.append(t)
tNoFuel=200
fall=False
while True:
    if m>=mEnd:
        m=m0-burn*t
        tNoFuel=t
    else:
        F=0
    if(fall==False):
        k2=c*rho0*10**(-beta*h)*s
        v=v+((F-m*g-m*k2*v**2)/m)*dt
        if v<=0.1 and t>1:
            tFall=t
            fall=True
    else:
        k2=c2*rho0*10**(-beta*h)*s2
        v=v-(m*g-k2*v**2)*dt/m
    h+=v*dt
    vx = vx - k2*np.sqrt(v**2+vx**2)*vx*dt/m
    x+=vx*dt
    t+=dt
    M.append(m)
    T.append(t)
    H.append(h)
    V.append(v)
    Vx.append(vx)
    X.append(x)
    if (h<0):
        break
plt.plot(T,H)
plt.xlabel('T')
plt.ylabel('H')
plt.scatter(tNoFuel,H[int(tNoFuel/dt)],marker='o',c='red')
plt.scatter(tFall,H[int(tFall/dt)],marker='v',c='red')
plt.show()
plt.plot(T,V)
plt.xlabel('T')
plt.ylabel('V')
plt.scatter(tNoFuel,V[int(tNoFuel/dt)],marker='o',c='red')
plt.scatter(tFall,V[int(tFall/dt)],marker='v',c='red')
plt.show()
plt.plot(T,X)
plt.xlabel('T')
plt.ylabel('X')
plt.scatter(tNoFuel,X[int(tNoFuel/dt)],marker='o',c='red')
plt.scatter(tFall,X[int(tFall/dt)],marker='o',c='red')
plt.show()
plt.plot(T,Vx)
plt.scatter(tNoFuel,Vx[int(tNoFuel/dt)],marker='o',c='red')
plt.scatter(tFall,Vx[int(tFall/dt)],marker='o',c='red')
plt.xlabel('T')
plt.ylabel('Vx')
plt.show()
fig, ax = plt.subplots()
line, = plt.plot([], [],linewidth=2)
rocket, = plt.plot([], [], 'o')
xdata, ydata = [], []
def update(frame,X,Y):
    if frame>=tNoFuel*20:
        # frame*=1
        rocket.set_color('red')
    else:
        rocket.set_color('green')
    if frame>tFall/dt:
        rocket.set_marker('v')
    if frame==0:
        xdata.clear()
        ydata.clear()
    xdata.append(X[frame])
    ydata.append(Y[frame])
    line.set_data(xdata, ydata)
    rocket.set_data(X[frame],Y[frame])
    
    return line,rocket,

def init():
    ax.set_xlim(0, max(X)*1.1)
    ax.set_ylim(0, max(H)*1.1)
    return line,
ani = animation.FuncAnimation(fig, update,init_func=init, frames=len(T),interval=1, fargs=(X,H), blit=True)
plt.show()
# ani.save('simulation.gif',progress_callback =lambda i, n: print(f'Saving frame {i} of {n}'), writer='imagemagick')
# print('make_gif done')