import streamlit as st

def style_background_home():

    st.markdown("""
        <style>
                .stApp {
                    background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 60%, #080b11 100%) !important;
                }

                .stApp div[data-testid="stColumn"] {
                    background: rgba(255, 255, 255, 0.03) !important;
                    border: 1px solid rgba(255, 255, 255, 0.08) !important;
                    backdrop-filter: blur(12px) !important;
                    padding: 2.5rem !important;
                    border-radius: 24px !important;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                }
                
                .stApp div[data-testid="stColumn"]:hover {
                    transform: translateY(-5px) !important;
                    border-color: rgba(99, 102, 241, 0.3) !important;
                    box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15) !important;
                }
        </style>  

                """
            ,unsafe_allow_html=True)
    

def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: radial-gradient(circle at top right, #0f172a 0%, #080b11 100%) !important;
                }

        </style>  

                """
            ,unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800;900&display=swap');

                 
         /* Hide Top Bar of streamlit */
                
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top:2rem !important;    
                max-width: 900px !important;
            }

            /* Typography */
            h1 {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 800 !important;
                font-size: 2.75rem !important;
                background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                margin-bottom: 1.5rem !important;
                line-height: 1.2 !important;
            }
                

            h2 {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.85rem !important;
                color: #f8fafc !important;
                margin-bottom: 1rem !important;
            }
                
            /* Default app font rule */
            .stApp, .stApp label, .stApp input, .stApp select, .stApp textarea {
                font-family: 'Inter', sans-serif !important;
            }

            /* Apply headings font */
            h1, h2, h3, h4 {
                font-family: 'Outfit', sans-serif !important;
            }

            h3, h4 {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            
            /* Apply gray color to standard markdown paragraphs only, avoiding button labels, inputs, etc. */
            div[data-testid="stMarkdownContainer"] p {
                color: #94a3b8 !important;
                line-height: 1.6 !important;
            }
            
            /* Ensure button text blocks inherit the correct button text color */
            button p, button div[data-testid="stMarkdownContainer"] p {
                color: inherit !important;
            }

            /* Restore font-family for Material Icons */
            span[data-testid="stIconMaterial"], div[data-testid="stIconMaterial"], i.material-icons {
                font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Symbols Sharp", "Material Icons" !important;
            }

            /* Custom Styled Buttons */
            button, div[data-testid="stButton"] button {
                border-radius: 12px !important;
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
                color: white !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                padding: 0.6rem 1.5rem !important;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }

            button[kind="secondary"], div[data-testid="stBaseButton-secondary"] button {
                background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%) !important;
                color: white !important;
                box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2) !important;
            }

            button[kind="tertiary"], div[data-testid="stBaseButton-tertiary"] button {
                background: rgba(255, 255, 255, 0.06) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                color: #cbd5e1 !important;
                box-shadow: none !important;
            }

            button:hover, div[data-testid="stButton"] button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35) !important;
                background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
                color: white !important;
            }

            button[kind="secondary"]:hover, div[data-testid="stBaseButton-secondary"] button:hover {
                background: linear-gradient(135deg, #fb7185 0%, #f43f5e 100%) !important;
                box-shadow: 0 6px 20px rgba(244, 63, 94, 0.35) !important;
            }

            button[kind="tertiary"]:hover, div[data-testid="stBaseButton-tertiary"] button:hover {
                background: rgba(255, 255, 255, 0.12) !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
                color: white !important;
            }
            
            button:active {
                transform: translateY(0px) !important;
            }

            /* Form & Inputs Styling */
            div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label {
                color: #cbd5e1 !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 500 !important;
                font-size: 0.9rem !important;
                margin-bottom: 0.4rem !important;
            }
            
            div[data-baseweb="input"] {
                background-color: rgba(30, 41, 59, 0.45) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 12px !important;
                transition: all 0.2s ease !important;
                padding: 2px 6px !important;
            }

            /* Make nested containers transparent to let the wrapper dark color show through */
            div[data-baseweb="input"] div {
                background-color: transparent !important;
                border: none !important;
            }

            div[data-baseweb="input"] input {
                background-color: transparent !important;
                color: #f8fafc !important;
                font-family: 'Inter', sans-serif !important;
                border: none !important;
            }

            /* Style placeholder text */
            div[data-baseweb="input"] input::placeholder {
                color: #64748b !important;
                opacity: 0.8 !important;
            }

            div[data-baseweb="input"]:focus-within {
                border-color: #6366f1 !important;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
            }

            div[data-baseweb="input"] button {
                background-color: transparent !important;
                border: none !important;
                box-shadow: none !important;
                color: #94a3b8 !important;
            }

            div[data-baseweb="input"] button:hover {
                color: #ffffff !important;
                background-color: transparent !important;
            }

            /* React Select overrides for Streamlit Selectbox */
            div[data-baseweb="select"] {
                border-radius: 12px !important;
                background-color: rgba(30, 41, 59, 0.45) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            div[data-baseweb="select"] > div {
                background-color: transparent !important;
                border: none !important;
                color: #f8fafc !important;
            }
            
            div[role="listbox"] {
                background-color: #1e293b !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 12px !important;
            }
            
            div[role="option"] {
                background-color: transparent !important;
                color: #cbd5e1 !important;
                transition: all 0.2s ease !important;
            }
            
            div[role="option"]:hover {
                background-color: rgba(99, 102, 241, 0.2) !important;
                color: white !important;
            }

            /* File Uploader and Camera Input */
            div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] {
                background-color: rgba(30, 41, 59, 0.25) !important;
                border: 1px dashed rgba(255, 255, 255, 0.12) !important;
                border-radius: 16px !important;
                padding: 1.25rem !important;
            }
            
            /* Dialog Modals overrides */
            div[data-testid="stDialog"], 
            div[data-testid="stDialog"] > div,
            div[role="dialog"], 
            div[data-baseweb="modal"] {
                background-color: #0f172a !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 24px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
            }
            
            /* Style modal close button */
            div[data-testid="stDialog"] button[aria-label="Close"],
            div[role="dialog"] button[aria-label="Close"] {
                background-color: transparent !important;
                border: none !important;
                box-shadow: none !important;
                color: #94a3b8 !important;
            }
            
            div[data-testid="stDialog"] button[aria-label="Close"]:hover,
            div[role="dialog"] button[aria-label="Close"]:hover {
                color: #ffffff !important;
                background-color: transparent !important;
            }

            /* Dividers */
            hr {
                border-color: rgba(255, 255, 255, 0.08) !important;
                margin: 2rem 0 !important;
            }

            /* Toast customization */
            div[data-testid="stToast"] {
                background-color: #1e1b4b !important;
                border: 1px solid rgba(99, 102, 241, 0.3) !important;
                border-radius: 12px !important;
                color: #ffffff !important;
            }

            /* Code Blocks */
            div[data-testid="stCodeBlock"] {
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 12px !important;
                background-color: rgba(0, 0, 0, 0.25) !important;
            }
            div[data-testid="stCodeBlock"] code {
                font-family: monospace !important;
                color: #818cf8 !important;
            }

            /* Callouts (st.info, st.warning, st.error) */
            div[data-testid="stCallout"] {
                background-color: rgba(30, 41, 59, 0.3) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-left: 4px solid #6366f1 !important;
                border-radius: 12px !important;
                color: #f8fafc !important;
            }
            div[data-testid="stCallout"] p {
                color: #cbd5e1 !important;
                font-size: 0.9rem !important;
            }
        </style>  

                """
            ,unsafe_allow_html=True)