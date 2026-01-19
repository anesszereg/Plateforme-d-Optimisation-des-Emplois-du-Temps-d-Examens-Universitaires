import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.analytics import Analytics
from src.session import require_auth, show_user_sidebar

st.set_page_config(
    page_title="Vice-Doyen - Vue Strategique",
    page_icon="",
    layout="wide"
)

# Authentication - only vice_doyen can access
require_auth(allowed_roles=['vice_doyen'])
show_user_sidebar()

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_analytics(_db):
    return Analytics(_db)

def main():
    st.title("Espace Vice-Doyen / Doyen")
    st.markdown("**Vue stratégique et globale du système de planification**")
    
    db = get_database()
    analytics = get_analytics(db)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "KPIs & Indicateurs",
        "Occupation Salles",
        "Conflits par Departement",
        "Validation EDT"
    ])
    
    with tab1:
        st.header("Indicateurs Cles de Performance")
        
        try:
            kpis = analytics.get_dashboard_kpis()
            if not kpis or not isinstance(kpis, dict):
                kpis = {}
            
            total_etudiants = int(kpis.get('total_etudiants', 0) or 0)
            total_professeurs = int(kpis.get('total_professeurs', 0) or 0)
            total_departements = int(kpis.get('total_departements', 0) or 0)
            examens_planifies = int(kpis.get('examens_planifies', 0) or 0)
            total_formations = int(kpis.get('total_formations', 0) or 0)
            total_modules = int(kpis.get('total_modules', 0) or 0)
            total_salles = int(kpis.get('total_salles', 0) or 0)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Etudiants", f"{total_etudiants:,}")
            with col2:
                st.metric("Professeurs", f"{total_professeurs:,}")
            with col3:
                st.metric("Departements", total_departements)
            with col4:
                st.metric("Examens planifies", examens_planifies)
            
            st.markdown("---")
            
            col5, col6, col7, col8 = st.columns(4)
            with col5:
                st.metric("Formations", total_formations)
            with col6:
                st.metric("Modules", total_modules)
            with col7:
                st.metric("Salles", total_salles)
            with col8:
                ratio = total_etudiants / max(total_professeurs, 1)
                st.metric("Ratio Etu/Prof", f"{ratio:.1f}")
            
            # Efficiency score
            st.markdown("---")
            periodes = db.get_periodes_examen(actif=True)
            if periodes:
                periode_id = periodes[0]['id']
                efficiency = analytics.calculate_efficiency_score(periode_id)
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    score = efficiency.get('score', 0)
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        title={'text': "Score d'Efficacité"},
                        gauge={'axis': {'range': [0, 100]},
                               'bar': {'color': "green" if score >= 70 else "orange" if score >= 50 else "red"}}
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_e2:
                    metrics = efficiency.get('metrics', {})
                    st.metric("Taux d'utilisation", f"{metrics.get('utilization_rate', 0):.1f}%")
                    st.metric("Taux de conflits", f"{metrics.get('conflict_rate', 0):.1f}%")
                    st.metric("Examens/jour moyen", f"{metrics.get('avg_exams_per_day', 0):.1f}")
        
        except Exception:
            st.info("Donnees en cours de chargement...")
    
    with tab2:
        st.header("Occupation des Salles et Amphitheatres")
        
        try:
            occupation = analytics.get_occupation_analysis()
            
            if not occupation.empty:
                fig = px.bar(
                    occupation,
                    x='date_examen',
                    y='taux_occupation_pct',
                    title="Taux d'occupation par jour",
                    labels={'taux_occupation_pct': 'Taux (%)', 'date_examen': 'Date'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(occupation, use_container_width=True, hide_index=True)
            else:
                st.info("Aucune donnée d'occupation disponible")
        
        except Exception:
            st.info("Donnees d'occupation non disponibles")
    
    with tab3:
        st.header("Analyse des Conflits par Departement")
        
        try:
            dept_stats = analytics.get_department_stats()
            
            if not dept_stats.empty:
                fig = px.bar(
                    dept_stats,
                    x='departement',
                    y='nb_examens_planifies',
                    color='departement',
                    title="Examens par Département"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(dept_stats, use_container_width=True, hide_index=True)
            else:
                st.info("Aucune statistique départementale disponible")
            
            # Conflict summary
            conflict_summary = analytics.get_conflict_summary()
            st.markdown("---")
            st.subheader("Resume des Conflits")
            
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            with col_c1:
                st.metric("Conflits Étudiants", conflict_summary.get('etudiants', 0))
            with col_c2:
                st.metric("Conflits Professeurs", conflict_summary.get('professeurs', 0))
            with col_c3:
                st.metric("Conflits Capacité", conflict_summary.get('capacite', 0))
            with col_c4:
                st.metric("Conflits Salles", conflict_summary.get('salles', 0))
        
        except Exception:
            st.info("Statistiques en cours de calcul...")
    
    with tab4:
        st.header("Validation Finale des EDT")
        
        st.warning("**Zone de validation finale** - Responsabilité du Vice-Doyen/Doyen")
        
        periodes = db.get_periodes_examen(actif=True)
        
        if periodes:
            periode_options = {f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] for p in periodes}
            selected = st.selectbox("Période à valider", list(periode_options.keys()))
            periode_id = periode_options[selected]
            
            try:
                kpis = analytics.get_dashboard_kpis()
                conflicts = analytics.get_conflict_summary()
                efficiency = analytics.calculate_efficiency_score(periode_id)
                
                col_v1, col_v2, col_v3 = st.columns(3)
                with col_v1:
                    st.metric("Examens planifiés", kpis.get('examens_planifies', 0))
                with col_v2:
                    total_conflicts = sum(conflicts.values())
                    st.metric("Total conflits", total_conflicts)
                with col_v3:
                    st.metric("Score efficacité", f"{efficiency.get('score', 0):.1f}/100")
                
                st.markdown("---")
                
                check1 = st.checkbox("J'ai vérifié l'occupation des salles")
                check2 = st.checkbox("J'ai vérifié les conflits par département")
                check3 = st.checkbox("J'ai vérifié la charge des enseignants")
                check4 = st.checkbox("EDT conforme aux objectifs institutionnels")
                
                all_checked = check1 and check2 and check3 and check4
                
                if st.button("Valider l'EDT", type="primary", disabled=not all_checked, use_container_width=True):
                    st.success(f"EDT valide par le Vice-Doyen/Doyen le {datetime.now().strftime('%d/%m/%Y a %H:%M')}")
                
                if not all_checked:
                    st.info("Cochez toutes les cases pour activer la validation")
            
            except Exception:
                st.info("Validation en attente de donnees...")
        else:
            st.warning("Aucune période d'examen active")

if __name__ == "__main__":
    main()
