import streamlit as st

def footer_home():

    st.markdown(f"""
        <div style="margin-top:5rem; margin-bottom: 1.5rem; display:flex; flex-direction: column; gap:10px; justify-content:center; align-items:center; opacity: 0.7;">
            <div style="height: 1px; width: 150px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.15), transparent);"></div>
            <p style="font-size:0.75rem; color:#64748b !important; font-family: 'Inter', sans-serif; margin:0; letter-spacing: 0.05em; text-align: center;">
                NovaClass &bull; Created by <strong style="color: #ffffff;">Vinayagasundaram Sabapathy</strong>
            </p>  
        </div>
                
                """, unsafe_allow_html=True)


def footer_dashboard():

    st.markdown(f"""
        <div style="margin-top:5rem; margin-bottom: 1.5rem; display:flex; flex-direction: column; gap:10px; justify-content:center; align-items:center; opacity: 0.6;">
            <div style="height: 1px; width: 150px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);"></div>
            <p style="font-size:0.75rem; color:#64748b !important; font-family: 'Inter', sans-serif; margin:0; text-align: center;">
                NovaClass &bull; Created by <strong style="color: #ffffff;">Vinayagasundaram Sabapathy</strong>
            </p>  
        </div>
                
                """, unsafe_allow_html=True)