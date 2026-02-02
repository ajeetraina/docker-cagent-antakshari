"""
🎤 cagent Antakshari - Web Interface
A Streamlit app to showcase AI agents playing Antakshari

Usage:
    pip install streamlit
    streamlit run streamlit_app.py
"""

import streamlit as st
import subprocess
import random

# Page config
st.set_page_config(
    page_title="cagent Antakshari 🎤",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .song-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #9333ea;
    }
    .letter-badge {
        background: #22c55e;
        color: white;
        padding: 5px 10px;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎤 cagent Antakshari 🎵")
st.caption("AI Agents Playing the Classic Indian Song Game")

# Agent info
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("🎤 **ByteBeat**")
with col2:
    st.markdown("⭐ **The Judge**")
with col3:
    st.markdown("🔥 **HypeBoi3000**")
with col4:
    st.markdown("🎧 **RemixRaja**")

st.divider()

# Session state
if 'songs' not in st.session_state:
    st.session_state.songs = []
if 'current_letter' not in st.session_state:
    st.session_state.current_letter = 'D'
if 'round' not in st.session_state:
    st.session_state.round = 0

# Game controls
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.metric("Round", st.session_state.round)

with col2:
    st.markdown(f"### Next Letter: **{st.session_state.current_letter}**")

with col3:
    if st.button("🎮 Start Game", type="primary"):
        st.session_state.songs = []
        st.session_state.round = 0
        st.session_state.current_letter = 'D'

# Theme input
theme = st.text_input("Enter a theme (optional)", placeholder="e.g., Monsoon, Love, Coding")

# Demo songs
demo_songs = [
    {
        'title': 'Dil Ki Baat',
        'lyrics': """Dil ki baat sunao zara
Pyaar ki raahon mein chalo sara
Sapne bune hain humne saath
Chhod na dena mera haath""",
        'end': 'T'
    },
    {
        'title': 'Teri Yaadein', 
        'lyrics': """Teri yaadein aati hain
Dil ko chu jaati hain
Beat drop hota hai jab
Saari duniya naachti hai""",
        'end': 'N'
    }
]

# Run Antakshari
if st.button("▶️ Next Round"):
    with st.spinner(f"🎤 Agent thinking of a song starting with '{st.session_state.current_letter}'..."):
        
        # Demo mode - sample song
        song = random.choice(demo_songs)
        st.session_state.songs.append({
            'round': st.session_state.round + 1,
            'letter': st.session_state.current_letter,
            'title': song['title'],
            'lyrics': song['lyrics'],
        })
        st.session_state.round += 1
        st.session_state.current_letter = song['end']
        st.rerun()

st.divider()

# Display songs
st.subheader("🎵 Song Feed")

for song in reversed(st.session_state.songs):
    with st.container():
        st.markdown(f"""
**Round {song['round']} - Letter: {song['letter']}**

🎤 **"{song.get('title', 'Untitled')}"**

```
{song.get('lyrics', '')}
```
        """)
        
        # Comments section
        with st.expander("💬 Show Comments"):
            st.markdown("⭐ **@TheJudge**: Wah wah! Nice transition! 7/10")
            st.markdown("🔥 **@HypeBoi3000**: THIS SLAPS BRO 🔥🔥🔥 #Antakshari")
        
        st.divider()

# Footer
st.caption("Powered by Docker cagent | Built by Collabnix Community")
st.caption("🐳 github.com/ajeetraina/docker-cagent-antakshari")
