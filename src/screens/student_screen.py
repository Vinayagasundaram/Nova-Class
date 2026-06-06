import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.database.db import get_all_students, create_student, get_student_attendance, get_student_subjects, unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():

    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    c1, c2 = st.columns([2, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""
            <div style="text-align: right; margin-bottom: 8px;">
                <span style="color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Student</span><br/>
                <strong style="color: #ffffff; font-size: 1.05rem; font-family: 'Outfit'; font-weight: 600;">{student_data['name']}</strong>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", type='secondary', key='logoutbtn', use_container_width=True):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()

    st.space()

    c1, c2 = st.columns([2, 1], vertical_alignment='center')
    with c1:
        st.markdown("<h2 style='margin: 0 !important;'>Enrolled Subjects</h2>", unsafe_allow_html=True)
    with c2:
        if st.button('Enroll in Subject', type='primary', use_container_width=True, icon=':material/add:'):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    if subjects:
        cols = st.columns(2, gap="medium")
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']

            stats = stats_map.get(sid, {"total":0, "attended": 0})
            def unenroll_button(subject_id=sid, subject_name=sub['name']):
                if st.button(
                    "Unenroll from Course",
                    type='tertiary',
                    icon=':material/delete_forever:',
                    key=f"unenroll_{subject_id}",
                    use_container_width=True
                ):
                    unenroll_student_to_subject(student_id, subject_id)
                    st.toast(f"Unenrolled from {subject_name} successfully!")
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name = sub['name'],
                    code = sub['subject_code'],
                    section = sub['section'],
                    stats = [
                        ('📅', 'Classes Conducted', stats['total']),
                        ('✅', 'Classes Attended', stats['attended']),
                    ],
                    footer_callback=unenroll_button
                )
    else:
        st.info("You are not enrolled in any subjects yet. Click 'Enroll in Subject' to join a class!")

    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
        
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Back to Portal", type='tertiary', key='backtoportalbtn', icon=':material/arrow_back:', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()
    
    st.divider()

    st.markdown("<h2 style='text-align: center; margin-top: 1rem;'>Sign in with FaceID</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8 !important; margin-top: -5px; margin-bottom: 2rem; font-size: 0.9rem;'>Align your face in the center of the frame below to authenticate instantly.</p>", unsafe_allow_html=True)

    show_registration = False
    photo_source = st.camera_input("Position your face in the center", label_visibility="collapsed")

    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner('Scanning facial features...'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('No face detected. Please adjust your lighting and try again.')
            elif num_faces > 1:
                st.warning('Multiple faces detected. Please scan one person at a time.')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f'Welcome back, {student["name"]}!', icon="👋")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! If you are a new student, please complete the registration profile below.')
                    show_registration = True
                    
    if show_registration:
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.07); border-left: 4px solid #6366f1; padding: 20px; border-radius: 16px; margin-top: 30px; margin-bottom: 20px;">
                <h3 style="margin: 0; color: #ffffff; font-family: 'Outfit'; font-weight: 600; font-size: 1.2rem;">Register Student Account</h3>
                <p style="color: #94a3b8 !important; font-size: 0.85rem; margin-top: 4px; margin-bottom: 0px !important;">Create your student profile using the captured face photo above.</p>
            </div>
        """, unsafe_allow_html=True)
        
        new_name = st.text_input("Your Full Name", placeholder='E.g. Bruce Wayne')

        if st.button('Register & Login', type='primary', use_container_width=True):
            if new_name:
                with st.spinner('Creating your facial profile...'):
                    img = np.array(Image.open(photo_source))
                    encodings = get_face_embeddings(img)

                    if encodings:
                        face_emb = encodings[0].tolist()
                        response_data = create_student(
                            new_name,
                            face_embedding=face_emb
                        )

                        if response_data:
                            train_classifier()
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = response_data[0]

                            st.toast(f'Account created! Welcome, {new_name}!', icon="🎉")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error('Could not extract facial embedding. Please try taking another snapshot with clearer lighting.')
            else:
                st.warning('Please enter your full name to proceed with registration!')

    footer_dashboard()