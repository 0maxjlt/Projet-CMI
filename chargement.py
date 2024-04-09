import threading
import tkinter
from tkinter import *
import sys
import time
import tkinter
import tkinter.messagebox
import customtkinter


root = tkinter.Tk()
frames = [tkinter.PhotoImage(file='test2.gif', format='gif -index %i'%(i)) for i in range(62)]

def center_window(win):
    win.wait_visibility() # make sure the window is ready


def M_95(n=0, top=None, lbl=None):
    # Play GIF (file name = m95.gif) in a 320x320 tkinter window
    # Play GIF concurrently with the loading animation below
    # Close tkinter window after play
    global process_is_alive  # used in loadingAnimation()
     # make one cycle of animation around 4 secs
    num_cycles = 2
    count = len(frames) * num_cycles
    delay = 4000 // count
    if n == 0:
        root.withdraw()
        top = tkinter.Toplevel()
        lbl = tkinter.Label(top, image=frames[0])
        lbl.pack()
        center_window(top)
        process_is_alive = True
    if n < count-1:
        lbl.config(image=frames[n%len(frames)])
        lbl.after(delay, M_95, n+1, top, lbl)
    else:
        top.destroy()
        root.deiconify()
        process_is_alive = False



M_95()


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

# -*- coding: utf-8 -*-
# 1) -  Importation des modules nécessaires
root.mainloop()
