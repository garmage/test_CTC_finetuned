import librosa
import numpy as np
import os
from pydub import AudioSegment
import soundfile as sf

# Chemins vers les dossiers
dossier_racine = "/home/elaugeais/Bureau/simsamu"
dossier_audio = "simsamu_wav"

# Créer le dossier de destination s'il n'existe pas déjà
if not os.path.exists(dossier_audio):
    os.makedirs(dossier_audio)

# Parcourir chaque sous-dossier dans le dossier racine
for nom_dossier in os.listdir(dossier_racine):
    chemin_sous_dossier = os.path.join(dossier_racine, nom_dossier)

    # S'assurer que c'est un dossier
    if not os.path.isdir(chemin_sous_dossier):
        continue

    # Chemins vers les fichiers audio originaux et modifiés
    fichier_original_m4a = os.path.join(chemin_sous_dossier, f"{nom_dossier}.m4a")
    fichier_sortie_wav = os.path.join(dossier_audio, f"{nom_dossier}.wav")

    # Vérifier si le fichier audio modifié existe déjà
    if os.path.isfile(fichier_sortie_wav):
        print(f"Le fichier audio pour {nom_dossier} existe déjà.")
        continue

    if not os.path.isfile(fichier_original_m4a):
        print(f"Fichier audio non trouvé pour : {chemin_sous_dossier}")
        continue

    # Convertir M4A en WAV
    sound = AudioSegment.from_file(fichier_original_m4a, format='m4a')
    fichier_temp_wav = fichier_original_m4a.replace('.m4a', '.wav')  
    sound.export(fichier_temp_wav, format='wav')

    # Copier le fichier WAV temporaire dans le dossier de sortie et le renommer
    os.rename(fichier_temp_wav, fichier_sortie_wav)
    print(f"Fichier converti et sauvegardé : {fichier_sortie_wav}")