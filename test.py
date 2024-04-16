from medkit.core.audio import MemoryAudioBuffer, AudioDocument
from medkit.audio.segmentation.pa_speaker_detector import PASpeakerDetector
from medkit.audio.transcription.sb_transcriber import SBTranscriber
import librosa
import numpy as np
import os

# Chemins vers les dossiers
dossier_audio = "simsamu_wav"
dossier_transcriptions = "transcription_simsamu_CTC_finetuned"

# Créer le dossier de transcriptions s'il n'existe pas déjà
if not os.path.exists(dossier_transcriptions):
    os.makedirs(dossier_transcriptions)

# Initialisation du détecteur de locuteurs
speaker_detector = PASpeakerDetector(
    model="medkit/simsamu-diarization",
    device=-1,  # Exécution sur CPU
    segmentation_batch_size=10,
    embedding_batch_size=10,
    output_label="speaker"
)

# Initialisation du transcripteur
transcriber = SBTranscriber(
    model="medkit/simsamu-transcription",
    needs_decoder=False,
    output_label="transcription",
    device=-1,  # Exécution sur CPU
    batch_size=10,
)

# Parcourir chaque fichier WAV dans le dossier audio
for fichier in os.listdir(dossier_audio):
    chemin_fichier_wav = os.path.join(dossier_audio, fichier)
    nom_fichier_texte = fichier.replace('.wav', '.txt')
    chemin_fichier_texte = os.path.join(dossier_transcriptions, nom_fichier_texte)

    # Vérifier si la transcription existe déjà
    if not os.path.isfile(chemin_fichier_texte):
        if os.path.isfile(chemin_fichier_wav) and fichier.endswith('.wav'):
            y, sr = librosa.load(chemin_fichier_wav, sr=None)
            y_resampled = librosa.resample(y, orig_sr=sr, target_sr=16000)

            # Assurez-vous que le tableau est en deux dimensions [nb_channels, nb_samples]
            if y_resampled.ndim == 1:
                y_resampled = y_resampled[np.newaxis, :]  # Ajoute une dimension pour les canaux

            # Créer un MemoryAudioBuffer avec le signal resamplé
            audio_buffer = MemoryAudioBuffer(signal=y_resampled, sample_rate=16000)
            audio_doc = AudioDocument(audio=audio_buffer)

            # Appliquer la diarisation et la transcription
            speech_segments = speaker_detector.run([audio_doc.raw_segment])
            transcriptions = transcriber.run(speech_segments)

            # Écrire les transcriptions dans un fichier texte
            with open(chemin_fichier_texte, 'w') as fichier_texte:
                for speech_seg in speech_segments:
                    transcription_attr = speech_seg.attrs.get(label="transcription")[0]
                    fichier_texte.write(f"{transcription_attr.value}\n")

            print(f"Transcription enregistrée : {chemin_fichier_texte}")
        else:
            print(f"Le fichier {chemin_fichier_wav} n'est pas valide ou n'existe pas.")
    else:
        print(f"La transcription de {chemin_fichier_wav} existe déjà : {chemin_fichier_texte}")
