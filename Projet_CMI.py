import subprocess, sys, os
from tkinter import filedialog
from pathlib import Path

def liste_fichiers_ext():

    a = subprocess.check_output(["ls"])
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

def trier_par_extension(nom_repertoire):

    ext_a_trier= input("Entrez une ou des extensions de la forme '.ext' : ").split()
    choix = int(input("Voulez vous : \n\t0 : Deplacer les fichiers \n\t1 : Copier les fichiers \nVotre réponse : "))
    liste_fichiers = liste_fichiers_ext()
    for fichier in liste_fichiers:
        for ext in ext_a_trier:
            if fichier[1] == ext:
                copier_ou_deplacer(choix, fichier, nom_repertoire)

def trier_par_theme(nom_repertoire,ext_a_trier):
    choix = int(input("Voulez vous : \n\t0 : Deplacer les fichiers \n\t1 : Copier les fichiers \nVotre réponse : "))
    liste_fichiers = liste_fichiers_ext()
    for fichier in liste_fichiers:
        for ext in ext_a_trier:
            if fichier[1] == ext:
                copier_ou_deplacer(choix, fichier, nom_repertoire)

def trier_par_motcle(nom_repertoire):
    mot_a_trier = input("Entrez des mots clés à trier séparés par des virgules : ").split(",")
    choix = int(input("Voulez vous : \n\t0 : Deplacer les fichiers \n\t1 : Copier les fichiers \nVotre réponse : "))

    liste_fichiers = liste_fichiers_ext()

    for fichier in liste_fichiers:
        for mot in mot_a_trier:
            if mot in fichier[0]:
                copier_ou_deplacer(choix, fichier, nom_repertoire)

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

def tri_dans_rep():

    nv_doss = int(input("0 : Nouveau dossier ou 1 : dossier existant : "))
    
    if nv_doss == 0:
        nom_dossier = input("Donnez un nom pour le dossier : ")
        print("Selectionnez un repertoire ou ranger ce fichier")

        chemin_dossier = filedialog.askdirectory()
        os.mkdir(chemin_dossier + "/" + nom_dossier)
        chemin = chemin_dossier + "/" + nom_dossier

    if nv_doss == 1:
        print("Selectionnez le repertoire")

        chemin = filedialog.askdirectory()
    
    return chemin


    
repertoire = filedialog.askdirectory()

a = subprocess.check_output(["ls", repertoire])
b = a.decode('utf-8')


if not("theme.csv" in b):
    os.system('touch theme.csv')
    
choix = int(input("0: Quitter, 1: Trier par extension, 2: Trier par thèmes, 3: Trier par mot clés : "))

while(choix):

    #Parametrage dossiers // OU RANGER LES FICHIERS 

    nom_repertoire = tri_dans_rep()

    #Utilisation de la bonne option

    if choix == 1:
        trier_par_extension(nom_repertoire)


    elif choix == 2:
        
        fd = open("theme.csv", "r")
        th = input("0 : Nouveau theme ou 1 : Deja existant : ")
        theme2 = []
        if th == '0':
            trier_par_theme(nom_repertoire, add_theme())
        else: 
            print("Liste des thèmes disponibles : ")
            for line in fd.readlines():
                print("\t- ", end = "")
                theme2.append(line.split(" : "))
                print(line.split(" : ")[0])

            theme = input("Quel thème : ")
            for t in theme2:
                if t[0] == theme:
                    trier_par_theme(nom_repertoire, t[1].split())

    elif choix == 3:
        trier_par_motcle(nom_repertoire)

    choix = int(input("0: Quitter, 1: Trier par extension, 2: Trier par thèmes, 3: Trier par mot clés : "))

