#!/usr/bin/env python3


import subprocess, sys, os
from tkinter import filedialog
from pathlib import Path

def liste_fichiers_ext(rep):

    a = subprocess.check_output(["ls",rep])
    b = a.decode('utf-8')
    c = []

    for i in b.split("\n"):
        c.append(os.path.splitext(i))
    return c

def copier_ou_deplacer(choix, fichier, nom_repertoire,src):
   

    if choix == 2:
        os.system("mv '" +src+ fichier[0]+fichier[1] + "' '" + nom_repertoire + "'")
        print("mv '" +src+ fichier[0]+fichier[1] + "' '" + nom_repertoire + "'")
    elif choix == 1:
        os.system("cp '" +src+"/"+ fichier[0]+fichier[1] + "' '" + nom_repertoire + "'")
        print("cp '" +src+"/"+ fichier[0]+fichier[1] + "' '" + nom_repertoire + "'")

def trier_par_extension(dest,src,ext_a_trier,choix):

    liste_fichiers = liste_fichiers_ext(src)
    for fichier in liste_fichiers:
        for ext in ext_a_trier:
            if fichier[1] == ext:
                copier_ou_deplacer(choix, fichier, dest,src)

def trier_par_theme(dest,src,ext_a_trier,choix):

    liste_fichiers = liste_fichiers_ext(src)
    for fichier in liste_fichiers:
        for ext in ext_a_trier:
            if fichier[1] == ext:
                copier_ou_deplacer(choix, fichier, dest,src)

def trier_par_motcle(dest,src,choix,mot_a_trier):
    print("les mots : ",mot_a_trier)

    liste_fichiers = liste_fichiers_ext(src)

    for fichier in liste_fichiers:
        for mot in mot_a_trier:
            if mot in fichier[0]:
                copier_ou_deplacer(choix, fichier, dest,src)

def pres_theme(nom_th):
    fd = open("theme.csv","r")
    lines = fd.readlines()
    fd.close()
    li = []
    for l in lines:
        li.append(l.split(" : "))
    for n in li:
        if n[0] == nom_th:
            print("nom de theme déjà présent")
            return True
    return False

def add_theme():
    
    extension = input("Quelle extension tu veux ajouter : ").split()
    fd = open("theme.csv",'a')
    nom = input("Entrez le nom du theme : ")
    theme = nom+" : "
    if not(pres_theme(nom)):
        for ext in extension:
            theme += ext+" "
        theme += '\n'
        fd.write(theme)
        fd.close()
        print(theme)
    
    return extension

def supprimer():
    rep = int(input("Suppr : 0 : Non 1 : oui\n rep : "))
    if rep == 1:
        sup = input('nom du thème : ')
        fd = open("theme.csv","r")
        lines = fd.readlines()
        fd.close()
        fd = open("theme.csv","w")
        lines_s = []
        a = ""
        for line in lines : 
                lines_s.append(line.split(" : "))
        for k in range(len(lines_s)):
            print(lines_s[k][0],end="")
            if lines_s[k][0]!=sup:
                a += lines[k]
        fd.write(a)
        fd.close()


from tkinter import *
from tkinter import ttk

import customtkinter as ctk

rep_src = ""
rep_dest = ""
root = ctk.CTk() 
root.geometry('600x400')
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")




def action(event):
    fd = open("theme.csv","r")
    lines = fd.readlines()
    fd.close()
    global ListeThemes
    ListeThemesb = [l.split(" : ")[0] for l in lines]
    if ListeThemesb != ListeThemes:
        ListeThemes = ListeThemesb
        Theme.configure(values=ListeThemes)
    if listeCombo.get() == "Extensions":

        Ext.place(x=20,y=140)
        MC.place_forget()
        Theme.place_forget()

    elif listeCombo.get() == "Mot-clé":

        MC.place(x=20,y=140)
        Theme.place_forget()
        Ext.place_forget()

    else:

        Theme.place(x=20,y=140)
        Ext.place_forget()
        MC.place_forget()

#####
def dossier():
    if var1.get() == "Nv":
        N_dossier.place(x=200,y=190)
        rep_button_dest.place(x=200,y=160)
        return 1
    elif var1.get() == "Ex":
        N_dossier.place_forget()
        rep_button_dest.place(x=200,y=160)
        return 2
    else:
        return 0
