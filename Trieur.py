#!/usr/bin/env python3


import subprocess, sys, os
from tkinter import filedialog
from pathlib import Path
from tkinter import *
import customtkinter as ctk
import threading
import sys
import time
import tkinter
import tkinter.messagebox
import customtkinter
from collections import Counter

def liste_fichiers_ext(rep):

    c = {}
    if rec.get() == "on":
        path=""
        a = subprocess.check_output(["ls","-R",rep]).decode("utf-8")
        for fic in a.split("\n"):
            if os.path.isdir(fic[:-1]):
                path = fic[:-1]
                c[path] = []
        for p in c.keys():
            fics = subprocess.check_output(["ls","-p",p]).decode("utf-8").split('\n')
            for f in fics:
                if not f.endswith('/'):
                    c[p].append(os.path.splitext(f))
    
    else:
        path = subprocess.check_output(["pwd"]).decode("utf-8")[:-1]
        a = subprocess.check_output(["ls",rep]).decode("utf-8")
        c[path] = []
        for fic in a.split("\n"):
            c[path].append(os.path.splitext(fic))
    return c


def copier_ou_deplacer(choix, fichier, nom_repertoire,src):
   
    if choix == 2:
        os.system("mv -n '" +src+"/"+ fichier[0]+fichier[1] + "' '" + nom_repertoire + "'")
    elif choix == 1:
        os.system("cp -n '" +src+"/"+ fichier[0]+fichier[1] + "' '" + nom_repertoire + "'")

def trier_par_extension(dest,src,ext_a_trier,choix):

    liste_fichiers = liste_fichiers_ext(src)
    for path in liste_fichiers.keys():
        for fichier in liste_fichiers[path]:
            for ext in ext_a_trier:
                if os.path.isfile(path+"/"+fichier[0]+fichier[1]):
                    if fichier[1] == ext:
                        copier_ou_deplacer(choix, fichier, dest,path)

def trier_par_theme(dest,src,ext_a_trier,choix):

    liste_fichiers = liste_fichiers_ext(src)
    for path in liste_fichiers.keys():
        for fichier in liste_fichiers[path]:
            for ext in ext_a_trier:
                if os.path.isfile(path+"/"+fichier[0]+fichier[1]):
                    if fichier[1] == ext:
                        copier_ou_deplacer(choix, fichier, dest,path)

def trier_par_motcle(dest,src,choix,mot_a_trier):

    liste_fichiers = liste_fichiers_ext(src)

    for path in liste_fichiers.keys():
        for fichier in liste_fichiers[path]:
            if os.path.isfile(path+"/"+fichier[0]+fichier[1]):
                for mot in mot_a_trier:
                    if mot in fichier[0]:
                        copier_ou_deplacer(choix, fichier, dest,path)

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

def add_theme(exts, nom_theme):
    
    extension = exts.split()
    fd = open("theme.csv",'a')
    theme = nom_theme + " : "
    if not(pres_theme(nom_theme)):
        for ext in extension:
            theme += ext+" "
        theme += '\n'
        fd.write(theme)
        fd.close()
        print(theme)
    
            
        fd = open("theme.csv","r")
        lines = fd.readlines()
        fd.close()
        global ListeThemes
        ListeThemes = [l.split(" : ")[0] for l in lines]
        print(ListeThemes)



    return extension

def supprimer(theme):



    sup = theme
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
    
    fd = open("theme.csv","r")
    lines = fd.readlines()
    fd.close()
    global ListeThemes
    ListeThemes = [l.split(" : ")[0] for l in lines]
    print(ListeThemes)


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
    if ModeDeTri.get() == "Extensions":

        Ext.place(x=20,y=140)
        MC.place_forget()
        Theme.place_forget()

    elif ModeDeTri.get() == "Mot-clé":

        MC.place(x=20,y=140)
        Theme.place_forget()
        Ext.place_forget()

    else:

        Theme.place(x=20,y=140)
        Ext.place_forget()
        MC.place_forget()


