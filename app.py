import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import Database
from src.auth import Auth, get_role_display_name

st.set_page_config(
    page_title="Plateforme d'Optimisation des Examens",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def get_database():
    try:
        db = Database()
        with db.get_connection() as conn:
            pass
        return db
    except Exception as e:
        return None

def init_session():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def show_db_statistics(db):
    """Display database statistics"""
    try:
        stats_query = """
        SELECT 
            (SELECT COUNT(*) FROM departements) as departements,
            (SELECT COUNT(*) FROM formations) as formations,
            (SELECT COUNT(*) FROM professeurs) as professeurs,
            (SELECT COUNT(*) FROM etudiants) as etudiants,
            (SELECT COUNT(*) FROM modules) as modules,
            (SELECT COUNT(*) FROM lieu_examen) as salles,
            (SELECT COUNT(*) FROM utilisateurs) as utilisateurs,
            (SELECT COUNT(*) FROM examens) as examens
        """
        result = db.execute_query(stats_query)
        if result:
            stats = result[0]
            
            st.markdown("### 📊 Statistiques de la Base de Données")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🏛️ Départements", stats['departements'])
                st.metric("📚 Formations", stats['formations'])
            with col2:
                st.metric("👨‍🏫 Professeurs", stats['professeurs'])
                st.metric("🎓 Étudiants", stats['etudiants'])
            with col3:
                st.metric("📖 Modules", stats['modules'])
                st.metric("🏫 Salles", stats['salles'])
            with col4:
                st.metric("👥 Utilisateurs", stats['utilisateurs'])
                st.metric("📝 Examens", stats['examens'])
            
            st.markdown("---")
    except Exception as e:
        pass

def login_form():
    st.title("Plateforme d'Examens Universitaires")
    st.markdown("### Connexion")
    
    db = get_database()
    
    if db is None:
        st.error("Impossible de se connecter a la base de donnees")
        st.stop()
    
    # Show database statistics
    show_db_statistics(db)
    
    auth = Auth(db)
    
    with st.form("login_form"):
        username = st.text_input("Email / Nom d'utilisateur", placeholder="exemple@univ.dz")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter", use_container_width=True, type="primary")
    
    if submit:
        if not username or not password:
            st.error("Veuillez remplir tous les champs")
        else:
            user = auth.authenticate(username.strip(), password)
            
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                
                role = user['role']
                page_map = {
                    'vice_doyen': 'Vice_Doyen',
                    'admin_examens': 'Admin_Examens',
                    'chef_departement': 'Chef_Departement',
                    'professeur': 'Professeurs',
                    'etudiant': 'Etudiants'
                }
                
                if role in page_map:
                    page_name = page_map[role]
                    st.markdown(f'<meta http-equiv="refresh" content="0; url=/{page_name}">', unsafe_allow_html=True)
                    st.success(f"Redirection vers {page_name}...")
                    st.stop()
                else:
                    st.rerun()
            else:
                st.error("Identifiants incorrects")
    
    st.markdown("---")
    with st.expander("Aide"):
        st.markdown("""
        ### Formats des identifiants
        - **Etudiants**: email + mot de passe (Nom+Prenom+Promo)
        - **Professeurs**: email + mot de passe fourni
        - **Administrateurs**: contactez le service informatique
        """)

def show_logged_in():
    user = st.session_state.user
    st.title("Plateforme d'Examens Universitaires")
    st.success(f"Connecte: **{user.get('prenom', '')} {user.get('nom', '')}**")
    st.info(f"Role: **{get_role_display_name(user['role'])}**")
    st.markdown("---")
    st.markdown("### Accedez a votre espace via le menu lateral")
    
    if st.button("Se deconnecter", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()

def main():
    init_session()
    if st.session_state.authenticated and st.session_state.user:
        show_logged_in()
    else:
        login_form()

if __name__ == "__main__":
    main()
