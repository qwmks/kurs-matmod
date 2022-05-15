from statistics import mode
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def model(m0=915,mFuel=650,F=4*10**(4)+9000,burn=5,d1=0.4,d2=4,h0=0,vx0=200):
    print(F)
    GConst=6.67430*10**(-11)
    MEarth=5.9722*10**(24)
    r0=6378137
    mEnd=m0-mFuel
    
    beta=5.6*10**(-5)
    H=[]
    T=[]
    V=[]
    M=[]
    Vx=[]
    X=[]
    K=[]
    G=[]
    t=0
    m=m0
    x=0
    c=0.045
    dt=0.05
    rho0=1.23
    s=np.pi*d1*d1/4
    vx=vx0
    h=h0
    g=GConst*MEarth/(r0+h)**2
    v=0.0
    c2=1.28
    s2=np.pi*d2*d2/4
    M.append(m)
    H.append(h)
    V.append(v)
    Vx.append(vx)
    X.append(x)
    T.append(t)
    K.append(c*rho0*10**(-beta*h)*s)
    G.append(g)
    tNoFuel=-1
    fall=False
    while True:
        g=GConst*MEarth/(r0+h)**2
        if m>=mEnd:
            m=m0-burn*t
            tNoFuel=t
        else:
            F=0
        if(fall==False):
            k2=c*rho0*10**(-beta*h)*s
            # v=v+((F-m*g-m*k2*np.sqrt(v**2+vx**2)*v)/m)*dt
            v=v+((F-m*g-m*k2*v*v)/m)*dt
            if v<=0.1 and t>1:
                tFall=t
                F=0
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
        K.append(k2)
        G.append(g)
        if (h<0):
            break
    if tNoFuel==-1:
        tNoFuel=max(T)
    return M,T,H,V,Vx,X,dt,tNoFuel,tFall,K,G

# M,T,H,V,Vx,X,dt,tNoFuel,tFall,K=model(915,650,4*10**(4)+9000,5,0.4,4,0,0)
# plt.plot(T,H)
# plt.xlabel('T')
# plt.ylabel('H')
# plt.scatter(tNoFuel,H[int(tNoFuel/dt)],marker='o',c='red')
# plt.scatter(tFall,H[int(tFall/dt)],marker='v',c='red')
# plt.show()
# plt.plot(T,V)
# plt.xlabel('T')
# plt.ylabel('V')
# plt.scatter(tNoFuel,V[int(tNoFuel/dt)],marker='o',c='red')
# plt.scatter(tFall,V[int(tFall/dt)],marker='v',c='red')
# plt.show()
# plt.plot(T,X)
# plt.xlabel('T')
# plt.ylabel('X')
# plt.scatter(tNoFuel,X[int(tNoFuel/dt)],marker='o',c='red')
# plt.scatter(tFall,X[int(tFall/dt)],marker='v',c='red')
# plt.show()
# plt.plot(T,Vx)
# plt.scatter(tNoFuel,Vx[int(tNoFuel/dt)],marker='o',c='red')
# plt.scatter(tFall,Vx[int(tFall/dt)],marker='v',c='red')
# plt.xlabel('T')
# plt.ylabel('Vx')
# plt.show()
# def showAnim():
#     fig, ax = plt.subplots()
#     line, = plt.plot([], [],linewidth=2)
#     rocket, = plt.plot([], [], 'o')
#     xdata, ydata = [], []
#     def update(frame,X,Y):
#         if frame>=tNoFuel*20:
#             # frame*=1
#             rocket.set_color('red')
#         else:
#             rocket.set_color('green')
#         if frame>tFall/dt:
#             rocket.set_marker('v')
#         if frame==0:
#             xdata.clear()
#             ydata.clear()
#         xdata.append(X[frame])
#         ydata.append(Y[frame])
#         line.set_data(xdata, ydata)
#         rocket.set_data(X[frame],Y[frame])
        
#         return line,rocket,

#     def init():
#         ax.set_xlim(0, max(X)*1.1)
#         ax.set_ylim(0, max(H)*1.1)
#         return line,
#     ani = animation.FuncAnimation(fig, update,init_func=init, frames=len(T),interval=1, fargs=(X,H), blit=True)
#     plt.show()