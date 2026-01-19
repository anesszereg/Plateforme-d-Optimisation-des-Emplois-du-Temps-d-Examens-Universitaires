import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.session import require_auth, show_user_sidebar, get_current_user

st.set_page_config(
    page_title="Professeurs - Planning",
    page_icon="",
    layout="wide"
)

# Authentication - only professeur can access
require_auth(allowed_roles=['professeur'])
show_user_sidebar()

@st.cache_resource
def get_database():
    return Database()

def main():
    st.title(" Espace Professeur")
    st.markdown("**Consultez votre planning personnel et votre charge horaire**")
    
    db = get_database()
    user = get_current_user()
    
    prof_id = user.get('professeur_id') if user else None
    
    if not prof_id:
        st.error("Erreur: ID professeur non trouvé")
        return
    
    # Get professor info
    prof_info = db.execute_query(
        "SELECT p.*, d.nom as departement FROM professeurs p JOIN departements d ON p.dept_id = d.id WHERE p.id = %s",
        (prof_id,)
    )
    
    if prof_info:
        info = prof_info[0]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Nom:** {info['prenom']} {info['nom']}")
        with col2:
            st.info(f"**Grade:** {info['grade']}")
        with col3:
            st.info(f"**Département:** {info['departement']}")
    
    tab1, tab2 = st.tabs([" Mon Planning", " Ma Charge Horaire"])
    
    with tab1:
        st.header(" Mon Planning de Surveillances")
        
        periodes = db.get_periodes_examen(actif=True)
        
        if periodes:
            periode_options = {f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] for p in periodes}
            selected = st.selectbox("Période d'examen", list(periode_options.keys()))
            periode_id = periode_options[selected]
            
            planning = db.get_planning_professeur(prof_id, periode_id)
            
            if planning:
                st.success(f" Vous avez **{len(planning)} surveillance(s)** planifiée(s)")
                
                df = pd.DataFrame(planning)
                df['date'] = pd.to_datetime(df['date_heure']).dt.date
                df['heure'] = pd.to_datetime(df['date_heure']).dt.strftime('%H:%M')
                
                # Stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total surveillances", len(planning))
                with col2:
                    responsable = len(df[df['role'] == 'responsable'])
                    st.metric("En tant que responsable", responsable)
                with col3:
                    st.metric("Jours de surveillance", df['date'].nunique())
                
                st.markdown("---")
                
                # Calendar view
                for date in sorted(df['date'].unique()):
                    st.markdown(f"###  {date}")
                    day_surv = df[df['date'] == date].sort_values('heure')
                    
                    for _, surv in day_surv.iterrows():
                        role_icon = "⭐" if surv['role'] == 'responsable' else ""
                        st.markdown(f"- **{surv['heure']}** | {surv['module']} | {surv['salle']} | {role_icon} {surv['role']}")
                
                st.markdown("---")
                
                # Export
                csv = df.to_csv(index=False, encoding='utf-8')
                st.download_button(" Télécharger mon planning", csv, "mon_planning.csv", "text/csv")
            else:
                st.info("📭 Aucune surveillance planifiée pour cette période")
        else:
            st.warning("Aucune période d'examen active")
    
    with tab2:
        st.header(" Ma Charge Horaire")
        
        # Get workload
        charge = db.execute_query("""
            SELECT COUNT(*) as nb_surveillances,
                   SUM(e.duree_minutes) as total_minutes,
                   COUNT(DISTINCT DATE(e.date_heure)) as nb_jours
            FROM surveillances s
            JOIN examens e ON s.examen_id = e.id
            WHERE s.prof_id = %s
        """, (prof_id,))
        
        if charge and charge[0]['nb_surveillances']:
            c = charge[0]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Surveillances totales", c['nb_surveillances'])
            with col2:
                hours = (c['total_minutes'] or 0) // 60
                st.metric("Heures totales", f"{hours}h")
            with col3:
                st.metric("Jours mobilisés", c['nb_jours'])
        else:
            st.info("Aucune surveillance assignée")

if __name__ == "__main__":
    main()