def dossier():
    if var1.get() == "Nv":
        N_dossier.place(x=220,y=130)
        rep_button_dest.place(x=220,y=100)
    else:
        N_dossier.place_forget()
        rep_button_dest.place(x=220,y=100)


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
    
    global info 
    if rep_src != "":
        liste_ls = liste_fichiers_ext(rep_src)
        liste_dossiers = []
        liste_fichiers = []
        nb_dossiers = -1
        nb_fichiers = 0
        
        for p in liste_ls.keys():
            for fichier in liste_ls[p]:
                if os.path.isdir(rep_src + '/' + fichier[0] + fichier[1]):
                    liste_dossiers.append(fichier)
                    nb_dossiers = nb_dossiers + 1
            
                if os.path.isfile(rep_src + '/' + fichier[0] + fichier[1]):
                    if fichier[1] == "":
                        liste_fichiers.append("Pas d'ext.")
                        nb_fichiers += 1
                    else:
                        liste_fichiers.append(fichier[1])
                        nb_fichiers += 1

        dico = (dict(Counter(liste_fichiers)))

        strInfo = ""
    
        espacement = "        "

        for cle,values in dico.items():
            
            if int(values) >= 100:
                espacement = "    "
                strInfo += ("     {1}" + espacement + "|    {0} \n").format(cle, values)
            elif int(values) >= 10:
                espacement = "      "
                strInfo += ("     {1}" + espacement + "|    {0} \n").format(cle, values)

            else : 
                strInfo += ("     {1}" + espacement + "|    {0} \n").format(cle, values) 
            
            espacement = "        "

        label_info_src.configure(text_color = "green2")
        info = "Votre dossier contient : \n\n Nombre  |  Extension\n               |  \n" + strInfo
        text_info_src.set(info ) 
        label_info_src.pack()

        strInfo2 = "Dossiers : " + str(nb_dossiers) + "\nFichiers : " + str(nb_fichiers)
        text_info_nombre.set(strInfo2)
        label_info_nombre.pack()
        label_info_nombre.place(x = 100, y = 550)

        
        nom_dossier_src = rep_src.split('/')[-1]
        text_nom_src.set("Nom : " + nom_dossier_src)
        label_nom_src.configure(text_color = "aquamarine2")
        label_nom_src.place(x = 100, y = 300)

        label_info_gen.configure(text_color = "seaGreen1")
    #taille rep
        taille_octet = 0
        for path, dirs, files in os.walk(rep_src):
            for f in files:
                fp = os.path.join(path, f)
                taille_octet += os.path.getsize(fp)
        taille_Ko = taille_octet//1000

    #affichage taille rep
        text_taille_src.set("Taille : " + str(taille_Ko) + "Ko")
        label_taille_src.place(x = 95, y = 600)



def cpi():
	if var2.get() == "Cp":
		return 1
	elif var2.get() == "Dp":	
		return 2
	else: 
		return 0

def nei():
    if var1.get() == "Nv":
        return 1
    elif var1.get() == "Ex":
        return 2
    else:
        return 0


def check_rec():
    print("1111111111111111111")
    global info 
    if rep_src != "":
        liste_ls = liste_fichiers_ext(rep_src)
        liste_dossiers = []
        liste_fichiers = []
        nb_dossiers = -1
        nb_fichiers = 0
        
        for p in liste_ls.keys():
            for fichier in liste_ls[p]:
                if os.path.isdir(rep_src + '/' + fichier[0] + fichier[1]):
                    liste_dossiers.append(fichier)
                    nb_dossiers = nb_dossiers + 1
            
                if os.path.isfile(rep_src + '/' + fichier[0] + fichier[1]):
                    if fichier[1] == "":
                        liste_fichiers.append("Pas d'ext.")
                        nb_fichiers += 1
                    else:
                        liste_fichiers.append(fichier[1])
                        nb_fichiers += 1

        dico = (dict(Counter(liste_fichiers)))

        strInfo = ""
    
        espacement = "        "

        for cle,values in dico.items():
            
            if int(values) >= 100:
                espacement = "    "
                strInfo += ("     {1}" + espacement + "|    {0} \n").format(cle, values)
            elif int(values) >= 10:
                espacement = "      "
                strInfo += ("     {1}" + espacement + "|    {0} \n").format(cle, values)

            else : 
                strInfo += ("     {1}" + espacement + "|    {0} \n").format(cle, values) 
            
            espacement = "        "

        label_info_src.configure(text_color = "green2")
        info = "Votre dossier contient : \n\n Nombre  |  Extension\n               |  \n" + strInfo
        text_info_src.set(info ) 
        label_info_src.pack()

        strInfo2 = "Dossiers : " + str(nb_dossiers) + "\nFichiers : " + str(nb_fichiers)
        text_info_nombre.set(strInfo2)
        label_info_nombre.pack()
        label_info_nombre.place(x = 100, y = 550)

        
        nom_dossier_src = rep_src.split('/')[-1]
        text_nom_src.set("Nom : " + nom_dossier_src)
        label_nom_src.configure(text_color = "aquamarine2")
        label_nom_src.place(x = 100, y = 300)

        label_info_gen.configure(text_color = "seaGreen1")
    #taille rep
        taille_octet = 0
        for path, dirs, files in os.walk(rep_src):
            for f in files:
                fp = os.path.join(path, f)
                taille_octet += os.path.getsize(fp)
        taille_Ko = taille_octet//1000

    #affichage taille rep
        text_taille_src.set("Taille : " + str(taille_Ko) + "Ko")
        label_taille_src.place(x = 95, y = 600)



