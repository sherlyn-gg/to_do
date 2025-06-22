import streamlit as st
from PIL import Image
from datetime import date
import base64

# Page config
st.set_page_config(page_title="To Do List", page_icon="📝", layout="wide")

# --- User credentials ---
USER_CREDENTIALS = {
    "keziya": "intotheunknown",
    "sherlyn": "samuel127"
}

# --- Session state initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Login Page ---
def show_login():
    with open("static/loginar.jpg", "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
            }}

            .login-box h2 {{
                text-align: center;
                margin-bottom: 20px;
                color: #da8ab0;
            }}

            label {{
                color: black !important;
                font-weight: bold;
            }}

            .stTextInput, .stPasswordInput {{
                max-width: 250px;
                margin-left: auto;
                margin-right: auto;
            }}

            input, .stTextInput > div > div, .stPasswordInput > div > div {{
                background-color: #f0f0f0 !important;
                color: black !important;
                border-radius: 5px;
            }}

            .stButton > button {{
                border-radius: 5px !important;
                background-color: #da8ab0 !important;
                color: black !important;
            }}

            .stButton {{
                display: flex;
                justify-content: center;
                margin-top: 10px;
            }}

            div[data-testid="stAlert"][role="alert"] {{
                background-color: #f0d5a6 !important;
                color: black !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 16px !important;
            }}

            div[data-testid="stAlert"][role="alert"] p {{
                color: black !important;
                font-weight: 600 !important;
                font-size: 16px !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="login-box"><h2><i><b> login ♡ྀི ₊</b></i></h2>', unsafe_allow_html=True)
            username = st.text_input("Username", key="username_input")
            password = st.text_input("Password", type="password", key="password_input")
            login_clicked = st.button("Login")
            st.markdown("</div>", unsafe_allow_html=True)

            if login_clicked:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")


# --- To-Do App ---
def show_todo():
    from streamlit_sortables import sort_items

    st.markdown("""
        <style>
            .stApp {
                background-color: #e3c6da;
                color: white !important;
            }
            input, textarea, select {
                background-color: white !important;
                color: black !important;
            }
            section[data-testid="stSidebar"] {
                background-color: white !important;
                color: black !important;
            }
            .stButton > button {
                background-color: white !important;
                color: black !important;
            }
            div[data-testid="stAlert-info"] {
                background-color: #d4e8ef !important;
                color: white !important;
                border-left: 5px solid #1f77b4;
            }
                /* Force override of the red drag box */
            div[role="listbox"] > div {
                background-color: #8bbcda !important;
                color: black !important;
                border-radius: 10px !important;
                padding: 8px 16px !important;
                font-weight: bold;
            }

            /* While dragging */
            div[role="option"] {
                background-color: #8bbcda !important;
                color: black !important;
            }

            /* Fix red drag box from streamlit_sortables */
            .sortable-item {
                background-color: #8bbcda !important;
                color: black !important;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar top
    st.sidebar.image("static/marst.png", use_container_width=True)
    menu = st.sidebar.selectbox("Menu", ["📌 Add Task", "✅ View Tasks", "❌ Clear Completed"])

    # Sidebar bottom user box
    st.sidebar.markdown("<div style='height: 300px;'></div>", unsafe_allow_html=True)  # Push content down
    st.sidebar.markdown(f"""
        <div style='
            padding: 10px;
            background-color: #f0d5a6;
            color: black;
            text-align: center;
            border-radius: 8px;
            margin-bottom: 10px;
            font-weight: bold;
        '>
            👤 Logged in as {st.session_state.username}
        </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Main Content
    st.image("static/march.jpg", use_container_width=True)

    if menu == "📌 Add Task":
        st.title("Add a New Task")
        col1, col2 = st.columns(2)
        with col1:
            task_text = st.text_input("✍ Task Name")
        with col2:
            due_date = st.date_input("📅 Due Date", date.today())

        status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
        is_priority = st.checkbox("⭐ Mark as Priority")

        if st.button("➕ Add Task"):
            if task_text:
                st.session_state.tasks.append({
                    "task": task_text,
                    "done": status == "Done",
                    "status": status,
                    "date": due_date,
                    "priority": is_priority
                })
                st.success(f"Added task: {task_text}")
            else:
                st.warning("Please enter a task.")

    elif menu == "✅ View Tasks":
        st.title("📝 Your Tasks")
        if st.session_state.tasks:
            task_labels = [f"{'⭐' if t.get('priority') else '☆'} {t['task']}" for t in st.session_state.tasks]
            sorted_labels = sort_items(task_labels, direction="vertical")
            label_to_task = {f"{'⭐' if t.get('priority') else '☆'} {t['task']}": t for t in st.session_state.tasks}
            st.session_state.tasks = [label_to_task[label] for label in sorted_labels]

            for i, t in enumerate(st.session_state.tasks):
                col1, col2, col3, col4 = st.columns([0.05, 0.05, 0.55, 0.35])
                with col1:
                    checked = st.checkbox("", key=f"check_{i}", value=t["done"])
                with col2:
                    if st.button("⭐" if t["priority"] else "☆", key=f"star_{i}"):
                        st.session_state.tasks[i]["priority"] = not t["priority"]
                with col3:
                    st.markdown(
                        f"<span style='text-decoration: {'line-through' if checked else 'none'};'>{t['task']}</span>",
                        unsafe_allow_html=True
                    )
                with col4:
                    st.markdown(
                        f"<span style='color:{'green' if t['status'] == 'Done' else 'orange' if t['status'] == 'Doing' else '#8bbcda'}'>"
                        f"{t['status']} — {t['date']}</span>", unsafe_allow_html=True
                    )
                st.session_state.tasks[i]["done"] = checked
        else:
            st.info("No tasks yet. Try adding one!")

    elif menu == "❌ Clear Completed":
        st.title("Clear Completed Tasks")
        completed = [t for t in st.session_state.tasks if t["done"]]
        if not completed:
            st.info("No completed tasks to clear.")
        else:
            if st.button("Clear Completed Tasks"):
                st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]
                st.success("Completed tasks cleared!")

    st.markdown("<hr><center>made by sherlyn samuel</center><hr>", unsafe_allow_html=True)

# --- Main Logic ---
if not st.session_state.logged_in:
    show_login()
else:
    show_todo()
