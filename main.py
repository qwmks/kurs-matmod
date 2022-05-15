import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from zondModel import model
import matplotlib.animation as animation
import base64

icon= base64.b64encode(open("rocket.png", "rb").read())
def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
def collapse(layout, key, visible):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key,visible=visible))
def main():   
    sg.theme('Dark Purple 3')
    airplane= [[sg.Text('Высота самолета, м: '), sg.Input(default_text=0,key='H')],
        [sg.Text('Скорость самолета, м/с: '), sg.Input(default_text=0,key='Vx')]]
    layout = [ [sg.Text('Введите параметры')],
        [sg.Text('Общая масса, кг: '), sg.Input(default_text=915)],
        [sg.Text('Масса топлива, кг: '), sg.Input(default_text=650)],
        [sg.Text('Сила двигателя, H: '), sg.Input(default_text=49000)],
        [sg.Text('Расход топлива в секунду, кг/c: '), sg.Input(5)],
        [sg.Text('Диаметр зонда, м: '), sg.Input(0.4)],
        [sg.Text('Диаметр парашута, м: '), sg.Input(4)],
        [collapse(airplane, '-airplane-',False)],
        [sg.Checkbox('Запуск с самолета:', default=False,enable_events=True,key='-hide-airplane')],
        [sg.Button('Ввести', key='show')] ]
    window = sg.Window('Моделирование зонда', layout, icon=icon)
    airplane=False
    while True:
        event, values = window.read()
        if event.startswith('-hide-airplane'):
            airplane = not airplane
            window['H'].update('0')
            window['Vx'].update('0')
            window['-hide-airplane'].update(airplane)
            window['-airplane-'].update(visible=airplane)
        if event == 'show':
            print(values['Vx'])
            M,T,H,V,Vx,X,dt,tNoFuel,tFall,K,G=model(float(values[0]),float(values[1]),float(values[2]),float(values[3]),float(values[4]),float(values[5]),float(values['H']),float(values['Vx']))
            showRes(M,T,H,V,Vx,X,dt,tNoFuel,tFall,K,G)
        if event == sg.WIN_CLOSED:
            break
    window.close()
def showRes(M,T,H,V,Vx,X,dt,tNoFuel,tFall,K,G):
    layout = [[sg.Canvas(size=(1200, 500), key='-CANVAS-')],
        [sg.Button('Показать анимацию', key='show'),sg.Button('Показать таблицы', key='table')]]
    window = sg.Window('Графики', layout,finalize=True, icon=icon)
    canvas =window['-CANVAS-'].TKCanvas
    fig,ax =plt.subplots(2,2)
    fig.set_size_inches(12,7)
    fig_agg = draw_figure(canvas, fig)
    ax[0,0].plot(T,H)
    ax[0,0].set_xlabel('T')
    ax[0,0].set_ylabel('H')
    ax[0,0].scatter(tNoFuel,H[int(tNoFuel/dt)],marker='o',c='red')
    ax[0,0].scatter(tFall,H[int(tFall/dt)],marker='v',c='red')

    ax[0,1].plot(T,V)
    ax[0,1].set_xlabel('T')
    ax[0,1].set_ylabel('V')
    ax[0,1].scatter(tNoFuel,V[int(tNoFuel/dt)],marker='o',c='red')
    ax[0,1].scatter(tFall,V[int(tFall/dt)],marker='v',c='red')

    ax[1,0].plot(T,X)
    ax[1,0].set_xlabel('T')
    ax[1,0].set_ylabel('X')
    ax[1,0].scatter(tNoFuel,X[int(tNoFuel/dt)],marker='o',c='red')
    ax[1,0].scatter(tFall,X[int(tFall/dt)],marker='v',c='red')

    ax[1,1].plot(T,Vx)
    ax[1,1].scatter(tNoFuel,Vx[int(tNoFuel/dt)],marker='o',c='red')
    ax[1,1].scatter(tFall,Vx[int(tFall/dt)],marker='v',c='red')
    ax[1,1].set_xlabel('T')
    ax[1,1].set_ylabel('Vx')
    fig_agg.draw()
    plt.close()
    while True:
        event, values = window.read()
        if event == 'show':
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
        if event=='table':
            window.close()
            showTable(M,T,H,V,Vx,X,dt,tNoFuel,tFall,K,G)
            
        if event == sg.WIN_CLOSED:
            break
    window.close()
