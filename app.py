import streamlit as st
from pathlib import Path

from config import APP_NAME, APP_VERSION
from database import get_conversations, initialize_database
from assistant import AURA

from modules.notes import add_note, delete_note, get_notes
from modules.reminders import (
    add_reminder,
    complete_reminder,
    delete_reminder,
    get_reminders
)
from modules.tasks import (
    add_task,
    complete_task,
    delete_task,
    get_task_statistics,
    get_tasks
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AURA - AI Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# SESSION STATE
# ============================================================

if "assistant" not in st.session_state:
    st.session_state.assistant = AURA()

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# LOAD FRONTEND CSS
# ============================================================

def load_css():

    css_file = Path("frontend/styles.css")

    if css_file.exists():

        with open(
            css_file,
            "r",
            encoding="utf-8"
        ) as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-logo">
                <div class="logo-icon">🤖</div>
                <div>
                    <h2>AURA</h2>
                    <p>AI Personal Assistant</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            "### Navigation"
        )

        page = st.radio(
            "Navigation",
            [
                "💬 AI Assistant",
                "🏠 Dashboard",
                "✅ Tasks",
                "📝 Notes",
                "⏰ Reminders",
                "🕘 History"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown(
            """
            <div class="sidebar-features">

            <h4>✨ AURA Features</h4>

            <p>🤖 AI Intent Detection</p>
            <p>✅ Smart Task Management</p>
            <p>📝 Personal Notes</p>
            <p>⏰ Reminders</p>
            <p>🧮 Calculator</p>
            <p>🔎 Intelligent Search</p>
            <p>📊 Productivity Analytics</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.caption(
            f"{APP_NAME} v{APP_VERSION}"
        )

    return page


# ============================================================
# TOP HEADER
# ============================================================

def header():

    st.markdown(
        """
        <div class="aura-header">

            <div>
                <h1>🤖 AURA</h1>
                <p>Your intelligent personal assistant</p>
            </div>

            <div class="status-badge">
                🟢 AI Online
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AI ASSISTANT PAGE
# ============================================================

def assistant_page():

    header()

    st.markdown(
        """
        <div class="welcome-card">

            <div class="welcome-icon">
                🤖
            </div>

            <div>
                <h2>Hello! I'm AURA 👋</h2>

                <p>
                    I can help you manage tasks, save notes,
                    calculate expressions, search information
                    and organize your productivity.
                </p>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### 💬 Conversation"
    )

    if not st.session_state.messages:

        st.info(
            "Start a conversation with AURA below. "
            "Try: **add task complete my Python project**"
        )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    prompt = st.chat_input(
        "Ask AURA something..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        response, intent, confidence = (
            st.session_state.assistant.process(
                prompt
            )
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        with st.chat_message("assistant"):

            st.markdown(response)

            with st.expander(
                "🧠 AI Analysis"
            ):

                col1, col2 = st.columns(2)

                col1.metric(
                    "Detected Intent",
                    intent
                )

                col2.metric(
                    "Confidence",
                    f"{confidence:.1%}"
                )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    header()

    st.markdown(
        "### 📊 Productivity Overview"
    )

    stats = get_task_statistics()

    notes = get_notes()

    reminders = get_reminders()

    conversations = get_conversations()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📋 Total Tasks",
        stats["total"]
    )

    col2.metric(
        "✅ Completed",
        stats["completed"]
    )

    col3.metric(
        "📝 Notes",
        len(notes)
    )

    col4.metric(
        "💬 Conversations",
        len(conversations)
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.markdown(
            "### 🎯 Task Progress"
        )

        if stats["total"] > 0:

            percentage = (
                stats["completed"]
                / stats["total"]
            )

            st.progress(
                percentage
            )

            st.write(
                f"**{percentage:.1%}** of your tasks completed"
            )

        else:

            st.info(
                "No tasks yet. Add your first task!"
            )

    with right:

        st.markdown(
            "### ⏰ Reminders"

        )

        pending_reminders = [
            reminder
            for reminder in reminders
            if not reminder["completed"]
        ]

        if pending_reminders:

            for reminder in pending_reminders[:5]:

                st.write(
                    f"⏰ **{reminder['title']}**"
                )

                st.caption(
                    reminder["reminder_time"]
                )

        else:

            st.info(
                "No pending reminders."
            )

    st.divider()

    st.markdown(
        "### 🚀 Quick Actions"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="quick-card">
                <h3>✅ Tasks</h3>
                <p>Organize your daily work.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="quick-card">
                <h3>📝 Notes</h3>
                <p>Keep your ideas organized.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="quick-card">
                <h3>🧠 AI</h3>
                <p>Let AURA understand your requests.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TASK PAGE
# ============================================================

def tasks_page():

    header()

    st.markdown(
        "### ✅ Task Manager"
    )

    stats = get_task_statistics()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Tasks",
        stats["total"]
    )

    col2.metric(
        "Completed",
        stats["completed"]
    )

    col3.metric(
        "Pending",
        stats["pending"]
    )

    st.divider()

    with st.form("add_task_form"):

        st.markdown(
            "### ➕ Add New Task"
        )

        title = st.text_input(
            "Task title",
            placeholder="Example: Complete Python project"
        )

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        submitted = st.form_submit_button(
            "➕ Add Task"
        )

        if submitted:

            if title.strip():

                add_task(
                    title,
                    priority
                )

                st.success(
                    "Task added successfully! 🎉"
                )

                st.rerun()

            else:

                st.warning(
                    "Please enter a task title."
                )

    st.divider()

    st.markdown(
        "### 📋 Your Tasks"
    )

    tasks = get_tasks()

    if not tasks:

        st.info(
            "You don't have any tasks yet."
        )

        return

    for task in tasks:

        col1, col2, col3, col4 = st.columns(
            [0.08, 0.52, 0.18, 0.22]
        )

        with col1:

            st.write(
                "✅"
                if task["completed"]
                else "⬜"
            )

        with col2:

            st.markdown(
                f"**#{task['id']} — {task['title']}**"
            )

        with col3:

            st.write(
                task["priority"]
            )

        with col4:

            if not task["completed"]:

                if st.button(
                    "Complete",
                    key=f"complete_{task['id']}"
                ):

                    complete_task(
                        task["id"]
                    )

                    st.rerun()

            else:

                if st.button(
                    "Delete",
                    key=f"delete_{task['id']}"
                ):

                    delete_task(
                        task["id"]
                    )

                    st.rerun()


# ============================================================
# NOTES PAGE
# ============================================================

def notes_page():

    header()

    st.markdown(
        "### 📝 Personal Notes"
    )

    with st.form("note_form"):

        title = st.text_input(
            "Note title",
            placeholder="Example: Machine Learning Ideas"
        )

        content = st.text_area(
            "Note content",
            placeholder="Write your note here...",
            height=160
        )

        submitted = st.form_submit_button(
            "💾 Save Note"
        )

        if submitted:

            if (
                title.strip()
                and content.strip()
            ):

                add_note(
                    title,
                    content
                )

                st.success(
                    "Note saved successfully! 📝"
                )

                st.rerun()

            else:

                st.warning(
                    "Please enter both title and content."
                )

    st.divider()

    notes = get_notes()

    if not notes:

        st.info(
            "No notes available."
        )

        return

    for note in notes:

        with st.expander(
            f"📝 {note['title']}"
        ):

            st.write(
                note["content"]
            )

            st.caption(
                f"Created: {note['created_at']}"
            )

            if st.button(
                "🗑️ Delete Note",
                key=f"note_delete_{note['id']}"
            ):

                delete_note(
                    note["id"]
                )

                st.rerun()


# ============================================================
# REMINDERS PAGE
# ============================================================

def reminders_page():

    header()

    st.markdown(
        "### ⏰ Reminder Manager"
    )

    with st.form("reminder_form"):

        title = st.text_input(
            "Reminder",
            placeholder="Example: Submit assignment"
        )

        reminder_time = st.text_input(
            "Date and time",
            placeholder="2026-09-15 18:30"
        )

        submitted = st.form_submit_button(
            "⏰ Create Reminder"
        )

        if submitted:

            if (
                title.strip()
                and reminder_time.strip()
            ):

                add_reminder(
                    title,
                    reminder_time
                )

                st.success(
                    "Reminder created successfully! ⏰"
                )

                st.rerun()

            else:

                st.warning(
                    "Please enter all details."
                )

    st.divider()

    reminders = get_reminders()

    if not reminders:

        st.info(
            "No reminders available."
        )

        return

    for reminder in reminders:

        col1, col2, col3 = st.columns(
            [0.5, 0.3, 0.2]
        )

        with col1:

            status = (
                "✅"
                if reminder["completed"]
                else "⏰"
            )

            st.write(
                f"{status} **{reminder['title']}**"
            )

        with col2:

            st.write(
                reminder["reminder_time"]
            )

        with col3:

            if not reminder["completed"]:

                if st.button(
                    "Done",
                    key=f"rem_done_{reminder['id']}"
                ):

                    complete_reminder(
                        reminder["id"]
                    )

                    st.rerun()

            else:

                if st.button(
                    "Delete",
                    key=f"rem_delete_{reminder['id']}"
                ):

                    delete_reminder(
                        reminder["id"]
                    )

                    st.rerun()


# ============================================================
# HISTORY PAGE
# ============================================================

def history_page():

    header()

    st.markdown(
        "### 🕘 Conversation History"
    )

    conversations = get_conversations()

    if not conversations:

        st.info(
            "No conversations yet."
        )

        return

    for conversation in conversations:

        with st.expander(
            f"💬 Conversation #{conversation['id']}"
        ):

            st.markdown(
                f"**👤 You:**  \n"
                f"{conversation['user_message']}"
            )

            st.markdown(
                f"**🤖 AURA:**  \n"
                f"{conversation['assistant_response']}"
            )

            st.caption(
                f"Intent: {conversation['intent']} • "
                f"{conversation['created_at']}"
            )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    load_css()

    page = sidebar()

    if page == "💬 AI Assistant":

        assistant_page()

    elif page == "🏠 Dashboard":

        dashboard_page()

    elif page == "✅ Tasks":

        tasks_page()

    elif page == "📝 Notes":

        notes_page()

    elif page == "⏰ Reminders":

        reminders_page()

    elif page == "🕘 History":

        history_page()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()