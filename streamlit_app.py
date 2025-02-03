import streamlit as st
import numpy as np
import random

# Configuration de la page
st.set_page_config(page_title="Simulation Économique - Banque Centrale", layout="wide")

# Initialisation du jeu
if "year" not in st.session_state:
    st.session_state.year = 2025
    st.session_state.PIB = 1000  # PIB initial (en milliards)
    st.session_state.inflation = 2.0  # Inflation en %
    st.session_state.debt = 500  # Dette publique initiale (milliards)
    st.session_state.tax_rate = 25  # Taux de taxation initial (%)
    st.session_state.budget_allocation = {"Éducation": 25, "Santé": 25, "Infrastructures": 25, "Transferts sociaux": 25}
    st.session_state.events = []
    st.session_state.history = []

# Interface utilisateur
st.title("🏦 Simulation Économique - Banque Centrale")

st.markdown(f"**📅 Année : {st.session_state.year}**")

# Variables économiques actuelles
st.subheader("📊 Indicateurs économiques actuels")
st.markdown(f"- **PIB :** {st.session_state.PIB:.2f} milliards 💰")
st.markdown(f"- **Inflation :** {st.session_state.inflation:.2f}% 📈")
st.markdown(f"- **Dette publique :** {st.session_state.debt:.2f} milliards 💳")
st.markdown(f"- **Taux de taxation :** {st.session_state.tax_rate}% 💸")

# Ajustement des politiques économiques
st.sidebar.header("⚙️ Décisions économiques")
tax_rate = st.sidebar.slider("💰 Taux de taxation (%)", 10, 50, st.session_state.tax_rate)

budget_education = st.sidebar.slider("🏫 Budget Éducation (%)", 0, 50, st.session_state.budget_allocation["Éducation"])
budget_sante = st.sidebar.slider("🏥 Budget Santé (%)", 0, 50, st.session_state.budget_allocation["Santé"])
budget_infra = st.sidebar.slider("🚧 Budget Infrastructures (%)", 0, 50, st.session_state.budget_allocation["Infrastructures"])
budget_transferts = st.sidebar.slider("🤝 Budget Transferts sociaux (%)", 0, 50, st.session_state.budget_allocation["Transferts sociaux"])

# Vérification que le budget total ne dépasse pas 100%
if budget_education + budget_sante + budget_infra + budget_transferts > 100:
    st.sidebar.warning("⚠️ La somme des budgets dépasse 100% ! Ajustez vos valeurs.")
    st.stop()

# Bouton pour appliquer les décisions et passer à l'année suivante
if st.button("📅 Appliquer les décisions et avancer d'une année"):

    # Calcul de la croissance du PIB
    croissance = (tax_rate / 50) * 3  # Hypothèse de croissance liée aux taxes (simplifié)
    croissance += (budget_education + budget_sante + budget_infra) * 0.02  # Contribution des investissements publics

    # Effets de l'inflation et de la dette
    inflation_impact = np.clip(st.session_state.inflation * 0.05, -1, 1)
    dette_impact = np.clip(st.session_state.debt / 1000, -2, 2)
    
    # Calcul final de la croissance économique
    croissance_finale = max(0, croissance - inflation_impact - dette_impact)
    st.session_state.PIB *= (1 + croissance_finale / 100)

    # Mise à jour de l'inflation (impact des budgets et de la dette)
    st.session_state.inflation += (tax_rate - 25) * 0.05 - (budget_education + budget_sante) * 0.02 + dette_impact * 0.1
    st.session_state.inflation = max(0, st.session_state.inflation)  # Évite l'inflation négative

    # Mise à jour de la dette publique (dépenses vs recettes fiscales)
    recettes_fiscales = (tax_rate / 100) * st.session_state.PIB
    depenses = (budget_education + budget_sante + budget_infra + budget_transferts) / 100 * st.session_state.PIB
    st.session_state.debt += depenses - recettes_fiscales

    # Événements aléatoires tous les 10 ans
    if st.session_state.year % 10 == 0:
        events_list = [
            ("📉 Récession mondiale", -2),
            ("💡 Révolution technologique", +2),
            ("💰 Boom des exportations", +3),
            ("🚨 Crise financière", -3),
            ("🏭 Effondrement d'un secteur industriel", -2),
        ]
        event = random.choice(events_list)
        st.session_state.events.append((st.session_state.year, event[0]))
        st.session_state.PIB *= (1 + event[1] / 100)

    # Sauvegarde des décisions
    st.session_state.history.append({
        "Année": st.session_state.year,
        "PIB": st.session_state.PIB,
        "Inflation": st.session_state.inflation,
        "Dette": st.session_state.debt,
        "Taxation": tax_rate,
        "Éducation": budget_education,
        "Santé": budget_sante,
        "Infrastructures": budget_infra,
        "Transferts": budget_transferts
    })

    # Mise à jour des valeurs stockées
    st.session_state.year += 1
    st.session_state.tax_rate = tax_rate
    st.session_state.budget_allocation = {
        "Éducation": budget_education,
        "Santé": budget_sante,
        "Infrastructures": budget_infra,
        "Transferts sociaux": budget_transferts
    }

# 📊 Affichage de l'historique
st.subheader("📜 Historique des décisions économiques")
st.write(st.session_state.history)

# 📢 Affichage des événements économiques
if st.session_state.events:
    st.subheader("⚠️ Événements économiques passés")
    for year, event in st.session_state.events:
        st.markdown(f"**{year}** : {event}")

st.markdown("💡 **Que veux-tu améliorer ou ajouter à ce jeu ?** 🚀")
