"""
Session management module for Streamlit authentication
"""

import streamlit as st
from typing import List, Optional

def init_session():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    init_session()
    return st.session_state.authenticated and st.session_state.user is not None

def get_current_user() -> Optional[dict]:
    """Get current logged in user"""
    init_session()
    return st.session_state.user if st.session_state.authenticated else None

def get_user_role() -> Optional[str]:
    """Get current user's role"""
    user = get_current_user()
    return user['role'] if user else None

def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user = None

def require_auth(allowed_roles: List[str] = None):
    """
    Require authentication to access a page
    Returns True if access granted, stops execution otherwise
    """
    init_session()
    
    if not is_authenticated():
        st.error("🔒 Accès refusé - Veuillez vous connecter")
        st.info("👉 Utilisez la page **Connexion** dans le menu latéral.")
        
        with st.expander(" Connexion rapide"):
            show_quick_login()
        
        st.stop()
        return False
    
    user = get_current_user()
    
    if allowed_roles and user['role'] not in allowed_roles:
        st.error("🚫 Accès non autorisé")
        st.warning(f"Votre rôle **{get_role_display_name(user['role'])}** n'a pas accès à cette page.")
        
        st.markdown("###  Rôles autorisés:")
        for role in allowed_roles:
            st.markdown(f"- {get_role_icon(role)} {get_role_display_name(role)}")
        
        st.stop()
        return False
    
    return True

def show_quick_login():
    """Show a quick login form"""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from src.database import Database
    from src.auth import Auth
    
    try:
        db = Database()
        auth = Auth(db)
        
        username = st.text_input("Email", key="quick_login_user")
        password = st.text_input("Mot de passe", type="password", key="quick_login_pass")
        
        if st.button("Se connecter", key="quick_login_btn"):
            if username and password:
                user = auth.authenticate(username.strip(), password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.success(" Connexion réussie!")
                    st.rerun()
                else:
                    st.error(" Identifiants incorrects")
            else:
                st.warning("Remplissez tous les champs")
    except Exception as e:
        st.error(f"Erreur: {e}")

def show_user_sidebar():
    """Show user info in sidebar"""
    user = get_current_user()
    
    if user:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 Connecté")
        name = f"{user.get('prenom', '')} {user.get('nom', '')}".strip()
        if name:
            st.sidebar.markdown(f"**{name}**")
        st.sidebar.markdown(f"{get_role_icon(user['role'])} {get_role_display_name(user['role'])}")
        
        if st.sidebar.button(" Déconnexion", use_container_width=True):
            logout()
            st.rerun()

def get_role_display_name(role: str) -> str:
    """Get display name for a role"""
    role_names = {
        'vice_doyen': 'Vice-Doyen / Doyen',
        'admin_examens': 'Administrateur des Examens',
        'chef_departement': 'Chef de Département',
        'professeur': 'Professeur',
        'etudiant': 'Étudiant'
    }
    return role_names.get(role, role)

def get_role_icon(role: str) -> str:
    """Get icon for a role"""
    role_icons = {
        'vice_doyen': '',
        'admin_examens': '',
        'chef_departement': '',
        'professeur': '',
        'etudiant': ''
    }
    return role_icons.get(role, '👤')
