from tkinter import *
from random import randint

def verificarLetraFunc():
    letrasUsadas.append(letraObtenida.get())
    print(letrasUsadas)

    if letraObtenida.get() in palabra:
        if palabra.count(letraObtenida.get()) > 1:
            for i in range(len(palabra)):
                if palabra[i] == letraObtenida.get():
                    guiones[i].config(text=""+letraObtenida.get())
        else:
            guiones[palabra.index(letraObtenida.get())].config(text=""+letraObtenida.get())

pantalla = Tk()
letraObtenida = StringVar()
letrasUsadas = []
archivo = open("palabras.txt", "r")
conjuntoPalabras = list(archivo.read().split("\n"))
palabra = conjuntoPalabras[randint(0,len(conjuntoPalabras)-1)].lower()

pantalla.config(width=1000, height=700, bg="black", relief="raised", bd=5)

#Creación del primer frame, en base a la pantalla
frame1 = Frame(pantalla)
frame1.config(width=1000, height=700, bg="gray", relief="flat")
frame1.grid_propagate(False)
#Empaquetamos el primer frame
frame1.pack()

#Label para indicar al usuario que aqhi tiene que poner una letra
Label(frame1, text="Ingresa una letra:", bg="gray", font=("Verdana", 24)).grid(row=0, column=0, padx=10, pady=10)

#Entrada de la letra
letra = Entry(frame1, width=1, font=("Verdana", 24), textvariable=letraObtenida).grid(row=0, column=1, padx=10, pady=10)

#Boton de comprobacion de letra
btnVerLetra = Button(frame1, text="Verificar", bg="white", font=("Verdana", 18), command=verificarLetraFunc).grid(row=1, column=0, padx=10, pady=10)


#Guiones de la palabra

guiones = [Label(frame1, text="_", bg="gray", font=("Verdana", 24))for _ in palabra]
inicialX = 200
for i in range(len(palabra)):
    guiones[i].place(x=inicialX, y=400)
    inicialX +=50

pantalla.mainloop()
