import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="StudyMatch", page_icon="🔥", layout="centered")

# 2. Initialize Session State Data
if "initialized" not in st.session_state:
    # Mock data for potential study partners in the stack
    st.session_state.potential_partners = [
        {
            "id": 1,
            "name": "Sarah Jenkins",
            "age": 20,
            "gender": "Female",
            "fav_subject": "Physics",
            "bio": "Struggling with quantum mechanics problem sets. Let's study together! I can help you with Python.",
            "avatar": "👩‍🔬"
        },
        {
            "id": 2,
            "name": "Alex Tan",
            "age": 21,
            "gender": "Male",
            "fav_subject": "Computer Science",
            "bio": "Grinding LeetCode data structures and discrete math. Looking for someone to hold me accountable.",
            "avatar": "👨‍💻"
        },
        {
            "id": 3,
            "name": "Elena Rostova",
            "age": 19,
            "gender": "Female",
            "fav_subject": "Literature",
            "bio": "Writing my thesis on 19th-century books. Down for coffee and quiet library reading sessions.",
            "avatar": "👩‍🎨"
        },
        {
            "id": 4,
            "name": "Marcus Vance",
            "age": 22,
            "gender": "Male",
            "fav_subject": "Math",
            "bio": "Prepping for calculus exams. Down for intense morning study blocks and quizzing each other.",
            "avatar": "👨‍💼"
        },
        {
            "id": 5,
            "name": "Chloe Kim",
            "age": 20,
            "gender": "Female",
            "fav_subject": "Chemistry",
            "bio": "Pre-med track. Memorizing organic chemistry pathways right now. Let's quiz each other!",
            "avatar": "👩‍⚕️"
        },
        {   
            "id": 6,
            "name": "Ivan",
            "age": 18,
            "gender": "Male",
            "fav_subject": "Physics",
            "bio": "I love using gemini.",
            "avatar": "👩‍⚕️"
        },
        {
            "id": 7,
            "name": "Jiaquan",
            "age": 18,
            "gender": "Male",
            "fav_subject": "Chemistry",
            "bio": "I hate school.",
            "avatar": "👩‍⚕️"
        }
    ]
    st.session_state.current_index = 0
    st.session_state.matches = []
    st.session_state.active_chat_id = None
    st.session_state.chats = {}  # Format: {partner_id: [messages]}
    st.session_state.initialized = True

# Custom Styles for the Tinder Profile Card Layout
st.markdown(
    """
    <style>
    .profile-card {
        background-color: #f8f9fa !important;
        border: 2px solid #e9ecef;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .profile-card h2, .profile-card h4, .profile-card p {
        color: #212529 !important;
        margin: 5px 0px;
    }
    .dark .profile-card {
        background-color: #1e222b !important;
        border: 2px solid #3e4451;
    }
    .dark .profile-card h2, .dark .profile-card h4, .dark .profile-card p {
        color: #ffffff !important;
    }
    .subject-badge {
        display: inline-block;
        background-color: #ff4b4b;
        color: white !important;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Sidebar for Navigation & Matches
with st.sidebar:
    st.title("🔥 StudyMatch")
    st.caption("Swipe right to find your ideal study partner")
    st.markdown("---")
    
    st.header("💬 Your Matches")
    if not st.session_state.matches:
        st.write("No matches yet! Keep swiping to find partners.")
    else:
        for match in st.session_state.matches:
            # Button for each matched user to open chat
            if st.button(f"{match['avatar']} Chat with {match['name']}", key=f"nav_chat_{match['id']}", use_container_width=True):
                st.session_state.active_chat_id = match['id']
                st.rerun()
                
    if st.session_state.active_chat_id is not None:
        st.markdown("---")
        if st.button("🎴 Return to Swiping Feed", use_container_width=True, type="secondary"):
            st.session_state.active_chat_id = None
            st.rerun()

# 4. App Flow Routing (View Chat vs. View Swipe Deck)

# VIEW A: The Chat Room
if st.session_state.active_chat_id is not None:
    partner = next(p for p in st.session_state.potential_partners if p["id"] == st.session_state.active_chat_id)
    
    st.title(f"💬 Chatting with {partner['name']}")
    st.write(f"Subject Focus: **{partner['fav_subject']}**")
    st.markdown("---")
    
    # Initialize message list for this user if it doesn't exist
    if partner["id"] not in st.session_state.chats:
        st.session_state.chats[partner["id"]] = []
        
    # Render chat logs
    for msg in st.session_state.chats[partner["id"]]:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])
            
    # Input field for typing messages
    if user_reply := st.chat_input(f"Send a message to {partner['name']}..."):
        st.session_state.chats[partner["id"]].append({"role": "user", "text": user_reply})
        
        # Instant mock response simulation loop
        bot_reply = f"Hey! Glad we matched! I'm completely down to work on some {partner['fav_subject']} problems together. When are you free to study?"
        st.session_state.chats[partner["id"]].append({"role": "assistant", "text": bot_reply})
        st.rerun()

# VIEW B: The Tinder Card Swiping Feed
else:
    # Check if we have run out of profiles in the card stack
    if st.session_state.current_index >= len(st.session_state.potential_partners):
        st.title("🎉 That's Everyone For Now!")
        st.subheader("You've gone through all the study profiles in your area.")
        if st.button("🔄 Reset Deck and Swipe Again", use_container_width=True):
            st.session_state.current_index = 0
            st.session_state.matches = []
            st.session_state.chats = {}
            st.rerun()
    else:
        # Get data for the person currently on top of the deck stack
        current_person = st.session_state.potential_partners[st.session_state.current_index]
        
        st.title("🎴 Find Study Partners")
        
        # Render the custom designed UI Card
        st.markdown(
            f"""
            <div class="profile-card">
                <h1 style='font-size: 60px; margin: 0;'>{current_person['avatar']}</h1>
                <h2>{current_person['name']}, {current_person['age']}</h2>
                <h4>Gender: {current_person['gender']}</h4>
                <p style="font-style: italic; margin-top: 15px;">"{current_person['bio']}"</p>
                <div class="subject-badge">📚 Fav Subject: {current_person['fav_subject']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Swiping Buttons Layout Side-By-Side
        col_left, col_right = st.columns(2)
        
        with col_left:
            if st.button("❌ Pass (Swipe Left)", key="swipe_left", use_container_width=True, type="secondary"):
                # Simply skip to the next person profile card
                st.session_state.current_index += 1
                st.rerun()
                
        with col_right:
            if st.button("💖 Like (Swipe Right)", key="swipe_right", use_container_width=True, type="primary"):
                # Add to matched list data and show a toast popup notification
                st.session_state.matches.append(current_person)
                st.toast(f"🎉 You and {current_person['name']} matched to study together!")
                
                # Advance layout state index
                st.session_state.current_index += 1
                st.rerun()