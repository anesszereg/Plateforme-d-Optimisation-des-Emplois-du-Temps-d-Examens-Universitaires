import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import Database
from src.analytics import Analytics
from src.scheduler import ExamScheduler

st.set_page_config(
    page_title="Plateforme d'Optimisation des Examens",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_analytics(_db):
    return Analytics(_db)

@st.cache_resource
def get_scheduler(_db):
    return ExamScheduler(_db)

def main():
    st.markdown('<div class="main-header">🎓 Plateforme d\'Optimisation des Emplois du Temps d\'Examens</div>', unsafe_allow_html=True)
    
    db = get_database()
    analytics = get_analytics(db)
    
    st.sidebar.title("📋 Navigation")
    st.sidebar.info("Utilisez les pages dans le menu pour accéder aux différentes fonctionnalités")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Rôles disponibles")
    st.sidebar.markdown("""
    - **Administration** : Génération d'EDT
    - **Statistiques** : Vue stratégique
    - **Départements** : Gestion départementale
    - **Consultation** : Planning personnel
    """)
    
    st.header("📊 Tableau de Bord Global")
    
    try:
        kpis = analytics.get_dashboard_kpis()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="👨‍🎓 Étudiants",
                value=f"{kpis.get('total_etudiants', 0):,}",
                delta="Total inscrits"
            )
        
        with col2:
            st.metric(
                label="👨‍🏫 Professeurs",
                value=f"{kpis.get('total_professeurs', 0):,}",
                delta="Corps enseignant"
            )
        
        with col3:
            st.metric(
                label="📚 Modules",
                value=f"{kpis.get('total_modules', 0):,}",
                delta="Enseignements"
            )
        
        with col4:
            st.metric(
                label="📝 Inscriptions",
                value=f"{kpis.get('total_inscriptions', 0):,}",
                delta="Total"
            )
        
        st.markdown("---")
        
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            st.metric(
                label="🏛️ Départements",
                value=kpis.get('total_departements', 0)
            )
        
        with col6:
            st.metric(
                label="🎯 Formations",
                value=kpis.get('total_formations', 0)
            )
        
        with col7:
            st.metric(
                label="🏫 Salles",
                value=kpis.get('total_salles', 0)
            )
        
        with col8:
            st.metric(
                label="💺 Capacité totale",
                value=f"{kpis.get('capacite_totale', 0):,}"
            )
        
        st.markdown("---")
        
        st.subheader("📈 Statistiques par Département")
        
        dept_stats = analytics.get_department_stats()
        
        if not dept_stats.empty:
            col_left, col_right = st.columns(2)
            
            with col_left:
                fig_students = px.bar(
                    dept_stats,
                    x='departement',
                    y='nb_etudiants',
                    title='Répartition des Étudiants par Département',
                    labels={'nb_etudiants': 'Nombre d\'étudiants', 'departement': 'Département'},
                    color='nb_etudiants',
                    color_continuous_scale='Blues'
                )
                fig_students.update_layout(showlegend=False)
                st.plotly_chart(fig_students, use_container_width=True)
            
            with col_right:
                fig_profs = px.bar(
                    dept_stats,
                    x='departement',
                    y='nb_professeurs',
                    title='Nombre de Professeurs par Département',
                    labels={'nb_professeurs': 'Nombre de professeurs', 'departement': 'Département'},
                    color='nb_professeurs',
                    color_continuous_scale='Greens'
                )
                fig_profs.update_layout(showlegend=False)
                st.plotly_chart(fig_profs, use_container_width=True)
            
            st.dataframe(
                dept_stats,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Aucune statistique disponible pour le moment")
        
        st.markdown("---")
        
        st.subheader("🔍 Détection de Conflits")
        
        conflict_summary = analytics.get_conflict_summary()
        
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        
        with col_c1:
            st.metric(
                label="⚠️ Conflits Étudiants",
                value=conflict_summary.get('etudiants', 0),
                delta="Examens multiples/jour"
            )
        
        with col_c2:
            st.metric(
                label="⚠️ Conflits Professeurs",
                value=conflict_summary.get('professeurs', 0),
                delta=">3 examens/jour"
            )
        
        with col_c3:
            st.metric(
                label="⚠️ Conflits Capacité",
                value=conflict_summary.get('capacite', 0),
                delta="Salles surchargées"
            )
        
        with col_c4:
            st.metric(
                label="⚠️ Conflits Salles",
                value=conflict_summary.get('salles', 0),
                delta="Chevauchements"
            )
        
        total_conflicts = sum(conflict_summary.values())
        if total_conflicts == 0:
            st.success("✅ Aucun conflit détecté dans le planning actuel!")
        else:
            st.warning(f"⚠️ {total_conflicts} conflit(s) détecté(s). Consultez la page Administration pour plus de détails.")
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {e}")
        st.info("💡 Assurez-vous que la base de données est initialisée et contient des données.")
        st.code("""
# Pour initialiser la base de données:
python scripts/init_database.py

# Pour générer les données de test:
python scripts/generate_data.py
        """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ À propos")
    st.sidebar.info("""
    **Version**: 1.0.0
    
    **Technologies**:
    - PostgreSQL
    - Python
    - Streamlit
    
    **Objectif**: Génération automatique d'emplois du temps d'examens en <45 secondes
    """)

if __name__ == "__main__":
    main()
