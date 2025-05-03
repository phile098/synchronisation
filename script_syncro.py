#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import psutil
from datetime import datetime
from tqdm import tqdm
import re
import sys
import sys


def nettoyer_nom_fichier(nom):
    """
    Remplace les caractères non valides dans un nom de fichier par un underscore (_).
    """
    return re.sub(r'[<>:"/\\|?*]', '_', nom)  # Remplace les caractères interdits par "_"
print(datetime.now().strftime("%Y%'-'m-%d-%H%-M%-S"))
def presentation():

    print(r'''
 __                                  _           _   _             
/ _\_   _ _ __   ___ _ __ ___  _ __ (_)___  __ _| |_(_) ___  _ __  
\ \| | | | '_ \ / __| '__/ _ \| '_ \| / __|/ _` | __| |/ _ \| '_ \ 
_\ \ |_| | | | | (__| | | (_) | | | | \__ \ (_| | |_| | (_) | | | |
\__/\__, |_| |_|\___|_|  \___/|_| |_|_|___/\__,_|\__|_|\___/|_| |_|
    |___/                                                          


************************************************************
***          Bienvenue dans le script de synchronisation ***
************************************************************
*** Auteur  : phile098                                   ***
*** Version : 1.0                                        ***
*** Git :https://github.com/phile098/syncronisation.git  ***
*** Description :                                        ***
*** Ce programme permet de synchroniser un dossier       ***
*** de votre machine vers un disque externe,             ***
*** tout en sauvegardant les versions modifiées.         ***
***                                                      ***
*** Prérequis :                                          ***
***  - Python 3                                          ***
***  - Un dossier à synchroniser                         ***
***  - Un disque monté dans /media/                      ***
************************************************************
        ''')

def est_entier(valeur):

    """
    verifie si la valeur est un entier"""
    try:
        int(valeur) 
        return True  
    except ValueError:
        return False  
def liste_dossier():
    chemin=os.getcwd()
    listedossier=os.listdir(chemin)
    print("Voici la liste des dossiers existants :")
    for i  in range(len(listedossier)):
        if os.path.isdir(listedossier[i]):
            print(i,':',listedossier[i])
    dossier =int(input("Entrez le chiffre associer dossier à syncroniser sur le disk de la machine : "))
    if est_entier(dossier)==False:
        print("Ce n'est pas un chiffre")
        exit()
    return os.path.join(chemin, listedossier[dossier])
def chemin_disque():
    chemindisque=[]
    cpt=-1
    toutdisque=psutil.disk_partitions()
    for partiton in toutdisque:
        if partiton.mountpoint.startswith('/media/'):
            cpt+=1
            chemindisque.append(partiton.mountpoint)

            print(cpt,':',partiton.mountpoint)

    diskchoisi=int(input('Entrez le chiffre associer disk :'))
    if est_entier(diskchoisi)==False:
        print("Ce n'est pas un chiffre")
        exit()
    return chemindisque[int(diskchoisi)]
def fichier_identique(f1,f2):
    if os.path.exists(f1) and os.path.exists(f2):
        if os.path.getsize(f1) < os.path.getsize(f2) :
            return 'novelversion'

        if os.path.getsize(f1) == os.path.getsize(f2) and int(os.path.getmtime(f1)) == int(os.path.getmtime(f2)):
            return True
        
    return False
def syncronisation(destination,pc):
   
    destination=os.path.join(destination, 'synchronisation')
    if not os.path.exists(destination):
        os.makedirs(destination)
    total_fichiers = sum(len(files) for _, _, files in os.walk(pc))
    with tqdm(total=total_fichiers,desc="Synchronisation des fichiers",unit="fichier",dynamic_ncols=True,leave=True,file=sys.stdout,ascii=True,disable=False) as pbar:
        for racine, _, dossier in os.walk(pc):
            if racine.startswith(os.path.expanduser("~")):
                for fichier in dossier:
                    chemin_source = os.path.join(racine, fichier)
                    
                    chemin_relatif = os.path.relpath(chemin_source, pc)

                    chemin_dest = os.path.join(destination, chemin_relatif)

                    os.makedirs(os.path.dirname(chemin_dest), exist_ok=True)

                    if not os.path.exists(chemin_source):
                        pbar.update(1)
                        continue
                    if not fichier_identique(chemin_source, chemin_dest):
                        shutil.copy2(chemin_source, chemin_dest)
                    elif fichier_identique(chemin_source, chemin_dest)=='novelversion':
                        horodatage =datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                        shutil.copy2(chemin_source, chemin_dest+'_v-'+horodatage)
                    pbar.update(1)


def main():
    presentation()
    dossier=liste_dossier()
    chemin_disk=chemin_disque()
    syncronisation(chemin_disk,dossier)
    

main()
