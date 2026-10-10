import streamlit as st
import pickle
import numpy as np

with open('gradient_boosting_base_noshow_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.sidebar.title("Tableau de bord")
page = st.sidebar.selectbox("Sélectionnez votre page", ["Accueil", "À propos", "Prédiction"])


if page == "Accueil":
    st.title('🎯 Prédiction des Rendez-vous Médicaux Manqués')

    st.markdown("""
    <style>
    .description {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>

    <div class="description">
    <h2>Description du projet</h2>
    <p>Ce projet prédit si un patient se présentera ou non à son rendez-vous médical en se basant sur ses informations personnelles et médicales.</p>
    </div>
    """, unsafe_allow_html=True)

    from PIL import Image

    try:
        img = Image.open("image.webp")
        st.image(img, caption="Prédiction de présence aux rendez-vous médicaux", use_container_width=True)
    except Exception as e:
        st.error("Erreur lors du chargement de l'image : " + str(e))



elif page == "À propos":
    st.title("ℹ️ À propos du Dataset")
    st.markdown("""
    - **Dataset** : No-show appointments
    - **Source** : Kaggle
    - **Objectif** : Prédire si un patient manquera son rendez-vous médical en fonction de ses caractéristiques personnelles et médicales.

    ### Caractéristiques utilisées :
    - **Scholarship (Aide sociale)** : Indique si le patient bénéficie d'une aide sociale.
    - **Hypertension** : Indique si le patient souffre d'hypertension.
    - **Diabetes** : Indique si le patient souffre de diabète.
    - **Alcoholism** : Indique si le patient souffre d'alcoolisme.
    - **Handcap (Niveau de handicap)** : Indique le niveau de handicap du patient.
    - **SMS_received** : Indique si le patient a reçu un SMS de rappel pour le rendez-vous.
    - **AgeGroup_60andMore (Âge ≥ 60 ans)** : Indique si le patient a 60 ans ou plus.
    - **waiting_days (Délai entre la réservation et la date de RDV)** : Indique le nombre de jours entre la réservation et la date du rendez-vous.
    """)
elif page == "Prédiction":
    st.title("📅 Prédiction de Présence au Rendez-vous")

    col1, col2 = st.columns(2)

    with col1:
        Scholarship = st.selectbox("Bénéficie d'une bourse ?", ["Veuillez sélectionner...", "Non", "Oui"])
        Hipertension = st.selectbox("Hypertension ?", ["Veuillez sélectionner...", "Non", "Oui"])
        Diabetes = st.selectbox("Diabète ?", ["Veuillez sélectionner...", "Non", "Oui"])
        Alcoholism = st.selectbox("Alcoolisme ?", ["Veuillez sélectionner...", "Non", "Oui"])

    with col2:
        Handcap = st.selectbox("Handicap ?", ["Veuillez sélectionner...", "Non", "Oui"])
        SMS_received = st.selectbox("SMS reçu ?", ["Veuillez sélectionner...", "Non", "Oui"])
        AgeGroup_60andMore = st.selectbox("Âge ≥ 60 ans ?", ["Veuillez sélectionner...", "Non", "Oui"])
        waiting_days = st.number_input("Nombre de jours d'attente", min_value=0)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bouton Prédire
    if st.button("Prédire"):
        if "Veuillez sélectionner..." in [Scholarship, Hipertension, Diabetes, Alcoholism,
                                          Handcap, SMS_received, AgeGroup_60andMore]:
            st.error("⚠️ Veuillez sélectionner une option dans chaque champ.")
        else:
            # Encodage binaire
            Scholarship = 1 if Scholarship == "Oui" else 0
            Hipertension = 1 if Hipertension == "Oui" else 0
            Diabetes = 1 if Diabetes == "Oui" else 0
            Alcoholism = 1 if Alcoholism == "Oui" else 0
            SMS_received = 1 if SMS_received == "Oui" else 0
            AgeGroup_60andMore = 1 if AgeGroup_60andMore == "Oui" else 0
            Handcap = 1 if Handcap == "Oui" else 0

            # Préparation des données pour la prédiction
            user_input = np.array([[Scholarship, Hipertension, Diabetes, Alcoholism,
                                    Handcap, SMS_received, AgeGroup_60andMore, waiting_days]])

            prediction = model.predict(user_input)

            if prediction[0] == 'No':
                st.success("✅ Le patient est susceptible de se présenter à son rendez-vous.")
            else:
                st.warning("⚠️ Le patient est susceptible de manquer son rendez-vous.")
