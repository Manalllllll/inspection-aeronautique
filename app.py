import streamlit as st
from ultralytics import YOLO
from PIL import Image
from gtts import gTTS
import speech_recognition as sr
import os
import tempfile
import base64
from io import BytesIO
import re
import datetime

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="Inspection Aéronautique ✈️",
    page_icon="✈️",
    layout="wide"
)

# ===== TITRE =====
st.title("✈️ Inspection de Pièces Aéronautiques")
st.write("**YaneCode Academy — Projet de Manal Fartah**")
st.divider()

# ===== CHARGER LE MODÈLE =====
@st.cache_resource
def load_model():
    return YOLO('model/best.pt')

model = load_model()

# ===== FONCTION AUDIO HTML5 =====
def text_to_audio_html(texte, auto_play=True):
    try:
        text_clean = re.sub(r'[^\w\s.,!?:;%\-]', '', texte)
        tts = gTTS(text=text_clean, lang='fr', slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode()
        autoplay = "autoplay" if auto_play else ""
        audio_html = f"""
        <audio {autoplay} controls style="width: 100%;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        return audio_html
    except Exception as e:
        st.error(f"❌ Erreur audio: {str(e)}")
        return None

# ===== FONCTION CHATBOT =====
def chatbot_reponse(question, contexte_defaut=""):
    question = question.lower()
    
    if "fissure" in question or "défaut" in question or "defaut" in question:
        return """🔧 Une fissure sur une pièce aéronautique est très sérieuse !
        
Elle peut être causée par :
- La fatigue du métal
- Les vibrations répétées  
- La corrosion
- Les chocs mécaniques

Action recommandée : Retirer immédiatement la pièce du service et contacter l'équipe de maintenance."""

    elif "réparer" in question or "reparer" in question:
        return """🛠️ Procédure de réparation :
        
1. Isoler la pièce défectueuse
2. Documenter le défaut (photos, rapport)
3. Évaluer la gravité (mineur/modéré/critique)
4. Choisir la méthode : réparation ou remplacement
5. Valider par un inspecteur certifié
6. Tester avant remise en service"""

    elif "dangereux" in question or "danger" in question or "risque" in question:
        return """⚠️ Niveau de danger :
        
🔴 CRITIQUE : Fissure sur pièce structurelle → Vol interdit
🟡 MODÉRÉ : Défaut de surface mineur → Surveillance renforcée  
🟢 FAIBLE : Légère corrosion superficielle → Traitement préventif

Votre pièce nécessite une évaluation par un expert certifié."""

    elif "corrosion" in question:
        return """🔬 La corrosion aéronautique :
        
Types principaux :
- Corrosion galvanique (2 métaux différents)
- Corrosion par piqûres (aluminium)
- Corrosion sous contrainte

Traitement : Nettoyage chimique + protection + inspection NDT"""

    elif "rapport" in question:
        return """📋 Le rapport d'inspection contient :
        
1. Date et heure de l'inspection
2. Référence de la pièce (P/N, S/N)
3. Type de défaut détecté
4. Niveau de confiance de l'IA
5. Décision recommandée
6. Signature de l'inspecteur"""

    elif "bonjour" in question or "salut" in question or "hello" in question:
        return """👋 Bonjour ! Je suis votre expert en maintenance aéronautique.

Je peux vous aider sur :
✈️ Les types de défauts aéronautiques
🔧 Les procédures de réparation
📋 L'interprétation des rapports
⚠️ Les niveaux de danger

Posez-moi votre question !"""

    else:
        return """🤖 Je suis l'assistant expert en inspection aéronautique.

Je peux répondre à vos questions sur :
- Les fissures et défauts
- Les procédures de réparation  
- Les niveaux de danger
- La corrosion
- Les rapports d'inspection

Reformulez votre question avec ces mots clés 😊"""

# ===== FONCTION RAPPORT =====
def generer_rapport(defaut, confiance):
    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    if defaut == "Positive":
        rapport = f"""
RAPPORT D INSPECTION AERONAUTIQUE
=====================================
Date : {now}
Resultat : DEFAUT DETECTE
Type : Fissure et Anomalie de surface
Confiance : {confiance:.1f}%
Niveau de risque : ELEVE
Decision : PIECE A REPARER IMMEDIATEMENT
Action : Retirer la piece du service
et proceder a une inspection approfondie.
====================================="""
    else:
        rapport = f"""
RAPPORT D INSPECTION AERONAUTIQUE
=====================================
Date : {now}
Resultat : PIECE EN BON ETAT
Type : Surface saine
Confiance : {confiance:.1f}%
Niveau de risque : FAIBLE
Decision : PIECE ACCEPTABLE
Action : La piece peut etre utilisee
normalement en service.
====================================="""
    return rapport

# ===== LAYOUT =====
col_gauche, col_droite = st.columns([1, 1])

# ===== COLONNE GAUCHE =====
with col_gauche:
    st.subheader("📸 Upload & Analyse")
    
    photo = st.file_uploader(
        "Choisissez une image de pièce...",
        type=['jpg', 'jpeg', 'png']
    )
    
    if photo is not None:
        image = Image.open(photo)
        st.image(image, caption="Photo uploadée", width=400)
        
        if st.button("🔍 Analyser la pièce", type="primary"):
            with st.spinner("⏳ L'IA analyse..."):
                results = model.predict(image, conf=0.5)
                defaut = results[0].names[results[0].probs.top1]
                confiance = results[0].probs.top1conf.item() * 100
            
            # Sauvegarder TOUT dans session_state
            st.session_state['defaut'] = defaut
            st.session_state['confiance'] = confiance
            st.session_state['rapport'] = generer_rapport(defaut, confiance)
            st.session_state['analyse_faite'] = True

    # Afficher résultats TOUJOURS si analyse faite
    if st.session_state.get('analyse_faite'):
        defaut = st.session_state['defaut']
        confiance = st.session_state['confiance']
        rapport = st.session_state['rapport']

        if defaut == "Positive":
            st.error("⚠️ DÉFAUT DÉTECTÉ !")
            c1, c2, c3 = st.columns(3)
            c1.metric("Type", "Fissure")
            c2.metric("Confiance", f"{confiance:.1f}%")
            c3.metric("Décision", "À RÉPARER")
        else:
            st.success("✅ PIÈCE EN BON ÉTAT !")
            c1, c2, c3 = st.columns(3)
            c1.metric("Type", "Saine")
            c2.metric("Confiance", f"{confiance:.1f}%")
            c3.metric("Décision", "ACCEPTABLE")

        st.subheader("📋 Rapport automatique :")
        st.code(rapport)

        if st.button("🔊 Écouter le rapport", key="btn_audio_rapport"):
            with st.spinner("🎵 Génération audio..."):
                audio_html = text_to_audio_html(rapport, auto_play=True)
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
                    st.success("✅ Audio généré !")

# ===== COLONNE DROITE =====
with col_droite:
    st.subheader("💬 Chatbot Expert Aéronautique")
    
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    for msg in st.session_state['messages']:
        if msg['role'] == 'user':
            st.chat_message("user").write(msg['content'])
        else:
            st.chat_message("assistant").write(msg['content'])
    
    question = st.chat_input("Posez votre question...")
    
    if question:
        st.session_state['messages'].append({
            'role': 'user', 
            'content': question
        })
        st.chat_message("user").write(question)
        
        contexte = f"Défaut: {st.session_state['defaut']}" if 'defaut' in st.session_state else ""
        reponse = chatbot_reponse(question, contexte)
        
        st.session_state['messages'].append({
            'role': 'assistant', 
            'content': reponse
        })
        st.chat_message("assistant").write(reponse)
        st.session_state['derniere_reponse'] = reponse
    
    # Bouton écouter réponse
    if 'derniere_reponse' in st.session_state:
        if st.button("🔊 Écouter la réponse", key="btn_audio_chat"):
            with st.spinner("🎵 Génération audio..."):
                audio_html = text_to_audio_html(
                    st.session_state['derniere_reponse'],
                    auto_play=True
                )
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)

    st.divider()

    # ===== DÉTECTION VOCALE =====
    st.subheader("🎤 Parler avec le chatbot")
    if st.button("🎤 Enregistrer ma voix", key="btn_micro"):
        with st.spinner("🎤 Parlez maintenant..."):
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    st.info("🎤 Parlez maintenant (5 secondes max)...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    texte_voix = r.recognize_google(audio, language='fr-FR')
                    st.success(f"🎙️ Vous avez dit : **{texte_voix}**")
                    
                    contexte = f"Défaut: {st.session_state['defaut']}" if 'defaut' in st.session_state else ""
                    reponse = chatbot_reponse(texte_voix, contexte)
                    st.chat_message("assistant").write(reponse)
                    
                    audio_html = text_to_audio_html(reponse, auto_play=True)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                        
            except sr.WaitTimeoutError:
                st.warning("⏰ Délai dépassé. Réessayez.")
            except sr.UnknownValueError:
                st.error("❌ Je n'ai pas compris. Réessayez.")
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")

# ===== TEST AUDIO =====
st.divider()
col_test1, col_test2, col_test3 = st.columns([1, 2, 1])
with col_test2:
    if st.button("🎧 Tester l'audio", use_container_width=True):
        test_msg = "Test audio. Si vous entendez ce message, le système fonctionne correctement."
        with st.spinner("Test en cours..."):
            audio_html = text_to_audio_html(test_msg, auto_play=True)
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
                st.success("✅ Test réussi !")

st.divider()
st.caption("YaneCode Academy · ENSA Safi · Avril 2026")