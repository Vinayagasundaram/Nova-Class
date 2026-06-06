import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    
    html = f"""<div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.07); border-left: 5px solid #6366f1; padding: 22px; border-radius: 16px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
<h3 style="margin: 0 0 8px 0; color: #ffffff; font-family: 'Outfit', sans-serif !important; font-weight: 700; font-size: 1.35rem; letter-spacing: 0.02em;">{name}</h3>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
<span style="background: rgba(99, 102, 241, 0.15); color: #818cf8; font-family: 'Inter', sans-serif; font-size: 0.75rem; font-weight: 600; padding: 3px 10px; border-radius: 6px; border: 1px solid rgba(99, 102, 241, 0.2); letter-spacing: 0.05em;">{code}</span>
<span style="color: #64748b; font-family: 'Inter', sans-serif; font-size: 0.8rem;">&bull;</span>
<span style="color: #94a3b8; font-family: 'Inter', sans-serif; font-size: 0.8rem; font-weight: 500;">Section {section}</span>
</div>"""
    
    if stats:
        html += '<div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom: 5px;">'
        for icon, label, value in stats:
            html += f'<div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.06); padding: 6px 12px; border-radius: 10px; font-size: 0.8rem; color: #cbd5e1; display: flex; align-items: center; gap: 6px; font-family: \'Inter\', sans-serif;"><span style="font-size: 0.9rem;">{icon}</span><span><b>{value}</b> {label}</span></div>'
        html += '</div>'

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()