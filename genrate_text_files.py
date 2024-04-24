import os

# Définir le chemin du dossier contenant les fichiers de transcription
chemin_dossier = 'transcription_simsamu_CTC_finetuned'

# Définir le chemin du fichier de sortie
fichier_sortie = 'transcriptions_formattees.txt'

# Ouvrir le fichier de sortie pour l'écriture
with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
    # Itérer sur tous les fichiers du dossier spécifié
    for nom_fichier in os.listdir(chemin_dossier):
        # Construire le chemin complet du fichier
        chemin_fichier = os.path.join(chemin_dossier, nom_fichier)
        
        # Assurer que le fichier est un fichier texte
        if os.path.isfile(chemin_fichier) and nom_fichier.endswith('.txt'):
            # Ouvrir le fichier de transcription pour lecture
            with open(chemin_fichier, 'r', encoding='utf-8') as f_in:
                # Lire le contenu entier du fichier et remplacer les retours à la ligne par des espaces
                contenu = f_in.read().replace('\n', ' ').strip()
                # Écrire le nom du fichier suivi par ': ', puis le contenu dans le fichier de sortie
                f_out.write(nom_fichier[:-4] + ': ' + contenu + '\n')

print("Les transcriptions ont été correctement formatées et écrites dans le fichier:", fichier_sortie)
