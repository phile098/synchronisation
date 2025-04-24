import os
import shutil
import psutil
from datetime import datetime
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
        if os.path.getsize(f1) > os.path.getsize(f2) and int(os.path.getmtime(f1)) > int(os.path.getmtime(f2)):
            return 'novelversion'

        if os.path.getsize(f1) == os.path.getsize(f2) and int(os.path.getmtime(f1)) == int(os.path.getmtime(f2)):
            return True
        
    return False
def syncronisation(destination,pc):
   
    destination=os.path.join(destination, 'synchronisation')
    if not os.path.exists(destination):
        os.makedirs(destination)
    for racine, _, dossier in os.walk(pc):
         if racine.startswith('/home/phile'):
            for fichier in dossier:
                chemin_source = os.path.join(racine, fichier)
                
                chemin_relatif = os.path.relpath(chemin_source, pc)

                chemin_dest = os.path.join(destination, chemin_relatif)

                os.makedirs(os.path.dirname(chemin_dest), exist_ok=True)

                if not fichier_identique(chemin_source, chemin_dest):
                    shutil.copy2(chemin_source, chemin_dest)
                elif fichier_identique(chemin_source, chemin_dest)=='novelversion':
                    horodatage = datetime.now().strftime("%Y%m%d-%H%M%S")
                    shutil.copy2(chemin_source, chemin_dest+'_v-'+horodatage)



def main():
    dossier=liste_dossier()
    chemin_disk=chemin_disque()
    syncronisation(chemin_disk,dossier)
    

main()