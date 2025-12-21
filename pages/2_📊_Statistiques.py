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

st.set_page_config(
    page_title="Statistiques - Vue Stratégique",
    page_icon="📊",
    layout="wide"
)

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_analytics(_db):
    return Analytics(_db)

def main():
    st.title("📊 Statistiques et Vue Stratégique")
    st.markdown("Tableau de bord pour Vice-doyen et Doyen")
    
    db = get_database()
    analytics = get_analytics(db)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 KPIs Globaux", "🏛️ Par Département", "👨‍🏫 Charge Professeurs", "💺 Occupation Salles"])
    
    with tab1:
        st.header("📈 Indicateurs Clés de Performance")
        
        try:
            kpis = analytics.get_dashboard_kpis()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 👥 Population")
                st.metric("Étudiants", f"{kpis.get('total_etudiants', 0):,}")
                st.metric("Professeurs", f"{kpis.get('total_professeurs', 0):,}")
                ratio = kpis.get('total_etudiants', 0) / max(kpis.get('total_professeurs', 1), 1)
                st.metric("Ratio Étudiants/Prof", f"{ratio:.1f}")
            
            with col2:
                st.markdown("### 📚 Académique")
                st.metric("Départements", kpis.get('total_departements', 0))
                st.metric("Formations", kpis.get('total_formations', 0))
                st.metric("Modules", kpis.get('total_modules', 0))
            
            with col3:
                st.markdown("### 🏫 Infrastructure")
                st.metric("Salles disponibles", kpis.get('total_salles', 0))
                st.metric("Capacité totale", f"{kpis.get('capacite_totale', 0):,}")
                st.metric("Examens planifiés", kpis.get('examens_planifies', 0))
            
            st.markdown("---")
            
            st.subheader("📊 Inscriptions")
            
            col_ins1, col_ins2 = st.columns(2)
            
            with col_ins1:
                total_inscriptions = kpis.get('total_inscriptions', 0)
                st.metric("Total Inscriptions", f"{total_inscriptions:,}")
                
                avg_per_student = total_inscriptions / max(kpis.get('total_etudiants', 1), 1)
                st.metric("Moyenne par étudiant", f"{avg_per_student:.1f} modules")
            
            with col_ins2:
                avg_per_module = total_inscriptions / max(kpis.get('total_modules', 1), 1)
                st.metric("Moyenne par module", f"{avg_per_module:.1f} étudiants")
                
                capacity_usage = (kpis.get('examens_planifies', 0) / max(kpis.get('total_salles', 1), 1)) * 100
                st.metric("Taux d'utilisation salles", f"{capacity_usage:.1f}%")
            
            periodes = db.get_periodes_examen(actif=True)
            if periodes:
                st.markdown("---")
                st.subheader("🎯 Score d'Efficacité du Planning")
                
                periode_options = {
                    f"{p['nom']}": p['id'] 
                    for p in periodes
                }
                
                selected_periode = st.selectbox(
                    "Sélectionnez une période",
                    options=list(periode_options.keys())
                )
                
                periode_id = periode_options[selected_periode]
                
                efficiency = analytics.calculate_efficiency_score(periode_id)
                
                score = efficiency['score']
                
                if score >= 80:
                    color = "green"
                    emoji = "🟢"
                elif score >= 60:
                    color = "orange"
                    emoji = "🟡"
                else:
                    color = "red"
                    emoji = "🔴"
                
                st.markdown(f"### {emoji} Score Global: {score:.1f}/100")
                
                st.progress(score / 100)
                
                col_eff1, col_eff2, col_eff3 = st.columns(3)
                
                metrics = efficiency['metrics']
                
                with col_eff1:
                    st.metric("Taux d'utilisation", f"{metrics['utilization_rate']:.1f}%")
                    st.metric("Examens totaux", metrics['total_exams'])
                
                with col_eff2:
                    st.metric("Taux de conflits", f"{metrics['conflict_rate']:.2f}%")
                    st.metric("Jours utilisés", metrics['unique_dates'])
                
                with col_eff3:
                    st.metric("Examens/jour (moy)", f"{metrics['avg_exams_per_day']:.1f}")
        
        except Exception as e:
            st.error(f"Erreur lors du chargement des KPIs: {e}")
    
    with tab2:
        st.header("🏛️ Statistiques par Département")
        
        try:
            dept_stats = analytics.get_department_stats()
            
            if not dept_stats.empty:
                st.dataframe(
                    dept_stats,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "nb_etudiants": st.column_config.NumberColumn(
                            "Étudiants",
                            format="%d 👨‍🎓"
                        ),
                        "nb_professeurs": st.column_config.NumberColumn(
                            "Professeurs",
                            format="%d 👨‍🏫"
                        ),
                        "nb_formations": st.column_config.NumberColumn(
                            "Formations",
                            format="%d 📚"
                        )
                    }
                )
                
                st.markdown("---")
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    fig_pie = px.pie(
                        dept_stats,
                        values='nb_etudiants',
                        names='departement',
                        title='Répartition des Étudiants',
                        hole=0.4
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col_chart2:
                    fig_bar = px.bar(
                        dept_stats,
                        x='departement',
                        y=['nb_formations', 'nb_modules'],
                        title='Formations et Modules par Département',
                        barmode='group'
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                dept_stats['ratio_etud_prof'] = dept_stats['nb_etudiants'] / dept_stats['nb_professeurs'].replace(0, 1)
                
                fig_ratio = px.bar(
                    dept_stats,
                    x='departement',
                    y='ratio_etud_prof',
                    title='Ratio Étudiants/Professeurs par Département',
                    color='ratio_etud_prof',
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig_ratio, use_container_width=True)
            else:
                st.info("Aucune statistique disponible")
        
        except Exception as e:
            st.error(f"Erreur: {e}")
    
    with tab3:
        st.header("👨‍🏫 Charge de Travail des Professeurs")
        
        try:
            charge_profs = analytics.get_professor_workload()
            
            if not charge_profs.empty:
                col_filter1, col_filter2 = st.columns(2)
                
                with col_filter1:
                    dept_filter = st.multiselect(
                        "Filtrer par département",
                        options=charge_profs['departement'].unique(),
                        default=charge_profs['departement'].unique()
                    )
                
                with col_filter2:
                    min_surv = st.slider(
                        "Nombre minimum de surveillances",
                        0,
                        int(charge_profs['nb_surveillances'].max()),
                        0
                    )
                
                filtered_df = charge_profs[
                    (charge_profs['departement'].isin(dept_filter)) &
                    (charge_profs['nb_surveillances'] >= min_surv)
                ]
                
                col_metric1, col_metric2, col_metric3 = st.columns(3)
                
                with col_metric1:
                    st.metric("Moyenne surveillances", f"{filtered_df['nb_surveillances'].mean():.1f}")
                
                with col_metric2:
                    st.metric("Maximum", int(filtered_df['nb_surveillances'].max()))
                
                with col_metric3:
                    st.metric("Minimum", int(filtered_df['nb_surveillances'].min()))
                
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                fig_hist = px.histogram(
                    filtered_df,
                    x='nb_surveillances',
                    title='Distribution des Surveillances',
                    nbins=20,
                    labels={'nb_surveillances': 'Nombre de surveillances'}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
                
                fig_box = px.box(
                    filtered_df,
                    x='departement',
                    y='nb_surveillances',
                    title='Répartition des Surveillances par Département',
                    color='departement'
                )
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("Aucune donnée de surveillance disponible")
        
        except Exception as e:
            st.error(f"Erreur: {e}")
    
    with tab4:
        st.header("💺 Occupation des Salles")
        
        try:
            occupation = analytics.get_occupation_analysis()
            
            if not occupation.empty:
                st.subheader("📅 Occupation par Jour")
                
                st.dataframe(
                    occupation,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "taux_occupation_pct": st.column_config.ProgressColumn(
                            "Taux d'occupation",
                            format="%.1f%%",
                            min_value=0,
                            max_value=100
                        )
                    }
                )
                
                fig_line = go.Figure()
                
                fig_line.add_trace(go.Scatter(
                    x=occupation['date_examen'],
                    y=occupation['taux_occupation_pct'],
                    mode='lines+markers',
                    name='Taux d\'occupation',
                    line=dict(color='blue', width=3),
                    marker=dict(size=8)
                ))
                
                fig_line.update_layout(
                    title='Évolution du Taux d\'Occupation des Salles',
                    xaxis_title='Date',
                    yaxis_title='Taux d\'occupation (%)',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_line, use_container_width=True)
                
                col_occ1, col_occ2 = st.columns(2)
                
                with col_occ1:
                    fig_bar_salles = px.bar(
                        occupation,
                        x='date_examen',
                        y='salles_utilisees',
                        title='Nombre de Salles Utilisées par Jour',
                        labels={'salles_utilisees': 'Salles utilisées'}
                    )
                    st.plotly_chart(fig_bar_salles, use_container_width=True)
                
                with col_occ2:
                    fig_bar_exams = px.bar(
                        occupation,
                        x='date_examen',
                        y='nb_examens',
                        title='Nombre d\'Examens par Jour',
                        labels={'nb_examens': 'Examens'}
                    )
                    st.plotly_chart(fig_bar_exams, use_container_width=True)
                
                avg_occupation = occupation['taux_occupation_pct'].mean()
                
                if avg_occupation < 50:
                    st.warning(f"⚠️ Taux d'occupation moyen faible: {avg_occupation:.1f}%. Optimisation possible.")
                elif avg_occupation > 90:
                    st.error(f"❌ Taux d'occupation très élevé: {avg_occupation:.1f}%. Risque de saturation.")
                else:
                    st.success(f"✅ Taux d'occupation optimal: {avg_occupation:.1f}%")
            else:
                st.info("Aucune donnée d'occupation disponible")
        
        except Exception as e:
            st.error(f"Erreur: {e}")

if __name__ == "__main__":
    main()
