import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Configuration de la page
st.set_page_config(page_title="Simulateur Fiscal", layout="wide")

# Titre du projet
st.title("📊 Simulateur des Effets de la Fiscalité sur l'Économie")

st.markdown("""
    Ce simulateur permet d'analyser l'impact de la fiscalité sur la croissance du PIB, 
    les recettes fiscales, la dette publique et l'inégalité des revenus.
""")

# 📌 **Ajout des sliders pour permettre l'interactivité**
st.sidebar.header("⚙️ Paramètres de Simulation")

tau = st.sidebar.slider("📈 Taux de Taxation (% du PIB)", min_value=10, max_value=50, value=26)
education = st.sidebar.slider("🏫 Budget Éducation (%)", min_value=5, max_value=40, value=27)
sante = st.sidebar.slider("🏥 Budget Santé (%)", min_value=5, max_value=40, value=26)
infrastructure = st.sidebar.slider("🚧 Budget Infrastructures (%)", min_value=5, max_value=30, value=13)
transferts_sociaux = st.sidebar.slider("🤝 Budget Transferts Sociaux (%)", min_value=1, max_value=20, value=5)

# Assurer que la somme ne dépasse pas 100%
total_budget = education + sante + infrastructure + transferts_sociaux
if total_budget > 100:
    st.sidebar.warning("⚠️ La somme des allocations dépasse 100% des recettes fiscales ! Ajustez les valeurs.")
    st.stop()

# 📌 **Définition du modèle de croissance dynamique**
def system(t, y):
    PIB, R, D = y
    R_effectif = tau * PIB  # Recettes fiscales
    croissance = 0.3 * (education / 100) * R_effectif \
               + 0.2 * (sante / 100) * R_effectif \
               + 0.15 * (infrastructure / 100) * R_effectif \
               + 0.1 * (transferts_sociaux / 100) * R_effectif \
               - 0.05 * (tau - 26) ** 2  # Effet négatif si taxation trop élevée
    
    dPIB_dt = PIB * croissance / 100
    dR_dt = R_effectif - 25  # Dépenses publiques fixes pour stabiliser
    dD_dt = 25 - R_effectif  # Dette évoluant en fonction des recettes fiscales
    return [dPIB_dt, dR_dt, dD_dt]

# 📌 **Résolution du modèle sur 50 ans**
t_eval = np.linspace(0, 50, 500)
sol = solve_ivp(system, [0, 50], [100, tau * 100, 50], t_eval=t_eval)

# 📌 **Affichage des résultats sous forme de graphiques interactifs**
st.subheader("📊 Résultats de la Simulation")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(sol.t, sol.y[0], label="📈 PIB", color='b')
ax.plot(sol.t, sol.y[1], label="💰 Recettes fiscales", color='g')
ax.plot(sol.t, sol.y[2], label="📉 Dette publique", color='r')
ax.set_xlabel("Années")
ax.set_ylabel("Valeurs en % du PIB")
ax.set_title("Évolution du PIB, des Recettes Fiscales et de la Dette Publique")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 📌 **Ajout d'une interprétation des résultats**
st.markdown("""
    - 📈 **Un taux de taxation trop élevé (>35%) entraîne une fuite des capitaux et ralentit la croissance.**  
    - 💰 **Un taux inférieur à 22% stimule l’investissement, mais peut creuser la dette.**  
    - 🏫 **Les investissements en éducation et santé augmentent la croissance à long terme.**  
""")

# 📌 **Comparaison avec des pays réels**
st.subheader("🌍 Comparaison avec les Données Réelles")

st.markdown("""
    | Pays       | Taux Fiscal (% PIB) | Croissance du PIB | Dette Publique (% PIB) |
    |------------|--------------------|-------------------|------------------------|
    | 🇫🇷 France | 47%                 | 1.5%              | 112%                   |
    | 🇨🇭 Suisse | 27%                 | 2.0%              | 41%                    |
    | 🇺🇸 USA    | 24%                 | 2.5%              | 98%                    |
""")

st.markdown("Ces chiffres permettent de mieux comprendre les choix fiscaux et leurs impacts à long terme.")

# 📌 **Améliorations possibles**
st.subheader("🚀 Prochaines Améliorations")
st.markdown("""
    - **Ajout de prévisions IA sur les impacts des politiques fiscales.**  
    - **Scénarios de crises économiques et réformes fiscales.**  
    - **Comparaison entre plusieurs stratégies fiscales.**  
""")
