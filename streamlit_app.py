import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt

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
    st.session_state.poor_happiness = 50  # Satisfaction des pauvres
    st.session_state.rich_happiness = 50  # Satisfaction des riches
    st.session_state.consecutive_happy_years = 0  # Années satisfaction continue
    st.session_state.deflation_years = 0  # Années consécutives de déflation

# Interface utilisateur
st.title("🏦 Simulation Économique - Banque Centrale")

st.markdown(f"**📅 Année : {st.session_state.year}**")

# Vérification des conditions de victoire et de défaite
debt_ratio = st.session_state.debt / st.session_state.PIB

if debt_ratio > 200:
    st.error("💀 GAME OVER : Votre dette est supérieure à 200 fois votre PIB !")
    st.stop()
elif st.session_state.inflation > 8:
    st.error("🔥 GAME OVER : L'inflation a dépassé 8% ! Hyperinflation incontrôlable !")
    st.stop()
elif st.session_state.deflation_years >= 2:
    st.error("❄️ GAME OVER : Deux années consécutives de déflation !")
    st.stop()
elif st.session_state.PIB >= 2000 and debt_ratio <= 0.5:
    st.success("🎉 VICTOIRE : Vous avez doublé votre PIB initial avec un endettement ≤ 50% !")
    st.stop()

# Variables économiques actuelles
st.subheader("📊 Indicateurs économiques actuels")
st.markdown(f"- **PIB :** {st.session_state.PIB:.2f} milliards 💰")
st.markdown(f"- **Inflation :** {st.session_state.inflation:.2f}% 📈")
st.markdown(f"- **Dette publique :** {st.session_state.debt:.2f} milliards 💳")
st.markdown(f"- **Taux d'endettement :** {debt_ratio:.2f}x du PIB")
st.markdown(f"- **Taux de taxation :** {st.session_state.tax_rate}% 💸")
st.markdown(f"- **Satisfaction des pauvres :** {st.session_state.poor_happiness}/100 😊")
st.markdown(f"- **Satisfaction des riches :** {st.session_state.rich_happiness}/100 🏦")

# Ajustement des politiques économiques
st.sidebar.header("⚙️ Décisions économiques")
tax_rate = st.sidebar.slider("💰 Taux de taxation (%)", 10, 50, st.session_state.tax_rate)

budget_education = st.sidebar.slider("🏫 Budget Éducation (%)", 0, 50, st.session_state.budget_allocation["Éducation"])
budget_sante = st.sidebar.slider("🏥 Budget Santé (%)", 0, 50, st.session_state.budget_allocation["Santé"])
budget_infra = st.sidebar.slider("🚧 Budget Infrastructures (%)", 0, 50, st.session_state.budget_allocation["Infrastructures"])
budget_transferts = st.sidebar.slider("🤝 Budget Transferts sociaux (%)", 0, 50, st.session_state.budget_allocation["Transferts sociaux"])

adjust_rate = st.sidebar.slider("💹 Ajustement des taux d'intérêt (%)", -5, 5, 0)  # Nouvelle option pour gérer l'inflation

# Vérification que le budget total ne dépasse pas 100%
if budget_education + budget_sante + budget_infra + budget_transferts > 100:
    st.sidebar.warning("⚠️ La somme des budgets dépasse 100% ! Ajustez vos valeurs.")
    st.stop()

# Bouton pour appliquer les décisions et passer à l'année suivante
if st.button("📅 Appliquer les décisions et avancer d'une année"):

    # Croissance du PIB retardée par les investissements
    croissance = (tax_rate / 50) * 3
    croissance += (st.session_state.budget_allocation["Éducation"] * 0.005)  # L'éducation a un effet retardé
    croissance += (budget_sante + budget_infra) * 0.02

    # Effets de l'inflation et de la dette
    inflation_impact = np.clip(st.session_state.inflation * 0.05, -1, 1)
    dette_impact = np.clip(st.session_state.debt / 1000, -2, 2)

    # Mise à jour de la croissance économique
    croissance_finale = max(0, croissance - inflation_impact - dette_impact)
    st.session_state.PIB *= (1 + croissance_finale / 100)

    # Mise à jour de l'inflation avec ajustement des taux
    st.session_state.inflation += (tax_rate - 25) * 0.05 - (budget_sante * 0.02) + dette_impact * 0.1 - adjust_rate * 0.1
    st.session_state.inflation = max(0, st.session_state.inflation)

    # Vérification de la déflation
    if st.session_state.inflation == 0:
        st.session_state.deflation_years += 1
    else:
        st.session_state.deflation_years = 0

    # Sauvegarde des décisions
    st.session_state.history.insert(0, {
        "Année": st.session_state.year,
        "PIB": st.session_state.PIB,
        "Inflation": st.session_state.inflation,
        "Dette": st.session_state.debt,
        "Taux d'endettement": debt_ratio,
        "Taxation": tax_rate,
        "Éducation": budget_education,
        "Santé": budget_sante,
        "Infrastructures": budget_infra,
        "Transferts sociaux": budget_transferts,
        "Taux d'intérêt ajusté": adjust_rate,
        "Satisfaction Pauvres": st.session_state.poor_happiness,
        "Satisfaction Riches": st.session_state.rich_happiness,
        "Années satisfaction continue": st.session_state.consecutive_happy_years
    })

    st.session_state.year += 1

# 📊 Graphique de l'évolution du PIB et de l'inflation
st.subheader("📊 Évolution économique")

years = [entry["Année"] for entry in st.session_state.history]
pib_values = [entry["PIB"] for entry in st.session_state.history]
inflation_values = [entry["Inflation"] for entry in st.session_state.history]

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.set_xlabel("Années")
ax1.set_ylabel("PIB (milliards)", color="blue")
ax1.plot(years, pib_values, label="📈 PIB", color='blue', marker='o')
ax1.tick_params(axis='y', labelcolor="blue")

ax2 = ax1.twinx()
ax2.set_ylabel("Inflation (%)", color="red")
ax2.plot(years, inflation_values, label="📉 Inflation", color='red', marker='s')
ax2.tick_params(axis='y', labelcolor="red")

fig.tight_layout()
st.pyplot(fig)
