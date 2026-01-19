import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.analytics import Analytics
from src.session import require_auth, show_user_sidebar, get_current_user

st.set_page_config(
    page_title="Chef de Département",
    page_icon="",
    layout="wide"
)

# Authentication - only chef_departement can access
require_auth(allowed_roles=['chef_departement'])
show_user_sidebar()

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_analytics(_db):
    return Analytics(_db)

def main():
    st.title(" Espace Chef de Département")
    st.markdown("**Validation EDT, statistiques et analyse des conflits par formation**")
    
    db = get_database()
    analytics = get_analytics(db)
    
    # Get user's department
    user = get_current_user()
    user_dept_id = user.get('departement_id') if user else None
    
    # Department selector (filtered to user's dept if chef_departement)
    departements = db.get_departements()
    
    if user_dept_id:
        # Filter to user's department only
        dept_options = {d['nom']: d['id'] for d in departements if d['id'] == user_dept_id}
        if not dept_options:
            dept_options = {d['nom']: d['id'] for d in departements}
    else:
        dept_options = {d['nom']: d['id'] for d in departements}
    
    selected_dept = st.selectbox("Département", list(dept_options.keys()))
    dept_id = dept_options[selected_dept]
    
    tab1, tab2, tab3, tab4 = st.tabs([
        " Vue d'ensemble",
        "📚 Formations",
        " Conflits",
        " Validation EDT"
    ])
    
    with tab1:
        st.header(f" Statistiques - {selected_dept}")
        
        # Department stats
        formations = db.get_formations(dept_id)
        profs = db.get_professeurs(dept_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Formations", len(formations) if formations else 0)
        with col2:
            st.metric(" Professeurs", len(profs) if profs else 0)
        with col3:
            # Count students in department
            students = db.execute_query("""
                SELECT COUNT(*) as count FROM etudiants e
                JOIN formations f ON e.formation_id = f.id
                WHERE f.dept_id = %s
            """, (dept_id,))
            st.metric(" Étudiants", students[0]['count'] if students else 0)
        
        st.markdown("---")
        
        # Formations breakdown
        if formations:
            st.subheader("📚 Répartition par Formation")
            df = pd.DataFrame(formations)
            fig = px.bar(df, x='nom', y='nb_modules', color='niveau', title="Modules par Formation")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("📚 Formations du Département")
        
        formations = db.get_formations(dept_id)
        
        if formations:
            for f in formations:
                with st.expander(f" {f['nom']} ({f['niveau']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Code:** {f['code']}")
                        st.write(f"**Niveau:** {f['niveau']}")
                    with col2:
                        st.write(f"**Modules:** {f['nb_modules']}")
                    
                    # Get modules for this formation
                    modules = db.execute_query(
                        "SELECT * FROM modules WHERE formation_id = %s ORDER BY semestre, nom",
                        (f['id'],)
                    )
                    if modules:
                        st.dataframe(pd.DataFrame(modules)[['nom', 'code', 'credits', 'semestre', 'duree_examen']], 
                                   use_container_width=True, hide_index=True)
        else:
            st.info("Aucune formation dans ce département")
    
    with tab3:
        st.header(" Conflits par Formation")
        
        # Get conflicts for department
        conflits_etu = db.get_conflits_etudiants()
        
        if conflits_etu:
            # Filter by department (through formations)
            df = pd.DataFrame(conflits_etu)
            st.warning(f" {len(df)} conflits étudiants détectés")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.success(" Aucun conflit détecté")
    
    with tab4:
        st.header(" Validation EDT Département")
        
        st.info(f"Validation des emplois du temps pour le département **{selected_dept}**")
        
        periodes = db.get_periodes_examen(actif=True)
        
        if periodes:
            periode_options = {f"{p['nom']}": p['id'] for p in periodes}
            selected = st.selectbox("Période", list(periode_options.keys()), key="valid_periode")
            periode_id = periode_options[selected]
            
            # Get exams for department
            examens = db.execute_query("""
                SELECT e.*, m.nom as module, l.nom as salle
                FROM examens e
                JOIN modules m ON e.module_id = m.id
                JOIN formations f ON m.formation_id = f.id
                JOIN lieu_examen l ON e.salle_id = l.id
                WHERE f.dept_id = %s AND e.periode_id = %s
                ORDER BY e.date_heure
            """, (dept_id, periode_id))
            
            if examens:
                st.success(f" {len(examens)} examens planifiés pour ce département")
                st.dataframe(pd.DataFrame(examens), use_container_width=True, hide_index=True)
                
                st.markdown("---")
                
                check1 = st.checkbox("J'ai vérifié les horaires des examens")
                check2 = st.checkbox("J'ai vérifié les salles attribuées")
                check3 = st.checkbox("EDT conforme aux besoins du département")
                
                if st.button(" Valider l'EDT du département", type="primary", 
                           disabled=not (check1 and check2 and check3), use_container_width=True):
                    st.success(f" EDT validé pour {selected_dept} le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
                    st.balloons()
            else:
                st.info("Aucun examen planifié pour ce département")
        else:
            st.warning("Aucune période d'examen active")

if __name__ == "__main__":
    main()
