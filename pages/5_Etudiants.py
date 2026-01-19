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
    page_title="Étudiants - Planning",
    page_icon="",
    layout="wide"
)

# Authentication - only etudiant can access
require_auth(allowed_roles=['etudiant'])
show_user_sidebar()

@st.cache_resource
def get_database():
    return Database()

def main():
    st.title(" Espace Étudiant")
    st.markdown("**Consultez votre planning d'examens personnalisé**")
    
    db = get_database()
    user = get_current_user()
    
    etudiant_id = user.get('etudiant_id') if user else None
    
    if not etudiant_id:
        st.error("Erreur: ID étudiant non trouvé")
        return
    
    # Get student info
    etudiant_info = db.execute_query(
        """SELECT e.*, f.nom as formation, f.niveau, d.nom as departement 
           FROM etudiants e 
           JOIN formations f ON e.formation_id = f.id 
           JOIN departements d ON f.dept_id = d.id 
           WHERE e.id = %s""",
        (etudiant_id,)
    )
    
    if etudiant_info:
        info = etudiant_info[0]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Nom:** {info['prenom']} {info['nom']}")
        with col2:
            st.info(f"**Formation:** {info['formation']} ({info['niveau']})")
        with col3:
            st.info(f"**Département:** {info['departement']}")
    
    st.markdown("---")
    st.header(" Mon Planning d'Examens")
    
    periodes = db.get_periodes_examen(actif=True)
    
    if periodes:
        periode_options = {f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] for p in periodes}
        selected = st.selectbox("Période d'examen", list(periode_options.keys()))
        periode_id = periode_options[selected]
        
        planning = db.get_planning_etudiant(etudiant_id, periode_id)
        
        if planning:
            st.success(f" Vous avez **{len(planning)} examen(s)** planifié(s)")
            
            df = pd.DataFrame(planning)
            df['date'] = pd.to_datetime(df['date_heure']).dt.date
            df['heure'] = pd.to_datetime(df['date_heure']).dt.strftime('%H:%M')
            
            # Stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total examens", len(planning))
            with col2:
                total_duration = df['duree_minutes'].sum()
                st.metric("Durée totale", f"{total_duration // 60}h {total_duration % 60}min")
            with col3:
                st.metric("Premier examen", str(df['date'].min()))
            with col4:
                st.metric("Dernier examen", str(df['date'].max()))
            
            st.markdown("---")
            
            # Filters
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                semestre_filter = st.multiselect(
                    "Filtrer par semestre",
                    options=[1, 2],
                    default=[1, 2]
                )
            
            # Calendar view
            st.subheader(" Détail de vos examens")
            
            for date in sorted(df['date'].unique()):
                st.markdown(f"###  {date}")
                day_exams = df[df['date'] == date].sort_values('heure')
                
                for _, exam in day_exams.iterrows():
                    st.markdown(f"""
                    - **{exam['heure']}** | 📚 {exam['module']} |  {exam['salle']} ({exam['batiment']}) | ⏱️ {exam['duree_minutes']} min
                    """)
            
            st.markdown("---")
            
            # Export
            csv = df.to_csv(index=False, encoding='utf-8')
            st.download_button(" Télécharger mon planning", csv, "mon_planning_examens.csv", "text/csv")
        else:
            st.info("📭 Aucun examen planifié pour cette période")
    else:
        st.warning("Aucune période d'examen active")

if __name__ == "__main__":
    main()
