import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Modèle de Fiscalité Optimale", layout="wide")

# Titre de l'application
st.title("📊 Modèle de Fiscalité Optimale")

st.markdown("""
Ce simulateur permet d'analyser l'effet du taux de taxation sur :
- 📈 La croissance du PIB
- 💰 Les recettes fiscales effectives
- 🏦 L'exode fiscal
- ⚖️ Les inégalités (indice de Gini)
- 📊 Prévisions sur 5 ans de l'évolution du PIB et des inégalités
""")

# Paramètres globaux du modèle
g_max = 2.5  # Croissance maximale atteignable (%)
tau_opt = 26  # Taux de fiscalité optimisant la croissance (%)
alpha = 0.05  # Sensibilité de la croissance au taux de fiscalité
I_min = 0.25  # Indice de Gini minimal atteignable
S = 0.2  # Sensibilité fiscale aux inégalités
tau_seuil = 30  # Seuil d'exode fiscal (%)
delta = 0.01  # Sensibilité de la base fiscale à l'exode
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

# 📌 Calcul des fonctions du modèle

# Croissance du PIB
g_tau = g_max - alpha * (tau - tau_opt) ** 2

# Indice de Gini
I_tau = I_min + S / (tau - 20) if tau > 20 else 1  # Évite une division par zéro

# Proportion de la base fiscale restante (exode fiscal) - mise à jour avec la nouvelle équation
M_tau = max(1 - delta * (tau - tau_seuil) ** 2, 0)  # Assurer que M_tau ne devient pas négatif

# Recettes fiscales effectives
R_effectif = max(M_tau * tau * PIB_initial, 0)  # Assurer que R_effectif ≥ 0

# 📊 Affichage des résultats sous forme de 4 graphiques distincts avec échelle fixe
st.subheader("📊 Résultats de la Simulation")

fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Graphique 1 : Croissance du PIB
axs[0, 0].bar(["Croissance du PIB"], [g_tau], color='blue')
axs[0, 0].set_ylim(0, g_max)  # Échelle fixe
axs[0, 0].set_ylabel("Croissance (%)")
axs[0, 0].set_title("📈 Croissance du PIB")

# Graphique 2 : Recettes fiscales
axs[0, 1].bar(["Recettes Fiscales"], [R_effectif], color='green')
axs[0, 1].set_ylim(0, 50)  # Échelle fixe
axs[0, 1].set_ylabel("Recettes (% du PIB)")
axs[0, 1].set_title("💰 Recettes Fiscales")

# Graphique 3 : Indice de Gini (Inégalités)
axs[1, 0].bar(["Indice de Gini"], [I_tau], color='red')
axs[1, 0].set_ylim(0, 1)  # Échelle fixe
axs[1, 0].set_ylabel("Indice de Gini")
axs[1, 0].set_title("⚖️ Inégalités (Indice de Gini)")

# Graphique 4 : Exode Fiscal
axs[1, 1].bar(["Exode Fiscal"], [(1 - M_tau) * 100], color='purple')
axs[1, 1].set_ylim(0, 100)  # Échelle fixe
axs[1, 1].set_ylabel("Exode Fiscal (%)")
axs[1, 1].set_title("🏦 Exode Fiscal")

plt.tight_layout()
st.pyplot(fig)

# 📈 Prévisions sur 5 ans de l'évolution du PIB et des inégalités
st.subheader("📊 Prévisions sur 5 ans")

years = np.arange(0, 6)  # Période de prévision
PIB_evolution = PIB_initial * (1 + g_tau / 100) ** years  # Projection du PIB avec croissance
I_evolution = I_tau - 0.01 * years  # Hypothèse d'amélioration des inégalités

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years, PIB_evolution, label="📈 PIB", color='blue', marker='o')
ax.set_xlabel("Années")
ax.set_ylabel("PIB")
ax.set_title("Évolution du PIB sur 5 ans")
ax.legend()
ax.grid(True)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years, I_evolution, label="⚖️ Indice de Gini", color='red', marker='o')
ax.set_xlabel("Années")
ax.set_ylabel("Indice de Gini")
ax.set_title("Évolution des Inégalités sur 5 ans")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 📌 Interprétation des résultats
st.markdown(f"""
- 📈 **Croissance du PIB :** {g_tau:.2f}%  
- 💰 **Recettes fiscales effectives :** {R_effectif:.2f}% du PIB  
- ⚖️ **Indice de Gini (inégalités) :** {I_tau:.2f}  
- 🏦 **Exode Fiscal :** {(1 - M_tau) * 100:.2f}%  
""")

st.markdown("💡 **Que veux-tu améliorer ou tester dans ce modèle ?**")
