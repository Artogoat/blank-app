import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Configuration de la page
st.set_page_config(page_title="Simulateur Fiscal", layout="wide")

# Titre du projet
st.title("📊 Simulateur des Effets de la Fiscalité sur l'Économie")

st.markdown(
    """
    Ce simulateur permet d'analyser l'impact de la fiscalité sur la croissance du PIB, 
    les recettes fiscales, la dette publique et l'inégalité des revenus.
    """
)

# Sidebar pour les paramètres
st.sidebar.header("Paramètres de Simulation")

# Sliders pour ajuster les variables fiscales
tau = st.sidebar.slider("📈 Taux de Fiscalité (% du PIB)", min_value=10, max_value=50, value=26)
gamma = st.sidebar.slider("💰 Élasticité de l'exode fiscal", min_value=0.1, max_value=2.0, value=0.5)
education = st.sidebar.slider("🏫 Budget alloué à l'éducation (%)", min_value=10, max_value=40, value=27)
sante = st.sidebar.slider("🏥 Budget alloué à la santé (%)", min_value=10, max_value=40, value=26)

# Définition du modèle de croissance dynamique
def M(tau):
    return 1 / (1 + np.exp(gamma * (tau - 35))) - 1 / (1 + np.exp(gamma * (22 - tau)))

def system(t, y):
    PIB, R, D = y
    M_tau = M(tau)
    R_effectif = tau * PIB * M_tau
    croissance = 0.3 * (education/100) * R_effectif + 0.2 * (sante/100) * R_effectif - 0.05 * (tau - 26) ** 2
    return [PIB * croissance / 100, R_effectif - 25, 25 - R_effectif]

# Résolution du modèle sur 50 ans
t_eval = np.linspace(0, 50, 500)
sol = solve_ivp(system, [0, 50], [100, tau * 100, 50], t_eval=t_eval)

# Affichage des résultats sous forme de graphiques interactifs
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

# Ajout de commentaires d'interprétation
st.markdown(
    """
    - 📈 **Un taux de fiscalité trop élevé (>35%) entraîne une fuite des capitaux et une stagnation de la croissance.**  
    - 💰 **Un taux inférieur à 22% stimule l’attraction des investissements, mais peut créer un déficit budgétaire.**  
    - 🏫 **Les investissements dans l’éducation et la santé augmentent la croissance à long terme.**  
    """
)

# Ajout d'une section pour comparer avec des pays réels
st.subheader("🌍 Comparaison avec les Données Réelles")

st.markdown(
    """
    | Pays       | Taux Fiscal (% PIB) | Croissance du PIB | Dette Publique (% PIB) |
    |------------|--------------------|-------------------|------------------------|
    | 🇫🇷 France | 47%                 | 1.5%              | 112%                   |
    | 🇨🇭 Suisse | 27%                 | 2.0%              | 41%                    |
    | 🇺🇸 USA    | 24%                 | 2.5%              | 98%                    |
    """
)

st.markdown("Ces chiffres permettent de mieux comprendre les choix fiscaux et leurs impacts à long terme.")

# Proposition d'amélioration du modèle
st.subheader("🚀 Prochaines Améliorations")
st.markdown(
    """
    - **Intégration de données en temps réel via l'API OCDE/FMI.**  
    - **Ajout de scénarios économiques (crises, réformes fiscales).**  
    - **Personnalisation avancée pour comparer plusieurs pays.**  
    """
)

st.markdown("💡 **Que veux-tu améliorer ou ajouter à ce simulateur ?**")
