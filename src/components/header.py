import streamlit as st
import base64
import os

def get_logo_src():
    logo_path = os.path.join(os.path.dirname(__file__), "..", "ui", "logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                return f"data:image/png;base64,{encoded_string}"
        except Exception:
            pass
    return "https://i.ibb.co/YTYGn5qV/logo.png"

def header_home():
    logo_src = get_logo_src()
    
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:40px; margin-top:20px">
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.25); display: flex; align-items: center; justify-content: center;">
                <img src='{logo_src}' style='height:64px;' />
            </div>
            <h1 style='text-align:center; margin-top: 20px; margin-bottom: 0px !important; font-family: "Outfit", sans-serif !important; font-weight: 900 !important; font-size: 2.75rem !important; letter-spacing: 0.15em !important; background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; line-height: 1.1;'>NOVACLASS</h1>
            <p style='text-align:center; color:#94a3b8 !important; font-family: "Inter", sans-serif; font-size: 0.85rem; margin-top: 5px; margin-bottom: 0px !important; letter-spacing: 0.15em; font-weight: 500; text-transform: uppercase;'>AI-powered attendance platform</p>
        </div>   
                
                """, unsafe_allow_html=True)
    
def header_dashboard():
    logo_src = get_logo_src()
    
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:flex-start; gap:16px; margin-bottom: 10px; margin-top: 10px;">
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); padding: 10px; border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <img src='{logo_src}' style='height:40px;' />
            </div>
            <div style="display: flex; flex-direction: column;">
                <h2 style='text-align:left; margin: 0 !important; font-family: "Outfit", sans-serif !important; font-weight: 800 !important; font-size: 1.45rem !important; letter-spacing: 0.08em !important; color: #ffffff !important; line-height: 1.1;'>NOVACLASS</h2>
            </div>
        </div>   
                
                """, unsafe_allow_html=True)