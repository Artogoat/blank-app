import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Modèle Simplifié de Fiscalité Optimale", layout="wide")

# Titre de l'application
st.title("📊 Modèle Simplifié de Fiscalité Optimale")

st.markdown("""
Ce simulateur permet d'analyser l'effet du taux de taxation sur :
- 📈 La croissance du PIB
- 💰 Les recettes fiscales effectives
- 🏦 L'exode fiscal
- ⚖️ Les inégalités (indice de Gini)
""")

# Paramètres globaux du modèle
g_max = 2.5  # Croissance maximale atteignable (%)
tau_opt = 26  # Taux de fiscalité optimisant la croissance (%)
alpha = 0.05  # Sensibilité de la croissance au taux de fiscalité
I_min = 0.25  # Indice de Gini minimal atteignable
S = 0.2  # Sensibilité fiscale aux inégalités
tau_seuil = 35  # Seuil d'exode fiscal (%)
PIB_initial = 100  # PIB initial

# 📌 Ajout des sliders pour ajuster les paramètres
st.sidebar.header("⚙️ Paramètres de Simulation")

tau = st.sidebar.slider("📈 Taux de Taxation (% du PIB)", min_value=10, max_value=50, value=26)
education = st.sidebar.slider("🏫 Budget Éducation (%)", min_value=5, max_value=40, value=27)
sante = st.sidebar.slider("🏥 Budget Santé (%)", min_value=5, max_value=40, value=26)
infrastructure = st.sidebar.slider("🚧 Budget Infrastructures (%)", min_value=5, max_value=30, value=13)
transferts_sociaux = st.sidebar.slider("🤝 Budget Transferts Sociaux (%)", min_value=1, max_value=20, value=5)

# Vérification que la somme des budgets ne dépasse pas 100%
total_budget = education + sante + infrastructure + transferts_sociaux
if total_budget > 100:
    st.sidebar.warning("⚠️ La somme des allocations dépasse 100% des recettes fiscales ! Ajustez les valeurs.")
    st.stop()

# 📌 Calcul des fonctions du modèle simplifié

# Croissance du PIB
g_tau = g_max - alpha * (tau - tau_opt) ** 2

# Indice de Gini
I_tau = I_min + S / (tau - 20) if tau > 20 else 1  # Évite une division par zéro

# Proportion de la base fiscale restante (exode fiscal)
M_tau = 1 - tau / tau_seuil

# Recettes fiscales effectives
R_effectif = max(M_tau * tau * PIB_initial, 0)  # Assurer que R_effectif ≥ 0

# 📊 Affichage des résultats
st.subheader("📊 Résultats de la Simulation")

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(["Croissance du PIB (%)", "Recettes Fiscales (% PIB)", "Indice de Gini", "Exode Fiscal (%)"],
       [g_tau, R_effectif, I_tau, (1 - M_tau) * 100],
       color=['blue', 'green', 'red', 'purple'])

ax.set_ylabel("Valeurs")
ax.set_title("Impact de la Fiscalité sur l'Économie")
st.pyplot(fig)

# 📌 Interprétation des résultats
st.markdown(f"""
- 📈 **Croissance du PIB :** {g_tau:.2f}%  
- 💰 **Recettes fiscales effectives :** {R_effectif:.2f}% du PIB  
- ⚖️ **Indice de Gini (inégalités) :** {I_tau:.2f}  
- 🏦 **Exode Fiscal :** {(1 - M_tau) * 100:.2f}%  
""")

st.markdown("💡 **Que veux-tu améliorer ou tester dans ce modèle ?**")
