import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
import numpy as np
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_results import attendance_result_dialog


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():

    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data['teacher_id']

    c1, c2 = st.columns([2, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""
            <div style="text-align: right; margin-bottom: 8px;">
                <span style="color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Teacher</span><br/>
                <strong style="color: #ffffff; font-size: 1.05rem; font-family: 'Outfit'; font-weight: 600;">{teacher_data['name']}</strong>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", type='secondary', key='logoutbtn', use_container_width=True):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data 
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
        
    tab1, tab2, tab3 = st.columns(3, gap="small")

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, use_container_width=True, icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, use_container_width=True, icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records', type=type3, use_container_width=True, icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_manage_subjects():

    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns([2, 1], vertical_alignment='center')

    with col1:
        st.markdown("<h2 style='margin: 0 !important;'>Manage Subjects</h2>", unsafe_allow_html=True)

    with col2:
        if st.button('Create Subject', type='primary', use_container_width=True, icon=':material/add:'):
            create_subject_dialog(teacher_id)

    st.space()
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Enrolled Students", sub.get('total_students', 0)),
                ("🕰️", "Classes Scanned", sub.get('total_classes', 0)),
            ]

            def share_btn(sub=sub):
                if st.button(
                    "Share Invite Code",
                    key=f"share_{sub['subject_id']}",
                    icon=":material/share:",
                    type="tertiary",
                    use_container_width=True
                ):
                    share_subject_dialog(sub['name'], sub['subject_code'])

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("You haven't created any subjects yet. Click 'Create Subject' above to start!")


def teacher_tab_take_attendance():

    teacher_id = st.session_state.teacher_data['teacher_id']
    st.markdown("<h2 style='margin: 0 !important;'>Run AI Scan</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8 !important; font-size: 0.9rem; margin-top: -5px;'>Select your subject and load classroom group photos to perform face recognition scans.</p>", unsafe_allow_html=True)

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('Please create at least one subject under the "Manage Subjects" tab before taking attendance.')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([2, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.markdown("<h3 style='margin-bottom: 1rem;'>Captured Classroom Photos</h3>", unsafe_allow_html=True)
        gallery_cols = st.columns(4, gap="small")

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'Photo {idx+1}')
                
    has_photos = bool(st.session_state.attendance_images)
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        if st.button('Clear Photos', use_container_width=True, type='secondary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('Run Analysis', use_container_width=True, type='primary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Analyzing facial features across photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('There are no students enrolled in this subject yet.')
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source Photo": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)


def teacher_tab_attendance_records():

    st.markdown("<h2 style='margin: 0 !important;'>Attendance Logs</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8 !important; font-size: 0.9rem; margin-top: -5px; margin-bottom: 2rem;'>View aggregated attendance history for all courses you conduct.</p>", unsafe_allow_html=True)
    
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found yet. Run an AI scan to log student attendance!")
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count = ('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + ' Present'
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
    )
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):

    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken!"
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match!"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully registered! You can log in now."
    except Exception as e:
        return False, "Unexpected registration error occurred!"


def login_teacher(username, password):

    if not username or not password:
        return False
    
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    
    return False

    
def teacher_screen_login():
    
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Back to Portal", type='tertiary', key='loginbackbtn', icon=':material/arrow_back:', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()
        
    st.divider()

    st.markdown("<h2 style='text-align: center; margin-top: 1rem;'>Teacher Sign In</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8 !important; margin-top: -5px; margin-bottom: 2rem; font-size: 0.9rem;'>Sign in to manage classes and review attendance reports.</p>", unsafe_allow_html=True)
    
    teacher_username = st.text_input("Username", placeholder='e.g. bruce_wayne', key='login_username')
    teacher_pass = st.text_input("Password", type='password', placeholder="Enter your password", key='login_pass')
    
    st.space()

    btnc1, btnc2 = st.columns(2, gap="medium")

    with btnc1:
        if st.button('Sign In', icon=':material/login:', shortcut='control+enter', use_container_width=True):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password combo.")

    with btnc2:
        if st.button('Register Account', type="tertiary", icon=':material/person_add:', use_container_width=True):
            st.session_state.teacher_login_type = "register"
            st.rerun() 

    footer_dashboard()


def teacher_screen_register():

    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Back to Portal", type='tertiary', key='loginbackbtn', icon=':material/arrow_back:', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.divider()

    st.markdown("<h2 style='text-align: center; margin-top: 1rem;'>Create Teacher Profile</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8 !important; margin-top: -5px; margin-bottom: 2rem; font-size: 0.9rem;'>Register a new account to organize classes and scan attendance.</p>", unsafe_allow_html=True)
    
    teacher_username = st.text_input("Username", placeholder='e.g. bruce_wayne', key='reg_username')
    teacher_name = st.text_input("Full Name", placeholder='e.g. Bruce Wayne', key='reg_name')
    teacher_pass = st.text_input("Password", type='password', placeholder="Enter password", key='reg_pass')
    teacher_pass_confirm = st.text_input("Confirm Password", type='password', placeholder="Retype password", key='reg_pass_conf')

    st.space()

    btnc1, btnc2 = st.columns(2, gap="medium")

    with btnc1:
        if st.button('Register Account', icon=':material/person_add:', shortcut='control+enter', use_container_width=True):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(1.5)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button('Sign In Instead', type="tertiary", icon=':material/login:', use_container_width=True):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()


    

    
        