###
def Valider():

    erreurs = ""
    if not(rep_src):
        erreurs += "Pas de dossier source selectionné \n"

    if not(exp_ext.get()) and not(exp_mc.get()):
        erreurs += "Pas de mode de tri selectionné\n"

    if (nei() == 0):
        erreurs += "Nouveau ou dossier existant pas coché \n"   
        
    else: 
        if not(rep_dest):
            erreurs += "Pas de dossier destination selectionné \n"
        if var1.get() == "Nv":
            if exp_ndoss.get() == "":
                erreurs += "Pas de nom donné pour le dossier\n"




    if (cpi() == 0):
        erreurs += "Copier ou deplacer pas coché\n"
        
    
        
    if (rep_src and rep_dest and cpi() != 0 and nei() != 0):	
        text_err_valider.set("BON")
        label_err_valider.configure(text_color = "green")
        label_err_valider.place(x = 500, y = 200)
        return 1

    text_err_valider.set(erreurs)
    label_err_valider.configure(text_color = "firebrick1")
    label_err_valider.place(x = 500, y = 200)

    return 0    
###

def present(nom):
    ls = subprocess.check_output(["ls",rep_dest]).decode('utf-8').split('\n')
    for d in ls:
        if d == nom:
            return 1
    return 0



def test_doss():
    print(Valider())
    if Valider():
        global rep_dest
        if var1.get() == "Nv":
            nom = exp_ndoss.get()
            print(rep_dest)
            if present(nom):
                err.place(x=250,y=350)
            else:

                print(ModeDeTri.get())
                err.place_forget()
                os.mkdir(rep_dest+"/"+nom)
                if ModeDeTri.get() == "Thèmes":
                    choix_theme(rep_dest+"/"+nom)
                elif ModeDeTri.get() == "Extensions":
                    choix_ext(rep_dest+"/"+nom)
                else:
                    choix_motcle(rep_dest+"/"+nom)

        else:
            print(ModeDeTri.get())
            if ModeDeTri.get() == "Thèmes":
                choix_theme(rep_dest)
            elif ModeDeTri.get() == "Extensions":
                choix_ext(rep_dest)
            else:
                choix_motcle(rep_dest)

frames = [tkinter.PhotoImage(file='animation.gif', format='gif -index %i'%(i)) for i in range(62)]

def center_window(win):
    win.wait_visibility() # make sure the window is ready


def chargement(n=0, top=None, lbl=None):
    # Play GIF (file name = m95.gif) in a 320x320 tkinter window
    # Play GIF concurrently with the loading animation below
    # Close tkinter window after play
    global process_is_alive  # used in loadingAnimation()
     # make one cycle of animation around 4 secs
    num_cycles = 1
    count = len(frames) * num_cycles
    delay = 1500 // count
    if n == 0:
        root.withdraw()
        top = tkinter.Toplevel()
        lbl = tkinter.Label(top, image=frames[0])
        lbl.pack()
        center_window(top)
        process_is_alive = True
    if n < count-1:
        lbl.config(image=frames[n%len(frames)])
        lbl.after(delay, chargement, n+1, top, lbl)
    else:
        top.destroy()
        root.deiconify()
        process_is_alive = False

chargement()

def actu():
    Theme2.configure(value=ListeThemes)



font=("System", 15)

OptionTri=["Extensions", "Thèmes","Mot-clé"]
ModeDeTri = ctk.CTkOptionMenu(master=root, values=OptionTri, command=action, width=140, dropdown_font = font, font = font)
ModeDeTri.place(x = 0,y = 0)
ModeDeTri.set("Mode de tri")

exp_ext = StringVar()
Ext = ctk.CTkEntry(master=root,textvariable=exp_ext,width=140, font = font)

