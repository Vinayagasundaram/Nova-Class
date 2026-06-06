import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_dashboard, footer_home
from src.ui.base_layout import style_base_layout, style_background_dashboard, style_background_home

def home_screen():

    header_home()
    style_base_layout()
    style_background_home()
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 15px; margin-top: 10px;">
                <span style="font-size: 3.5rem;">🎓</span>
            </div>
            <h3 style="text-align: center; margin: 0 0 10px 0; font-family: 'Outfit', sans-serif; font-weight: 700; color: #ffffff; font-size: 1.5rem;">Student Portal</h3>
            <p style="text-align: center; font-size: 0.85rem; color: #94a3b8 !important; margin-bottom: 25px; min-height: 45px; line-height: 1.5;">
                Log in instantly using FaceID, view your enrolled subjects, and track your attendance stats.
            </p>
        """, unsafe_allow_html=True)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', key='btn_student', use_container_width=True):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 15px; margin-top: 10px;">
                <span style="font-size: 3.5rem;">💼</span>
            </div>
            <h3 style="text-align: center; margin: 0 0 10px 0; font-family: 'Outfit', sans-serif; font-weight: 700; color: #ffffff; font-size: 1.5rem;">Teacher Portal</h3>
            <p style="text-align: center; font-size: 0.85rem; color: #94a3b8 !important; margin-bottom: 25px; min-height: 45px; line-height: 1.5;">
                Create subjects, share invite codes, upload classroom photos, and run automated AI attendance scans.
            </p>
        """, unsafe_allow_html=True)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', key='btn_teacher', use_container_width=True):
            st.session_state['login_type']='teacher'
            st.rerun()

    footer_home()
