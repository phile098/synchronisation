#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import shutil
import psutil
from datetime import datetime
from tqdm import tqdm
import re
import sys
import os
import time
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Script de synchronisation de dossiers avec versionnage"
    )

    parser.add_argument(
        '--source', '-s', type=str,
        help="Chemin du dossier source à synchroniser"
    )

    parser.add_argument(
        '--destination', '-d', type=str,
        help="Chemin du disque ou dossier destination"
    )

    parser.add_argument(
        '--interactive', '-i', action='store_true',
        help="Active le mode interactif pour choisir les dossiers"
    )


    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0',
        help="Affiche la version du programme"
    )

    return parser.parse_args()
def nettoyer_nom_fichier(nom):
    """
    Nettoie un nom de fichier/dossier :
    - supprime les caractères illégaux,
    - remplace les points consécutifs,
    - supprime les espaces et points en début/fin.
    """
    nom = re.sub(r'[<>:"/\\|?*]', '_', nom)  # caractères interdits
    nom = re.sub(r'\.{2,}', '.', nom)        # remplace plusieurs points consécutifs
    nom = nom.strip(' .')                    # supprime espaces et points début/fin


    return nom
def presentation():

    print(r'''
                       _                     _           _   _             
                      | |                   (_)         | | (_)            
  ___ _   _ _ __   ___| |__  _ __ ___  _ __  _ ___  __ _| |_ _  ___  _ __  
 / __| | | | '_ \ / __| '_ \| '__/ _ \| '_ \| / __|/ _` | __| |/ _ \| '_ \ 
 \__ \ |_| | | | | (__| | | | | | (_) | | | | \__ \ (_| | |_| | (_) | | | |
 |___/\__, |_| |_|\___|_| |_|_|  \___/|_| |_|_|___/\__,_|\__|_|\___/|_| |_|
       __/ |                                                               
      |___/                                                                



************************************************************
***          Bienvenue dans le script de synchronisation ***
************************************************************
*** Auteur  : phile098                                   ***
*** Version : 1.0                                        ***
*** Git :https://github.com/phile098/synchronisation.git ***
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
        print("Ce n'est pas un chiffre")
        exit()
def erreur_chiffre(x,taille):
    try:
        if x < 0 or x >taille:
            raise ValueError
    except ValueError:
        print("Erreur : le chiffre doit être compris entre 0 et", taille)
        exit()
def liste_dossier():
    
    chemin=os.getcwd()
    listedossier=os.listdir(chemin)
    taille=len(listedossier)
    print("Voici la liste des dossiers existants :")
    for i  in range(taille):
        if os.path.isdir(listedossier[i]):
            print(i,':',listedossier[i])
    dossier =(input("Entrez le chiffre associer dossier à syncroniser sur le disk de la machine : "))
    est_entier(dossier)

    erreur_chiffre(int(dossier),taille-1)

    return os.path.join(chemin, listedossier[int(dossier)])
def chemin_disque():
    chemindisque=[]
    cpt=-1
    toutdisque=psutil.disk_partitions()
    for partiton in toutdisque:
        if partiton.mountpoint.startswith('/media/'):
            cpt+=1
            chemindisque.append(partiton.mountpoint)
            print(cpt,':',partiton.mountpoint)

    diskchoisi=(input('Entrez le chiffre associer disk :'))
    est_entier(diskchoisi)
    erreur_chiffre(int(diskchoisi),cpt)

    return chemindisque[int(diskchoisi)]
def fichier_identique(f1,f2):
    if os.path.exists(f1) and os.path.exists(f2):
        if os.path.getsize(f1) < os.path.getsize(f2) :
            return 'novelversion'

        if os.path.getsize(f1) == os.path.getsize(f2) and int(os.path.getmtime(f1)) == int(os.path.getmtime(f2)):
            return True
        
    return False
def synchronisation(destination,source):
   
    destination=os.path.join(destination, 'synchronisation')
    if not os.path.exists(destination):
        os.makedirs(destination)
    dossier_final = os.path.basename(os.path.normpath(source))
    destination= os.path.join(destination,  dossier_final)
    if not os.path.exists(destination):

            os.makedirs(destination, exist_ok=True)

    total_fichiers = sum(len(files) for _, _, files in os.walk(source))
    with tqdm(total=total_fichiers,desc="Synchronisation des fichiers",unit="fichier",dynamic_ncols=True,leave=True,file=sys.stdout,ascii=True,disable=False) as pbar:
        for racine, _, dossier in os.walk(source):
            # if racine.startswith(os.path.expanduser("~")):
            for fichier in dossier:
                chemin_source = os.path.join(racine, fichier)
                
                chemin_relatif = os.path.relpath(chemin_source, source)
                parties = chemin_relatif.split(os.sep)
                parties_nettoyees = [nettoyer_nom_fichier(partie) for partie in parties]
                chemin_relatif_nettoye = os.path.join(*parties_nettoyees)

                chemin_dest = os.path.join(destination, chemin_relatif_nettoye)

                os.makedirs(os.path.dirname(chemin_dest), exist_ok=True)

                if not os.path.exists(chemin_source):
                    pbar.update(1)
                    continue
                a=fichier_identique(chemin_source, chemin_dest)
                if a==False:
                    try:
                        shutil.copy2(chemin_source, chemin_dest)
                    except FileNotFoundError:
                        print(f"Le fichier {chemin_source} n'existe pas.")
                        pbar.update(1)
                        continue
                elif a=='novelversion':
                    horodatage =datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                    try:
                        shutil.copy2(chemin_source, chemin_dest+'_v-'+horodatage)
                    except FileNotFoundError:
                        print(f"Le fichier {chemin_source} n'existe pas.")
                        pbar.update(1)
                        continue
                pbar.update(1)


def main():
    args = parse_arguments()
    presentation()

    if args.interactive:
        temp=time.time()
        source = liste_dossier()
        destination = chemin_disque()
        synchronisation(destination,source)
        temps_ecoule = time.time() - temp
        print(temps_ecoule)
    else: 
        if args.source is None or args.destination is None:
            print("Erreur : les arguments --source et --destination sont obligatoires.")
            sys.exit(1)
        source = args.source
        destination = args.destination  
        temp=time.time()
   


        synchronisation(destination,source)

        temps_ecoule = time.time() - temp
        print(temps_ecoule)
main()