######

def choix_theme(rep_dest):
    theme = Theme.get()
    print(rep_dest)
    fd = open("theme.csv","r")
    lines = fd.readlines()
    fd.close()
    ListeThemes = [l.split(" : ") for l in lines]
    for t in ListeThemes:
        if theme == t[0]:
            print(t[1])
            the = t[1].split()
    trier_par_theme(rep_dest,rep_src,the,cpi())

def choix_ext(rep_dest):
    trier_par_extension(rep_dest,rep_src,Ext.get().split(),cpi())

def choix_motcle(rep_dest):
    trier_par_motcle(rep_dest,rep_src,cpi(),MC.get().split())

def rep1():
    global rep_dest
    rep_dest = filedialog.askdirectory()

def rep2():
    global rep_src
    rep_src = filedialog.askdirectory()

def cpi():
	if var2.get() == "Cp":
		return 1
	elif var2.get() == "Dp":	
		return 2
	else: 
		return 0

#######

#######
def Valider():
    if not(rep_src and rep_dest):

        print("Pas de chemin choisi")
        return 0
    if (cpi() == 0):
        print("Copier pas coché")
        return 0
    else:	
        print("BON")
        return 1

def present(nom):
    ls = subprocess.check_output(["ls",rep_dest]).decode('utf-8').split('\n')
    for d in ls:
        if d == nom:
            return 1
    return 0



def test_doss():
    if Valider():
        global rep_dest
        if var1.get() == "Nv":
            nom = exp_ndoss.get()
            print(rep_dest)
            if present(nom):
                err.place(x=250,y=350)
            else:
                err.place_forget()
                os.mkdir(rep_dest+"/"+nom)
                choix_theme(rep_dest+"/"+nom)
        else:
            if listeCombo.get() == "Thèmes":
                choix_theme()
            elif listeCombo.get() == "Extensions":
                choix_ext()
            else:
                choix_motcle()



OptionTri = ["Extensions","Thèmes","Mot-clé"]
listeCombo = ctk.CTkOptionMenu(master=root, command=action, values=OptionTri)
listeCombo.place(x = 0,y = 0)

exp_ext = StringVar()
Ext = ctk.CTkEntry(master=root,textvariable=exp_ext,width=140)
exp_mc = StringVar()
MC = ctk.CTkEntry(master=root,textvariable=exp_mc,width=140)
fd = open("theme.csv","r")
lines = fd.readlines()
fd.close()
ListeThemes = [l.split(" : ")[0] for l in lines]
Theme = ctk.CTkOptionMenu(master=root,values=ListeThemes)
exp_ndoss = StringVar()
N_dossier = ctk.CTkEntry(master=root,textvariable=exp_ndoss,width=140)
rep_button_dest = ctk.CTkButton(master=root,text="repertoire",command=rep1)
rep_button_src = ctk.CTkButton(master=root,text="repertoire",command=rep2)
rep_button_src.place(x=0,y=0)
err = ctk.CTkLabel(master=root,text="Erreur, dossier existant",text_color="red")
var1 = ctk.StringVar()
D1 = ctk.CTkRadioButton(master = root, text="Nouveau dossier",hover=False,variable=var1,value = "Nv",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5,command = dossier)
D1.place(x = 200,y=100)
D2 = ctk.CTkRadioButton(master = root, text="Dossier existant",hover=False,variable=var1,value = "Ex",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5, command = dossier)
D2.place(x = 200,y=130)
label = ctk.CTkLabel(root)
label.pack()
listeCombo.place(x = 20,y = 100)
var2 = ctk.StringVar()
C1 = ctk.CTkRadioButton(master = root, text="Copier les fichier",hover=False,variable=var2,value = "Cp",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5)
C1.place(x = 350,y=100)
C2 = ctk.CTkRadioButton(master = root, text="Déplacer les fichier",hover=False,variable=var2,value = "Dp",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5)
C2.place(x = 350,y=130)
test_button = ctk.CTkButton(master=root,text="test",command = test_doss)
test_button.place(x=500,y=300)






root.mainloop()