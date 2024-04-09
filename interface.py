import subprocess, sys, os
from tkinter import filedialog
from pathlib import Path

def liste_fichiers_ext(rep):

    a = subprocess.check_output(["ls",rep])
    b = a.decode('utf-8')
    c = []

    for i in b.split():
        c.append(os.path.splitext(i))
    return c

def copier_ou_deplacer(choix, fichier, nom_repertoire):
   

    if choix == 0:
        os.system("mv '" + fichier[0]+fichier[1] + "' '" + nom_repertoire + "'")
    elif choix == 1:
        os.system("cp '" + fichier[0]+fichier[1] + "' '" + nom_repertoire + "'")

def trier_par_extension(dest,src):

    ext_a_trier= input("Entrez une ou des extensions de la forme '.ext' : ").split()
    choix = int(input("Voulez vous : \n\t0 : Deplacer les fichiers \n\t1 : Copier les fichiers \nVotre réponse : "))
    liste_fichiers = liste_fichiers_ext(src)
    for fichier in liste_fichiers:
        for ext in ext_a_trier:
            if fichier[1] == ext:
                copier_ou_deplacer(choix, fichier, dest)

def trier_par_theme(dest,src,ext_a_trier):
    choix = int(input("Voulez vous : \n\t0 : Deplacer les fichiers \n\t1 : Copier les fichiers \nVotre réponse : "))
    liste_fichiers = liste_fichiers_ext(src)
    for fichier in liste_fichiers:
        for ext in ext_a_trier:
            if fichier[1] == ext:
                copier_ou_deplacer(choix, fichier, dest)

def trier_par_motcle(dest,src):
    mot_a_trier = input("Entrez des mots clés à trier séparés par des virgules : ").split(",")
    choix = int(input("Voulez vous : \n\t0 : Deplacer les fichiers \n\t1 : Copier les fichiers \nVotre réponse : "))

    liste_fichiers = liste_fichiers_ext(src)

    for fichier in liste_fichiers:
        for mot in mot_a_trier:
            if mot in fichier[0]:
                copier_ou_deplacer(choix, fichier, dest)

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



#
#a = subprocess.check_output(["ls", repertoire])
#b = a.decode('utf-8')
#
#if not("theme.csv" in b):
#    os.system('touch theme.csv')
#    
#choix = int(input("0: Quitter, 1: Trier par extension, 2: Trier par thèmes, 3: Trier par mot clés : "))
#
#while(choix):
#
#    #Parametrage dossiers
#
#    nv_doss = int(input("0 : Nouveau dossier ou 1 : dossier existant : "))
#    
#    if nv_doss == 0:
#        nom_repertoire = input("Donnez un nom pour le dossier : ")
#        os.mkdir(nom_repertoire)
#    if nv_doss == 1:
#        nom_repertoire = input("Entrez le nom du dossier : ")
#    
#
#
#    #Utilisation de la bonne option
#
#    if choix == 1:
#        trier_par_extension(nom_repertoire)
#
#
#    elif choix == 2:
#        
#        fd = open("theme.csv", "r")
#        th = input("0 : Nouveau theme ou 1 : Deja existant : ")
#        theme2 = []
#        if th == '0':
#            trier_par_theme(nom_repertoire, add_theme())
#        else: 
#            print("Liste des thèmes disponibles : ")
#            for line in fd.readlines():
#                print("\t- ", end = "")
#                theme2.append(line.split(" : "))
#                print(line.split(" : ")[0])
#
#            theme = input("Quel thème : ")
#            for t in theme2:
#                if t[0] == theme:
#                    trier_par_theme(nom_repertoire, t[1].split())
#
#    elif choix == 3:
#        trier_par_motcle(nom_repertoire)
#
#    #choix = int(input("0: Quitter, 1: Trier par extension, 2: Trier par thèmes, 3: Trier par mot clés : "))

from tkinter import *
from tkinter import ttk
import customtkinter as ctk

repertoire = filedialog.askdirectory()
root = ctk.CTk() 
root.geometry('600x400')
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 4) - Choisir l'élément qui s'affiche par défaut
def action(event):
	
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

def test(event):
	print(xe.get())

def choix_theme(event):
    theme = Theme.get()
    fd = open("theme.csv","r")
    lines = fd.readlines()
    fd.close()
    ListeThemes = [l.split(" : ") for l in lines]
    for t in ListeThemes:
        if theme == t[0]:
            print(t[1])
            the = t[1].split()
    trier_par_theme("test",repertoire,the)

def copier_ou_deplacer_interface():
	
	if var2.get() == "1":
	
		return 1

	elif var2.get() == "2":
		
		return 2
	else: 
		return 0


def Valider():
	if not(repertoire):
		
		print("Pas de chemin choisi")
	if (copier_ou_deplacer_interface() == 0):
		print("Copier pas coché")
	elif (copier_ou_deplacer_interface() == 1 or 2):	
		print("BON")
	



#AFFICHAGE PREMIER MENU

OptionTri=["Extensions", "Thèmes","Mot-clé"]
listeCombo = ctk.CTkOptionMenu(master=root, values=OptionTri, command=action)
listeCombo.place(x = 0,y = 0)

xe = StringVar()
ex = StringVar()

Ext = ctk.CTkEntry(master=root,textvariable=xe,width=140)
MC = ctk.CTkEntry(master=root,textvariable=ex,width=140)

fd = open("theme.csv","r")
lines = fd.readlines()
fd.close()
ListeThemes = [l.split(" : ")[0] for l in lines]
Theme = ctk.CTkOptionMenu(master=root,values=ListeThemes, command = choix_theme,)

Ext.bind("<Return>",test)


var1 = ctk.StringVar()
D1 = ctk.CTkRadioButton(master = root, text="Nouveau dossier",hover=False,variable=var1,value = "1",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5)
D1.place(x = 200,y=100)
D2 = ctk.CTkRadioButton(master = root, text="Dossier existant",hover=False,variable=var1,value = "2",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5)
D2.place(x = 200,y=130)
label = ctk.CTkLabel(root)
label.pack()
listeCombo.place(x = 20,y = 100)

var2 = ctk.StringVar()
C1 = ctk.CTkRadioButton(master = root, text="Copier les fichier", command = copier_ou_deplacer_interface, hover=False,variable=var2,value = "1",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5)
C1.place(x = 350,y=100)
C2 = ctk.CTkRadioButton(master = root, text="Déplacer les fichier", command = copier_ou_deplacer_interface, hover=False,variable=var2,value = "2",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5)
C2.place(x = 350,y=130)

Valider = ctk.CTkButton(master = root, text = "test", command= Valider)
Valider.place(x = 300, y = 300)



root.mainloop()