def showTable(M,T,H,V,Vx,X,dt,tNoFuel,tFall,K,G):
    data=[]
    time1=min(tNoFuel,tFall)
    time2=max(tNoFuel,tFall)
    time1=int(time1)
    time2=int(time2)
    endTime=int(max(T))
    amount1=5
    amount2=5
    amount3=5
    for i in range(0,int(time1/dt),int(time1/dt//5)):
        row=[]
        row.append(T[i])
        row.append(H[i])
        row.append(V[i])
        row.append(X[i])
        row.append(Vx[i])
        row.append(K[i])
        row.append(G[i])
        row=[round(el,2) if row.index(el)!=5 else round(el,4) for el in row]
        data.append(row)


    for i in range(int(time1/dt),int(time2/dt),int((time2-time1)/dt//amount2)):
        row=[]
        row.append(T[i])
        row.append(H[i])
        row.append(V[i])
        row.append(X[i])
        row.append(Vx[i])
        row.append(K[i])
        row.append(G[i])
        row=[round(el,2) if row.index(el)!=5 else round(el,4) for el in row]
        data.append(row)
    for i in range(int(time2/dt),int(endTime/dt),int((max(T)-time2)/dt//amount3)):
        row=[]
        row.append(T[i])
        row.append(H[i])
        row.append(V[i])
        row.append(X[i])
        row.append(Vx[i])
        row.append(K[i])
        row.append(G[i])
        row=[round(el,2) if row.index(el)!=5 else round(el,4) for el in row]
        data.append(row)
    row=[]
    row.append(T[len(T)-1])
    row.append(H[len(T)-1])
    row.append(V[len(T)-1])
    row.append(X[len(T)-1])
    row.append(Vx[len(T)-1])
    row.append(K[len(T)-1])
    row.append(G[len(T)-1])
    row=[round(el,2) if row.index(el)!=5 else round(el,4) for el in row]
    data.append(row)
    print(len(data))
    layout = [[sg.Text('Таблицы со значениями параметров', justification='left', font='Helvetica 14')],
            [sg.Table(values=data, headings=['Время, c','Высота, м','Вертикальная скорость, м/с', "Горизонтальное расстояние,м","Горизонтальная скорость, м/с","Коэф. сопротивления воздуха",'Ускорение свободного падения, м/с^2'], 
                    col_widths=[10,10,30,35,35,35,35],
                    auto_size_columns=False,
                    display_row_numbers=False,
                    justification='left',
                    alternating_row_color='DarkMagenta',
                    key='-TABLE-',
                    row_colors=[(amount1,'red'),(amount1+amount2,'red'),(len(data)-1,'red')],
                    row_height=35,
                    num_rows=13)],
            [sg.Button('Графики', key='graphs'), sg.Button('Анимация', key='anim')] ]
    window = sg.Window('Метеозонд', layout, finalize=True, icon=icon)
    while True:
        event, values = window.read()
        if event == 'graphs':
            window.close()
            showRes(M,T,H,V,Vx,X,dt,tNoFuel,tFall,K,G)
        if event == 'anim':
            fig, ax = plt.subplots()
            line, = plt.plot([], [],linewidth=2)
            rocket, = plt.plot([], [], 'o')
            xdata, ydata = [], []
            def update(frame,X,Y):
                if frame>=tNoFuel/dt:
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
        if event == sg.WIN_CLOSED:
            break
# Executes main
if __name__ == '__main__':
    main()