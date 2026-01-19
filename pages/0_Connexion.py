import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.auth import Auth, get_role_display_name, get_role_icon

st.set_page_config(
    page_title="Connexion - Plateforme Examens",
    page_icon="",
    layout="centered"
)

@st.cache_resource
def get_database():
    try:
        return Database()
    except:
        return None

def init_session():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def login_form():
    st.title("Plateforme d'Examens")
    st.markdown("### Connexion")
    
    db = get_database()
    
    if db is None:
        st.error("Impossible de se connecter a la base de donnees")
        st.stop()
    
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
                st.success(f"Bienvenue {user.get('prenom', '')} {user.get('nom', '')}!")
                st.info(f"Role: {get_role_display_name(user['role'])}")
                st.rerun()
            else:
                st.error("Identifiants incorrects")
    
    st.markdown("---")
    with st.expander("Aide"):
        st.markdown("""
        ### Formats des identifiants
        - **Étudiants**: email + mot de passe (Nom+Prénom+Promo)
        - **Professeurs**: email + mot de passe fourni
        - **Administrateurs**: contactez le service informatique
        """)

def show_user_info():
    user = st.session_state.user
    
    if user:
        st.success(f"Connecte: **{user.get('prenom', '')} {user.get('nom', '')}**")
        st.info(f"Role: **{get_role_display_name(user['role'])}**")
        
        st.markdown("---")
        st.markdown("### Accedez a votre espace via le menu lateral")
        
        # Show available pages based on role
        role = user['role']
        if role == 'vice_doyen':
            st.markdown("- **Vice-Doyen**: Vue strategique, KPIs, validation EDT")
        elif role == 'admin_examens':
            st.markdown("- **Administration**: Generation EDT, conflits, optimisation")
        elif role == 'chef_departement':
            st.markdown("- **Departement**: Validation EDT, statistiques")
        elif role == 'professeur':
            st.markdown("- **Professeurs**: Planning personnel, charge horaire")
        elif role == 'etudiant':
            st.markdown("- **Etudiants**: Planning personnalise")
        
        st.markdown("---")
        if st.button("Se deconnecter", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

def main():
    init_session()
    
    if st.session_state.authenticated and st.session_state.user:
        show_user_info()
    else:
        login_form()

if __name__ == "__main__":
    main()
