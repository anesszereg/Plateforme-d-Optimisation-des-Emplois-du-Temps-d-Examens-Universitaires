import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database

st.set_page_config(
    page_title="Consultation - Planning Personnel",
    page_icon="",
    layout="wide"
)

@st.cache_resource
def get_database():
    return Database()

def main():
    st.title(" Consultation de Planning Personnel")
    st.markdown("Consultez votre emploi du temps d'examens personnalisé")
    
    db = get_database()
    
    user_type = st.radio(
        "Je suis:",
        ["‍ Étudiant", "‍ Professeur"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if user_type == "‍ Étudiant":
        show_student_view(db)
    else:
        show_professor_view(db)

def show_student_view(db):
    st.header("‍ Planning Étudiant")
    
    col_search1, col_search2 = st.columns(2)
    
    with col_search1:
        search_name = st.text_input(" Rechercher par nom")
    
    with col_search2:
        departements = db.get_departements()
        dept_options = ["Tous"] + [d['nom'] for d in departements]
        selected_dept = st.selectbox("Département", dept_options)
    
    if search_name:
        query = """
            SELECT e.id, e.nom, e.prenom, e.email, f.nom as formation, d.nom as departement
            FROM etudiants e
            JOIN formations f ON e.formation_id = f.id
            JOIN departements d ON f.dept_id = d.id
            WHERE e.nom ILIKE %s OR e.prenom ILIKE %s
        """
        if selected_dept != "Tous":
            query += " AND d.nom = %s"
            etudiants = db.execute_query(query, (f"%{search_name}%", f"%{search_name}%", selected_dept))
        else:
            etudiants = db.execute_query(query, (f"%{search_name}%", f"%{search_name}%"))
        
        if etudiants:
            st.success(f" {len(etudiants)} étudiant(s) trouvé(s)")
            
            etudiant_options = {
                f"{e['nom']} {e['prenom']} - {e['formation']}": e['id']
                for e in etudiants
            }
            
            selected_etudiant = st.selectbox(
                "Sélectionnez votre profil",
                options=list(etudiant_options.keys())
            )
            
            etudiant_id = etudiant_options[selected_etudiant]
            
            etudiant_info = next(e for e in etudiants if e['id'] == etudiant_id)
            
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.info(f"**Nom:** {etudiant_info['nom']} {etudiant_info['prenom']}")
            
            with col_info2:
                st.info(f"**Formation:** {etudiant_info['formation']}")
            
            with col_info3:
                st.info(f"**Département:** {etudiant_info['departement']}")
            
            st.markdown("---")
            
            periodes = db.get_periodes_examen(actif=True)
            
            if periodes:
                periode_options = {
                    f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id']
                    for p in periodes
                }
                
                selected_periode = st.selectbox(
                    "Période d'examen",
                    options=list(periode_options.keys())
                )
                
                periode_id = periode_options[selected_periode]
                
                planning = db.get_planning_etudiant(etudiant_id, periode_id)
                
                if planning:
                    st.success(f" Vous avez {len(planning)} examen(s) planifié(s)")
                    
                    planning_df = pd.DataFrame(planning)
                    planning_df['date'] = pd.to_datetime(planning_df['date_heure']).dt.date
                    planning_df['heure'] = pd.to_datetime(planning_df['date_heure']).dt.strftime('%H:%M')
                    
                    col_cal1, col_cal2 = st.columns(2)
                    
                    with col_cal1:
                        exams_by_date = planning_df.groupby('date').size().reset_index(name='count')
                        
                        fig_calendar = px.bar(
                            exams_by_date,
                            x='date',
                            y='count',
                            title='Calendrier de vos Examens',
                            labels={'count': 'Nombre d\'examens', 'date': 'Date'}
                        )
                        st.plotly_chart(fig_calendar, use_container_width=True)
                    
                    with col_cal2:
                        total_duration = planning_df['duree_minutes'].sum()
                        avg_duration = planning_df['duree_minutes'].mean()
                        
                        st.metric("Durée totale", f"{total_duration // 60}h {total_duration % 60}min")
                        st.metric("Durée moyenne", f"{avg_duration:.0f} min")
                        st.metric("Premier examen", planning_df['date'].min())
                        st.metric("Dernier examen", planning_df['date'].max())
                    
                    st.markdown("---")
                    
                    st.subheader(" Détail de votre Planning")
                    
                    for date in sorted(planning_df['date'].unique()):
                        st.markdown(f"###  {date.strftime('%A %d %B %Y')}")
                        
                        day_exams = planning_df[planning_df['date'] == date]
                        
                        for _, exam in day_exams.iterrows():
                            with st.container():
                                col_e1, col_e2, col_e3, col_e4 = st.columns([2, 2, 2, 1])
                                
                                with col_e1:
                                    st.markdown(f"** {exam['heure']}**")
                                
                                with col_e2:
                                    st.markdown(f"** {exam['module']}**")
                                    st.caption(exam['code_module'])
                                
                                with col_e3:
                                    st.markdown(f"** {exam['salle']}**")
                                    st.caption(exam['batiment'])
                                
                                with col_e4:
                                    st.markdown(f"**⏱ {exam['duree_minutes']} min**")
                                
                                st.markdown("---")
                    
                    if st.button(" Télécharger mon planning (CSV)"):
                        csv = planning_df.to_csv(index=False, encoding='utf-8')
                        st.download_button(
                            label="Télécharger",
                            data=csv,
                            file_name=f"planning_etudiant_{etudiant_id}.csv",
                            mime="text/csv"
                        )
                else:
                    st.info(" Aucun examen planifié pour cette période")
            else:
                st.warning("Aucune période d'examen active")
        else:
            st.warning("Aucun étudiant trouvé avec ce nom")
    else:
        st.info(" Entrez votre nom pour rechercher votre planning")

def show_professor_view(db):
    st.header("‍ Planning Professeur")
    
    col_search1, col_search2 = st.columns(2)
    
    with col_search1:
        search_name = st.text_input(" Rechercher par nom")
    
    with col_search2:
        departements = db.get_departements()
        dept_options = ["Tous"] + [d['nom'] for d in departements]
        selected_dept = st.selectbox("Département", dept_options)
    
    if search_name:
        query = """
            SELECT p.id, p.nom, p.prenom, p.email, p.grade, p.specialite, d.nom as departement
            FROM professeurs p
            JOIN departements d ON p.dept_id = d.id
            WHERE p.nom ILIKE %s OR p.prenom ILIKE %s
        """
        if selected_dept != "Tous":
            query += " AND d.nom = %s"
            professeurs = db.execute_query(query, (f"%{search_name}%", f"%{search_name}%", selected_dept))
        else:
            professeurs = db.execute_query(query, (f"%{search_name}%", f"%{search_name}%"))
        
        if professeurs:
            st.success(f" {len(professeurs)} professeur(s) trouvé(s)")
            
            prof_options = {
                f"{p['nom']} {p['prenom']} - {p['grade']} ({p['departement']})": p['id']
                for p in professeurs
            }
            
            selected_prof = st.selectbox(
                "Sélectionnez votre profil",
                options=list(prof_options.keys())
            )
            
            prof_id = prof_options[selected_prof]
            
            prof_info = next(p for p in professeurs if p['id'] == prof_id)
            
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.info(f"**Nom:** {prof_info['nom']} {prof_info['prenom']}")
            
            with col_info2:
                st.info(f"**Grade:** {prof_info['grade']}")
            
            with col_info3:
                st.info(f"**Département:** {prof_info['departement']}")
            
            st.markdown("---")
            
            periodes = db.get_periodes_examen(actif=True)
            
            if periodes:
                periode_options = {
                    f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id']
                    for p in periodes
                }
                
                selected_periode = st.selectbox(
                    "Période d'examen",
                    options=list(periode_options.keys())
                )
                
                periode_id = periode_options[selected_periode]
                
                planning = db.get_planning_professeur(prof_id, periode_id)
                
                if planning:
                    st.success(f" Vous avez {len(planning)} surveillance(s) planifiée(s)")
                    
                    planning_df = pd.DataFrame(planning)
                    planning_df['date'] = pd.to_datetime(planning_df['date_heure']).dt.date
                    planning_df['heure'] = pd.to_datetime(planning_df['date_heure']).dt.strftime('%H:%M')
                    
                    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                    
                    with col_stat1:
                        st.metric("Total surveillances", len(planning))
                    
                    with col_stat2:
                        responsable_count = len(planning_df[planning_df['role'] == 'responsable'])
                        st.metric("En tant que responsable", responsable_count)
                    
                    with col_stat3:
                        total_students = planning_df['nb_etudiants'].sum()
                        st.metric("Total étudiants surveillés", f"{total_students:,}")
                    
                    with col_stat4:
                        unique_dates = planning_df['date'].nunique()
                        st.metric("Jours de surveillance", unique_dates)
                    
                    st.markdown("---")
                    
                    col_chart1, col_chart2 = st.columns(2)
                    
                    with col_chart1:
                        surv_by_date = planning_df.groupby('date').size().reset_index(name='count')
                        
                        fig_calendar = px.bar(
                            surv_by_date,
                            x='date',
                            y='count',
                            title='Calendrier de vos Surveillances',
                            labels={'count': 'Nombre de surveillances', 'date': 'Date'}
                        )
                        st.plotly_chart(fig_calendar, use_container_width=True)
                    
                    with col_chart2:
                        role_counts = planning_df['role'].value_counts()
                        
                        fig_pie = px.pie(
                            values=role_counts.values,
                            names=role_counts.index,
                            title='Répartition par Rôle'
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    st.markdown("---")
                    
                    st.subheader(" Détail de votre Planning")
                    
                    for date in sorted(planning_df['date'].unique()):
                        st.markdown(f"###  {date.strftime('%A %d %B %Y')}")
                        
                        day_surv = planning_df[planning_df['date'] == date]
                        
                        for _, surv in day_surv.iterrows():
                            with st.container():
                                col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns([1, 2, 2, 1, 1])
                                
                                with col_s1:
                                    st.markdown(f"** {surv['heure']}**")
                                
                                with col_s2:
                                    st.markdown(f"** {surv['module']}**")
                                
                                with col_s3:
                                    st.markdown(f"** {surv['salle']}**")
                                    st.caption(surv['batiment'])
                                
                                with col_s4:
                                    role_emoji = "" if surv['role'] == 'responsable' else ""
                                    st.markdown(f"**{role_emoji} {surv['role'].title()}**")
                                
                                with col_s5:
                                    st.markdown(f"** {surv['nb_etudiants']}**")
                                    st.caption(f"{surv['duree_minutes']} min")
                                
                                st.markdown("---")
                    
                    if st.button(" Télécharger mon planning (CSV)"):
                        csv = planning_df.to_csv(index=False, encoding='utf-8')
                        st.download_button(
                            label="Télécharger",
                            data=csv,
                            file_name=f"planning_professeur_{prof_id}.csv",
                            mime="text/csv"
                        )
                else:
                    st.info(" Aucune surveillance planifiée pour cette période")
            else:
                st.warning("Aucune période d'examen active")
        else:
            st.warning("Aucun professeur trouvé avec ce nom")
    else:
        st.info(" Entrez votre nom pour rechercher votre planning")

if __name__ == "__main__":
    main()