exp_mc = StringVar()
MC = ctk.CTkEntry(master=root,textvariable=exp_mc, width=140, font = font)

fd = open("theme.csv","r")
lines = fd.readlines()
fd.close()
ListeThemes = [l.split(" : ")[0] for l in lines]
Theme = ctk.CTkOptionMenu(master=root,values=ListeThemes, width=160, dropdown_font = font, font = font)
Theme.set("Choix thème")

exp_ndoss = StringVar()
N_dossier = ctk.CTkEntry(master=root,textvariable=exp_ndoss,width=157, font = font)
rep_button_dest = ctk.CTkButton(master=root,text="Chemin du dossier",command=rep1, width=140, font = font)
rep_button_src = ctk.CTkButton(master=root,text="Quel dossier trier",command=rep2, width=140, font = font)
rep_button_src.place(x=20,y=40)


err = ctk.CTkLabel(master=root,text="Erreur, dossier existant",text_color="red")
var1 = ctk.StringVar()
D1 = ctk.CTkRadioButton(master = root, text="Nouveau dossier", width=140, font = font ,hover=False,variable=var1,value = "Nv",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5,command = dossier)
D1.place(x = 220,y=30)
D2 = ctk.CTkRadioButton(master = root, text="Dossier existant", width=140, font = font ,hover=False,variable=var1,value = "Ex",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5, command = dossier)
D2.place(x = 220,y=60)

ModeDeTri.place(x = 20,y = 100)
var2 = ctk.StringVar()
C1 = ctk.CTkRadioButton(master = root, text="Copier les fichier", width=140, font = font , hover=False,variable=var2,value = "Cp",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5)
C1.place(x = 400,y=30)
C2 = ctk.CTkRadioButton(master = root, text="Déplacer les fichier", width=140, font = font ,hover=False,variable=var2,value = "Dp",radiobutton_width=15,radiobutton_height=15,border_width_checked=3.5)
C2.place(x = 400,y=60)
test_button = ctk.CTkButton(master=root,text="Valider",command = test_doss, font = font)
test_button.place(x=900,y=100)

check_var = StringVar().set("on")
rec = customtkinter.CTkCheckBox(master=root, text="Parcourir sous dossiers", width=140    , font = font ,variable=check_var, onvalue="on", offvalue="off",command=check_rec)
rec.place(x=600,y=100)


text_info_gen = StringVar()
label_info_gen = ctk.CTkLabel(master=root,
                               textvariable=text_info_gen,
                               corner_radius=8,
                               justify = 'left',
                               text_color = "SlateBlue1",
                               font = ('System', 22))

text_info_gen.set("Informations générales")
label_info_gen.place(x = 35, y = 250)


text_info_src = StringVar()

frame = ctk.CTkScrollableFrame(root, height = 150, width= 200)
frame._scrollbar.configure(height = 0)

label_info_src = ctk.CTkLabel(master=frame,
                               textvariable=text_info_src,
                               justify = 'left',
                               text_color = "green2",
                               font = ('System', 15))
                               
text_info_src.set("Pas de dossier choisi" )
label_info_src.configure(text_color = "red2")
label_info_src.pack()
frame.place(x = 60, y = 350)

text_info_nombre = StringVar()
label_info_nombre = ctk.CTkLabel(master=root,
                               textvariable=text_info_nombre,
                               justify = 'left',
                               text_color = "Gold",
                               font = ('System', 15))

text_nom_src = StringVar()
label_nom_src = ctk.CTkLabel(master=root,
                               textvariable=text_nom_src,
                               justify = 'left',
                               text_color = "aquamarine2",
                               font = ('System', 15))
text_nom_src.set("Nom dossier")
label_nom_src.configure(text_color = "chocolate1")
label_nom_src.place(x = 110, y = 300)


text_taille_src = StringVar()
label_taille_src = ctk.CTkLabel(master=root,
                               textvariable=text_taille_src,
                               justify = 'left',
                               text_color = "DarkOrange1",
                               font = ('System', 15))

text_err_valider = StringVar()
label_err_valider = ctk.CTkLabel(master=root,
                               textvariable=text_err_valider,
                               justify = 'left',
                               text_color = "DarkOrange1",
                               font = ('System', 15))



def valider_addtheme():

    
    exts = text_addtheme.get()
    nom_theme = text_nomtheme.get()

    if exts != "" and nom_theme != "":

        entry_addtheme.delete(0,END)
        entry_nomtheme.delete(0,END)
        add_theme(exts, nom_theme)
        Theme2.configure(values=ListeThemes)
        Theme.configure(values=ListeThemes)
    else:
        print("Pas renseigné")
       
