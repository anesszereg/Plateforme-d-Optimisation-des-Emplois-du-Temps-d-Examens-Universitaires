import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.scheduler import ExamScheduler
from src.fast_scheduler import FastScheduler
from src.analytics import Analytics

st.set_page_config(
    page_title="Administration - Génération d'EDT",
    page_icon="👨‍💼",
    layout="wide"
)

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_scheduler(_db):
    return ExamScheduler(_db)

@st.cache_resource
def get_analytics(_db):
    return Analytics(_db)

def main():
    st.title("👨‍💼 Administration des Examens")
    st.markdown("Génération automatique et optimisation des emplois du temps d'examens")
    
    db = get_database()
    scheduler = get_scheduler(db)
    analytics = get_analytics(db)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Génération d'EDT", "🔍 Détection de Conflits", "📋 Examens Planifiés", "🏛️ Planning par Département"])
    
    with tab1:
        st.header("🚀 Génération Automatique d'Emploi du Temps")
        
        periodes = db.get_periodes_examen(actif=True)
        
        if not periodes:
            st.warning("⚠️ Aucune période d'examen active trouvée")
            st.info("Créez une période d'examen dans la base de données pour continuer")
        else:
            periode_options = {
                f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] 
                for p in periodes
            }
            
            selected_periode = st.selectbox(
                "Sélectionnez la période d'examen",
                options=list(periode_options.keys())
            )
            
            periode_id = periode_options[selected_periode]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.info("""
                **Contraintes appliquées:**
                - ✅ Maximum 1 examen par jour par étudiant
                - ✅ Maximum 3 examens par jour par professeur
                - ✅ Respect de la capacité des salles (20 étudiants max)
                - ✅ Pas de chevauchement de salles
                - ✅ Priorité aux professeurs du département
                """)
            
            with col2:
                annee_universitaire = st.text_input(
                    "Année universitaire",
                    value="2024-2025"
                )
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            
            with col_btn1:
                if st.button("🚀 Générer l'EDT", type="primary", use_container_width=True):
                    with st.spinner("Génération en cours... Optimisé pour ~10 secondes"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("Initialisation...")
                        progress_bar.progress(10)
                        
                        try:
                            status_text.text("Génération du planning...")
                            progress_bar.progress(30)
                            
                            # Use FastScheduler for ultra-fast performance
                            fast_scheduler = FastScheduler(db)
                            success, result = fast_scheduler.generate_schedule(periode_id, annee_universitaire)
                            
                            progress_bar.progress(80)
                            status_text.text("Finalisation...")
                            
                            if success:
                                progress_bar.progress(100)
                                status_text.text("Terminé!")
                                
                                st.success(f"✅ EDT généré avec succès en {result['execution_time']:.2f} secondes!")
                                
                                col_r1, col_r2, col_r3 = st.columns(3)
                                
                                with col_r1:
                                    st.metric("Examens planifiés", result['scheduled'])
                                
                                with col_r2:
                                    st.metric("Modules non planifiés", result['failed'])
                                
                                with col_r3:
                                    st.metric("Conflits détectés", result['total_conflicts'])
                                
                                if result['failed'] > 0:
                                    st.warning("⚠️ Certains modules n'ont pas pu être planifiés:")
                                    failed_df = pd.DataFrame(result['failed_modules'])
                                    st.dataframe(failed_df, use_container_width=True)
                                
                                if result['total_conflicts'] > 0:
                                    st.error(f"❌ {result['total_conflicts']} conflit(s) détecté(s). Consultez l'onglet 'Détection de Conflits'")
                                
                                st.balloons()
                            else:
                                st.error(f"❌ Erreur lors de la génération: {result.get('error', 'Erreur inconnue')}")
                        
                        except Exception as e:
                            st.error(f"❌ Erreur: {e}")
                            import traceback
                            st.code(traceback.format_exc())
            
            with col_btn2:
                if st.button("🔄 Optimiser l'EDT", use_container_width=True):
                    with st.spinner("Optimisation en cours..."):
                        try:
                            optimizations = scheduler.optimize_schedule(periode_id)
                            st.success(f"✅ {optimizations} optimisation(s) effectuée(s)")
                        except Exception as e:
                            st.error(f"❌ Erreur: {e}")
            
            with col_btn3:
                if st.button("🗑️ Supprimer tous les examens", use_container_width=True):
                    if st.checkbox("Confirmer la suppression"):
                        try:
                            db.delete_all_examens(periode_id)
                            st.success("✅ Tous les examens ont été supprimés")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erreur: {e}")
    
    with tab2:
        st.header("🔍 Détection de Conflits")
        
        conflict_types = st.multiselect(
            "Types de conflits à afficher",
            ["Étudiants", "Professeurs", "Capacité", "Salles"],
            default=["Étudiants", "Professeurs", "Capacité", "Salles"]
        )
        
        if "Étudiants" in conflict_types:
            st.subheader("⚠️ Conflits Étudiants (>1 examen/jour)")
            conflits_etudiants = db.get_conflits_etudiants()
            if conflits_etudiants:
                df = pd.DataFrame(conflits_etudiants)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.success("✅ Aucun conflit étudiant détecté")
        
        if "Professeurs" in conflict_types:
            st.subheader("⚠️ Conflits Professeurs (>3 examens/jour)")
            conflits_profs = db.get_conflits_professeurs()
            if conflits_profs:
                df = pd.DataFrame(conflits_profs)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.success("✅ Aucun conflit professeur détecté")
        
        if "Capacité" in conflict_types:
            st.subheader("⚠️ Conflits de Capacité")
            conflits_capacite = db.get_conflits_capacite()
            if conflits_capacite:
                df = pd.DataFrame(conflits_capacite)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.success("✅ Aucun conflit de capacité détecté")
        
        if "Salles" in conflict_types:
            st.subheader("⚠️ Conflits de Salles (chevauchements)")
            conflits_salles = db.get_conflits_salles()
            if conflits_salles:
                df = pd.DataFrame(conflits_salles)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.success("✅ Aucun conflit de salle détecté")
    
    with tab3:
        st.header("📋 Examens Planifiés")
        
        periodes = db.get_periodes_examen(actif=True)
        
        if periodes:
            periode_options = {
                f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] 
                for p in periodes
            }
            
            selected_periode_view = st.selectbox(
                "Période d'examen",
                options=list(periode_options.keys()),
                key="view_periode"
            )
            
            periode_id_view = periode_options[selected_periode_view]
            
            examens = db.get_examens(periode_id_view)
            
            if examens:
                df = pd.DataFrame(examens)
                
                st.metric("Total d'examens planifiés", len(examens))
                
                col_filter1, col_filter2 = st.columns(2)
                
                with col_filter1:
                    search_module = st.text_input("🔍 Rechercher un module")
                
                with col_filter2:
                    search_salle = st.text_input("🔍 Rechercher une salle")
                
                if search_module:
                    df = df[df['module_nom'].str.contains(search_module, case=False, na=False)]
                
                if search_salle:
                    df = df[df['salle_nom'].str.contains(search_salle, case=False, na=False)]
                
                st.dataframe(
                    df[['date_heure', 'module_nom', 'salle_nom', 'professeur', 'nb_inscrits', 'duree_minutes', 'statut']],
                    use_container_width=True,
                    hide_index=True
                )
                
                if st.button("📥 Exporter en CSV"):
                    csv = df.to_csv(index=False, encoding='utf-8')
                    st.download_button(
                        label="Télécharger le CSV",
                        data=csv,
                        file_name=f"examens_{periode_id_view}.csv",
                        mime="text/csv"
                    )
            else:
                st.info("Aucun examen planifié pour cette période")
    
    with tab4:
        st.header("🏛️ Planning par Département")
        
        periodes = db.get_periodes_examen(actif=True)
        
        if periodes:
            periode_options = {
                f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] 
                for p in periodes
            }
            
            selected_periode_dept = st.selectbox(
                "Période d'examen",
                options=list(periode_options.keys()),
                key="dept_periode"
            )
            
            periode_id_dept = periode_options[selected_periode_dept]
            
            # Get departments
            departements = db.get_departements()
            
            if departements:
                # Department selector
                dept_names = {d['nom']: d['id'] for d in departements}
                selected_dept = st.selectbox(
                    "Sélectionnez un département",
                    options=["Tous les départements"] + list(dept_names.keys())
                )
                
                # Get all exams with department info
                query = """
                    SELECT 
                        e.id,
                        e.date_heure,
                        e.duree_minutes,
                        e.nb_inscrits,
                        m.nom as module_nom,
                        m.code as module_code,
                        l.nom as salle_nom,
                        l.batiment,
                        p.nom || ' ' || p.prenom as professeur,
                        d.nom as departement,
                        f.nom as formation
                    FROM examens e
                    JOIN modules m ON e.module_id = m.id
                    JOIN lieu_examen l ON e.salle_id = l.id
                    JOIN professeurs p ON e.prof_responsable_id = p.id
                    JOIN formations f ON m.formation_id = f.id
                    JOIN departements d ON f.dept_id = d.id
                    WHERE e.periode_id = %s
                    ORDER BY d.nom, e.date_heure, m.nom
                """
                
                examens_dept = db.execute_query(query, (periode_id_dept,))
                
                if examens_dept:
                    # Filter by department if selected
                    if selected_dept != "Tous les départements":
                        examens_dept = [e for e in examens_dept if e['departement'] == selected_dept]
                    
                    if examens_dept:
                        df_dept = pd.DataFrame(examens_dept)
                        
                        # Summary metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Examens", len(examens_dept))
                        with col2:
                            unique_depts = df_dept['departement'].nunique()
                            st.metric("Départements", unique_depts)
                        with col3:
                            total_students = df_dept['nb_inscrits'].sum()
                            st.metric("Total Étudiants", f"{total_students:,}")
                        with col4:
                            unique_rooms = df_dept['salle_nom'].nunique()
                            st.metric("Salles Utilisées", unique_rooms)
                        
                        st.markdown("---")
                        
                        # Display format selector
                        display_format = st.radio(
                            "Format d'affichage",
                            ["Par Département et Date", "Calendrier", "Liste Détaillée"],
                            horizontal=True
                        )
                        
                        if display_format == "Par Département et Date":
                            # Group by department
                            for dept_name in sorted(df_dept['departement'].unique()):
                                with st.expander(f"🏛️ {dept_name}", expanded=(selected_dept != "Tous les départements")):
                                    dept_exams = df_dept[df_dept['departement'] == dept_name]
                                    
                                    st.markdown(f"**{len(dept_exams)} examens planifiés**")
                                    
                                    # Group by date
                                    dept_exams['date'] = pd.to_datetime(dept_exams['date_heure']).dt.date
                                    dept_exams['heure'] = pd.to_datetime(dept_exams['date_heure']).dt.strftime('%H:%M')
                                    
                                    for date in sorted(dept_exams['date'].unique()):
                                        st.markdown(f"### 📅 {date.strftime('%A %d %B %Y')}")
                                        
                                        date_exams = dept_exams[dept_exams['date'] == date].sort_values('heure')
                                        
                                        for _, exam in date_exams.iterrows():
                                            col_time, col_info = st.columns([1, 4])
                                            
                                            with col_time:
                                                st.markdown(f"**{exam['heure']}**")
                                                st.caption(f"{exam['duree_minutes']} min")
                                            
                                            with col_info:
                                                st.markdown(f"**{exam['module_nom']}** ({exam['module_code']})")
                                                st.markdown(f"📍 {exam['salle_nom']} - {exam['batiment']} | 👨‍🏫 {exam['professeur']} | 👥 {exam['nb_inscrits']} étudiants")
                                                st.markdown(f"🎓 Formation: {exam['formation']}")
                                        
                                        st.markdown("---")
                        
                        elif display_format == "Calendrier":
                            # Calendar view
                            df_dept['date'] = pd.to_datetime(df_dept['date_heure']).dt.date
                            df_dept['heure'] = pd.to_datetime(df_dept['date_heure']).dt.strftime('%H:%M')
                            
                            for date in sorted(df_dept['date'].unique()):
                                st.markdown(f"## 📅 {date.strftime('%A %d %B %Y')}")
                                
                                date_exams = df_dept[df_dept['date'] == date].sort_values('heure')
                                
                                # Create columns for time slots
                                time_slots = date_exams['heure'].unique()
                                
                                for time_slot in sorted(time_slots):
                                    st.markdown(f"### ⏰ {time_slot}")
                                    
                                    slot_exams = date_exams[date_exams['heure'] == time_slot]
                                    
                                    cols = st.columns(min(3, len(slot_exams)))
                                    
                                    for idx, (_, exam) in enumerate(slot_exams.iterrows()):
                                        with cols[idx % 3]:
                                            st.markdown(f"""
                                            <div style="border: 2px solid #1f77b4; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: #f0f8ff;">
                                                <h4 style="margin: 0; color: #1f77b4;">{exam['module_nom']}</h4>
                                                <p style="margin: 5px 0;"><strong>🏛️</strong> {exam['departement']}</p>
                                                <p style="margin: 5px 0;"><strong>📍</strong> {exam['salle_nom']} ({exam['batiment']})</p>
                                                <p style="margin: 5px 0;"><strong>👨‍🏫</strong> {exam['professeur']}</p>
                                                <p style="margin: 5px 0;"><strong>👥</strong> {exam['nb_inscrits']} étudiants</p>
                                                <p style="margin: 5px 0;"><strong>⏱️</strong> {exam['duree_minutes']} minutes</p>
                                            </div>
                                            """, unsafe_allow_html=True)
                                
                                st.markdown("---")
                        
                        else:  # Liste Détaillée
                            st.dataframe(
                                df_dept[['date_heure', 'departement', 'module_nom', 'module_code', 
                                        'salle_nom', 'batiment', 'professeur', 'nb_inscrits', 'duree_minutes']],
                                use_container_width=True,
                                hide_index=True
                            )
                        
                        # Export options
                        st.markdown("---")
                        col_exp1, col_exp2 = st.columns(2)
                        
                        with col_exp1:
                            if st.button("📥 Exporter en CSV", key="export_csv_dept"):
                                csv = df_dept.to_csv(index=False, encoding='utf-8')
                                st.download_button(
                                    label="Télécharger le CSV",
                                    data=csv,
                                    file_name=f"planning_departements_{periode_id_dept}.csv",
                                    mime="text/csv",
                                    key="download_csv_dept"
                                )
                        
                        with col_exp2:
                            if st.button("📊 Exporter en Excel", key="export_excel_dept"):
                                import io
                                output = io.BytesIO()
                                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                    df_dept.to_excel(writer, index=False, sheet_name='Planning')
                                output.seek(0)
                                st.download_button(
                                    label="Télécharger Excel",
                                    data=output,
                                    file_name=f"planning_departements_{periode_id_dept}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="download_excel_dept"
                                )
                    else:
                        st.info(f"Aucun examen planifié pour le département {selected_dept}")
                else:
                    st.info("Aucun examen planifié pour cette période")
            else:
                st.warning("Aucun département trouvé")
        else:
            st.warning("Aucune période d'examen active")

if __name__ == "__main__":
    main()
