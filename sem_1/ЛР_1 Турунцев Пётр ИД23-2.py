from tkinter import *
import math

root = Tk()
root.geometry("600x600")
root.config(cursor="dot")
canvas = Canvas(bg="white", width=600, height=600)
canvas.pack(anchor=CENTER, expand=1)

center = 300
radius = 200
radius_1 = 250
oval_radius = 10  # Радиус вращающегося круга

# Создание основной окружности
canvas.create_oval(center - radius, center - radius,
                   center + radius, center + radius)

# Создание вращающегося круга
oval = canvas.create_oval(center - oval_radius, center - oval_radius,
                           center + oval_radius, center + oval_radius)

angle = 0  # Начальный угол

param = 5
cntr=0
inc_dec_oval=0
def move():
    global angle
    global param
    global inc_dec_oval

    x = center + radius_1 * math.cos(math.radians(angle)) - oval_radius 
    y = center + radius_1 * math.sin(math.radians(angle)) - oval_radius 
    
    canvas.coords(oval, x +inc_dec_oval, y + inc_dec_oval , x + oval_radius, y + oval_radius)
    
    
    angle += param
    

    if angle >= 360:
        angle = 0
    root.after(50, move)




def increase_angle():
    global param
    param += 5  

def decrease_angle():
    global param
    param -= 5

def decrease_oval():
    global inc_dec_oval
    inc_dec_oval += 5  

def increase_oval():
    global inc_dec_oval
    inc_dec_oval -= 5

def destroy():
    global cntr
    root.attributes('-fullscreen', True)
    cntr += 1
    if cntr == 1:
        root.configure(bg='green')
    if cntr == 2:
        root.configure(bg='blue')
    if cntr == 3:
        root.configure(bg='yellow')
    if cntr == 4:
        root.configure(bg='purple')
    if cntr == 5:
        root.configure(bg='white')
        cntr = 0


    
    
    
    

button_increase = Button(root, text="Увеличить угол", command=increase_angle)
button_increase.pack(side=LEFT, padx=10)

button_decrease = Button(root, text="Уменьшить угол", command=decrease_angle)
button_decrease.pack(side=LEFT, padx=10)

button_increase = Button(root, text="Уменьшить овал", command=decrease_oval)
button_increase.pack(side=LEFT, padx=10)

button_decrease = Button(root, text="Увеличить овал", command=increase_oval)
button_decrease.pack(side=LEFT, padx=10)

button_decrease = Button(root, text="Сменить тему", command=destroy)
button_decrease.pack(side=LEFT, padx=10)

move()

root.mainloop()
