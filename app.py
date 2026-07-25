"""
Application de prédiction d'éligibilité au crédit
====================================================
Modèle : Régression Logistique (scikit-learn)
Variables attendues par le modèle (dans cet ordre) :
Gender, Married, Dependents, Education, Self_Employed,
Property_Area, ApplicantIncome, CoapplicantIncome,
LoanAmount, Loan_Amount_Term, Credit_History
"""

import streamlit as st
import pandas as pd
import pickle
import os

# =========================================================
# 1. CHARGEMENT DU MODÈLE
# =========================================================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model = load_model()

# Ordre exact des colonnes attendu par le modèle (voir model.feature_names_in_)
FEATURE_ORDER = [
    "Gender", "Married", "Dependents", "Education", "Self_Employed",
    "Property_Area", "ApplicantIncome", "CoapplicantIncome",
    "LoanAmount", "Loan_Amount_Term", "Credit_History"
]

# =========================================================
# 2. CONFIGURATION DE LA PAGE
# =========================================================
st.set_page_config(page_title="Éligibilité au crédit", page_icon="🏦", layout="centered")
st.title("🏦 Prédiction d'éligibilité au crédit")
st.write(
    "Renseignez les informations du demandeur ci-dessous pour estimer "
    "s'il est éligible à un prêt."
)

st.divider()

# =========================================================
# 3. FORMULAIRE DE SAISIE
# =========================================================
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Genre", ["Male", "Female"])
    married = st.selectbox("Marié(e) ?", ["Yes", "No"])
    dependents = st.selectbox("Nombre de personnes à charge", ["0", "1", "2", "3+"])
    education = st.selectbox("Niveau d'éducation", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Travailleur indépendant ?", ["Yes", "No"])
    property_area = st.selectbox("Zone de résidence", ["Urban", "Semiurban", "Rural"])

with col2:
    applicant_income = st.number_input("Revenu du demandeur", min_value=0.0, value=5000.0, step=100.0)
    coapplicant_income = st.number_input("Revenu du co-demandeur", min_value=0.0, value=0.0, step=100.0)
    loan_amount = st.number_input("Montant du prêt (en milliers)", min_value=0.0, value=150.0, step=10.0)
    loan_amount_term = st.number_input("Durée du prêt (en jours)", min_value=0.0, value=360.0, step=30.0)
    credit_history = st.selectbox(
        "Historique de crédit",
        options=[1.0, 0.0],
        format_func=lambda x: "Bon historique (1)" if x == 1.0 else "Mauvais / absent (0)"
    )

st.divider()

# =========================================================
# 4. ENCODAGE DES VARIABLES CATÉGORIELLES
#    (à adapter si ton entraînement utilisait un encodage différent)
# =========================================================
def encode_inputs():
    gender_enc = 1 if gender == "Male" else 0
    married_enc = 1 if married == "Yes" else 0
    education_enc = 1 if education == "Graduate" else 0
    self_employed_enc = 1 if self_employed == "Yes" else 0
    property_area_map = {"Rural": 0, "Semiurban": 1, "Urban": 2}
    property_area_enc = property_area_map[property_area]
    dependents_enc = 3 if dependents == "3+" else int(dependents)

    row = {
        "Gender": gender_enc,
        "Married": married_enc,
        "Dependents": dependents_enc,
        "Education": education_enc,
        "Self_Employed": self_employed_enc,
        "Property_Area": property_area_enc,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_amount_term,
        "Credit_History": credit_history,
    }
    return pd.DataFrame([row])[FEATURE_ORDER]

# =========================================================
# 5. PRÉDICTION
# =========================================================
if st.button("Évaluer l'éligibilité", type="primary"):
    X_new = encode_inputs()
    prediction = model.predict(X_new)[0]
    proba = model.predict_proba(X_new)[0]

    st.subheader("Résultat")
    if prediction == 1:
        st.success(f"✅ Éligible au crédit — probabilité : {proba[1]:.1%}")
    else:
        st.error(f"❌ Non éligible au crédit — probabilité de non-éligibilité : {proba[0]:.1%}")

    with st.expander("Voir les données envoyées au modèle"):
        st.dataframe(X_new)

st.caption("Modèle de scoring développé pour AIME - Consultance en statistiques")
