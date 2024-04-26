#!/usr/bin/env python3


import subprocess, sys, os
from tkinter import filedialog
from pathlib import Path
from tkinter import *
import customtkinter as ctk

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

rep_src = ""
rep_dest = ""

#création interface graphique

root = ctk.CTk() 
root.geometry('1280x720+320+180') 
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


def dossier():
    if var1.get() == "Nv":
        N_dossier.place(x=200,y=190)
        rep_button_dest.place(x=200,y=160)
    else:
        N_dossier.place_forget()
        rep_button_dest.place(x=200,y=160)


def choix_theme():
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

def choix_ext():
    trier_par_extension(rep_dest,rep_src,Ext.get().split(),cpi())

def choix_motcle():
    trier_par_motcle(rep_dest,rep_src,cpi(),MC.get().split())

def rep1():
    global rep_dest
    rep_dest = filedialog.askdirectory()