### Ajout theme

text_addtheme = StringVar()
entry_addtheme = ctk.CTkEntry(master=root,textvariable=text_addtheme,width=140, font = font)

text_nomtheme = StringVar()
entry_nomtheme = ctk.CTkEntry(master=root,textvariable=text_nomtheme,width=140, font = font)

btn_valider_addtheme = ctk.CTkButton(master=root,text="Envoyer",command=valider_addtheme, width=140, font = font)

entry_addtheme.place(x = 530, y = 480)
entry_nomtheme.place(x = 530, y = 390)
btn_valider_addtheme.place(x= 530, y = 530)

text_personnalisation = StringVar()
label_personnalisation = ctk.CTkLabel(master=root,
                               textvariable=text_personnalisation,
                               corner_radius=8,
                               justify = 'left',
                               text_color = "SlateBlue1",
                               font = ('System', 22))

text_personnalisation.set("Personnalisation")
label_personnalisation.place(x = 680, y = 250)

text_nom_affiche = StringVar()
label_nom_affiche = ctk.CTkLabel(master=root,
                               textvariable=text_nom_affiche,
                               justify = 'left',
                               text_color = "SteelBlue1",
                               font = ('System', 15))
text_nom_affiche.set("Ajouter Thème")
label_nom_affiche.place(x = 540, y = 300)

text_exttheme_affiche = StringVar()
label_exttheme = ctk.CTkLabel(master=root,
                               textvariable=text_exttheme_affiche,
                               corner_radius=8,
                               justify = 'left',
                               text_color = "cornflower blue",
                               font = ('System', 14))

text_exttheme_affiche.set("          Entrez des extensions à ajouter \n(separées par des espaces => '.ext1 .ext2')")
label_exttheme.place(x = 435, y = 435)

text_nomtheme_affiche = StringVar()
label_nomtheme_affiche = ctk.CTkLabel(master=root,
                               textvariable=text_nomtheme_affiche,
                               corner_radius=8,
                               justify = 'left',
                               text_color = "cornflower blue",
                               font = ('System', 14))

text_nomtheme_affiche.set("Entrez un nom de thème")
label_nomtheme_affiche.place(x = 500, y = 360)

#Supprimer theme

def Valider_supp_theme():
    
    if Theme2.get() != "":
        theme = Theme2.get()
        supprimer(theme)
        Theme2.configure(values=ListeThemes)
        Theme2.set("Choisir")
    else:
        print("pas choisi")


btn_valider_addtheme = ctk.CTkButton(master=root,text="Envoyer",command=Valider_supp_theme, width=140, font = font)
btn_valider_addtheme.place(x= 900, y = 530)

Theme2 = ctk.CTkOptionMenu(master=root,values=ListeThemes, width=160, dropdown_font = font, font = font)
Theme2.place(x = 900, y = 390)
Theme2.set("Choix thème")

text_supp_theme = StringVar()
label_supp_theme = ctk.CTkLabel(master=root,
                               textvariable=text_supp_theme,
                               corner_radius=8,
                               justify = 'left',
                               text_color = "cornflower blue",
                               font = ('System', 14))

text_supp_theme.set("Choisissez un thème à supprimer")
label_supp_theme.place(x = 850, y = 360)

text_supp_theme_2 = StringVar()
label_supp_theme_2 = ctk.CTkLabel(master=root,
                               textvariable=text_supp_theme_2,
                               justify = 'left',
                               text_color = "SteelBlue1",
                               font = ('System', 15))
text_supp_theme_2.set("Supprimer Thème")
label_supp_theme_2.place(x = 900, y = 300)


text_ligne = StringVar()
label_ligne = ctk.CTkLabel(master=root,
                               textvariable=text_ligne,
                               justify = 'left',
                               text_color = "dodger blue",
                               font = ('System', 20, "bold"))
text_ligne.set("_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________")
label_ligne.place(x = 0, y = 170)

text_ligne2 = StringVar()
label_ligne2 = ctk.CTkLabel(master=root,
                               textvariable=text_ligne2,
                               justify = 'left',
                               text_color = "dodger blue",
                               font = ('System', 15, "bold"))
text_ligne2.set("|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n ")
label_ligne2.place(x = 400, y = 196)

root.mainloop()
