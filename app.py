import streamlit as st
import database as db
import os
import random

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Couple Connect 💖", page_icon="💖", layout="centered")


def load_css():
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e1e2f, #2d1b33); color: white; }
    .card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 10px; }
    .score-box { background: linear-gradient(90deg, #ff4b6e, #ff8a71); padding: 15px; border-radius: 12px; text-align: center; font-size: 22px; font-weight: bold; margin-top: 10px;}
    .stButton>button { border-radius: 20px; transition: 0.3s; width: 100%; border: none; height: 45px; font-weight: bold; cursor: pointer;}
    .stButton>button:hover { transform: translateY(-3px); background-color: #ff4b6e !important; color: white !important; box-shadow: 0px 5px 15px rgba(255, 75, 110, 0.4); }
    .note-paper { background: #fff9c4; color: #333; padding: 10px; border-radius: 5px; border-left: 5px solid #fbc02d; margin-bottom: 5px; font-family: 'Comic Sans MS', cursive;}
    </style>
    """, unsafe_allow_html=True)


load_css()
db.create_table()


# 🧠 RULE-BASED ADVISOR
def get_rule_based_advice(q):
    q = q.lower()
    if any(word in q for word in ["fight", "angry", "argument", "jhogra"]):
        return "Stay calm. Being the first to say 'Sorry' shows how much you value the relationship. 💕"
    elif any(word in q for word in ["gift", "surprise"]):
        return "A handwritten note or cooking their favorite meal is a priceless gift! 🎁"
    elif any(word in q for word in ["trust", "doubt"]):
        return "Trust is built through honesty. Be transparent and keep your promises."
    else:
        return "Mutual love, patience, and respect are the keys to a perfect relationship! ❤️"


# ---------------- LOGIN / SIGNUP ----------------
if "user" not in st.session_state: st.session_state.user = None
if "show_game" not in st.session_state: st.session_state.show_game = False

st.markdown("<h1 style='text-align: center; color: #ff4b6e;'>💖 Couple Connect 💖</h1>", unsafe_allow_html=True)
menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

if menu == "Signup":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    u, p = st.text_input("Username").strip(), st.text_input("Password", type="password").strip()
    if st.button("Signup"):
        if u and p:
            try:
                db.add_user(u, p); st.success("Account created!")
            except:
                st.error("User exists.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Login":
    if st.session_state.user is None:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        u, p = st.text_input("Username").strip(), st.text_input("Password", type="password").strip()
        if st.button("Login"):
            if db.login(u, p):
                st.session_state.user = u; st.rerun()
            else:
                st.error("Wrong credentials!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        user, partner = st.session_state.user, db.get_user(st.session_state.user)[2]

        if partner is None:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            p_name = st.text_input("Partner's Name")
            if st.button("Connect 💕"):
                if db.get_user(p_name):
                    db.set_partner(user, p_name);
                    db.set_partner(p_name, user);
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # 🔔 TOASTS
            latest_msgs = db.get_messages(user)
            if latest_msgs:
                for s, m in latest_msgs[::-1][:1]:
                    if "MOOD:" in m: st.toast(f"🔔 {s} is feeling {m.split(':')[1]}", icon="🎭")
                    if "QUIZ_ANS:" in m: st.toast(f"🔔 {s} answered a quiz!", icon="📝")

            st.markdown(f"<div class='card'><h3 style='text-align:center;'>💑 {user} & {partner}</h3>",
                        unsafe_allow_html=True)

            # --- MOOD SHARING (New Feature) ---
            st.write("Share your mood with your partner:")
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                if st.button("😊 Happy"): db.send_message(user, partner, "MOOD: Happy 😊")
            with m2:
                if st.button("🥰 Love"): db.send_message(user, partner, "MOOD: In Love 🥰")
            with m3:
                if st.button("🥺 Sad"): db.send_message(user, partner, "MOOD: Sad 🥺")
            with m4:
                if st.button("😤 Angry"): db.send_message(user, partner, "MOOD: Angry 😤")

            # Action Buttons
            st.markdown("---")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button("💌 Miss You"): db.send_message(user, partner, "Miss you! 💕")
            with c2:
                if st.button("❤️ Love You"): db.send_message(user, partner, "Love you! ❤️")
            with c3:
                if st.button("🤗 Hugs"): db.send_message(user, partner, "Sending a big Hug 🤗")
            with c4:
                if st.button("🎮 Game Mode"): st.session_state.show_game = not st.session_state.show_game

            # 🎮 PREMIUM GAME SECTION
            if st.session_state.show_game:
                st.markdown("---")
                t1, t2, t3, t4, t5 = st.tabs(["Daily Task 🎯", "Quiz 📝", "Gifts 🎁", "Truth 🎲", "Notes 📝"])

                with t1:
                    tasks = [
                        "Call your partner and tell them why they are special.",
                        "Send a picture of your favorite memory together.",
                        "Write a 3-line poem for your partner.",
                        "Plan a virtual movie date for tonight.",
                        "Compliment your partner on something they recently achieved."
                    ]
                    st.info(f"**Today's Challenge:** {random.choice(tasks)}")
                    if st.button("Task Completed! ✅"):
                        db.send_message(user, partner, "TASK: I completed today's challenge! 🏆")
                        st.balloons()

                with t2:
                    quiz_50 = ["Favorite Food?", "First Date?", "Dream Trip?", "Favorite Song?", "Biggest Fear?",
                               "My Shoe Size?", "Eye Color?", "Morning/Night person?", "Dream Job?",
                               "Favorite Memory?"]  # Add more to reach 50
                    sel_q = st.selectbox("Pick a Question", quiz_50)
                    ans = st.text_input("Your Answer")
                    if st.button("Submit"):
                        db.save_answer(user, sel_q, ans)
                        db.send_message(user, partner, f"QUIZ_ANS: Answered '{sel_q}'")

                with t3:
                    gift = st.selectbox("Choose Gift", ["🌹 Rose", "🍫 Chocolate", "💍 Ring", "📱 iPhone", "🧸 Teddy"])
                    if st.button("Send"):
                        db.send_message(user, partner, f"SENT_GIFT:{gift}")

                with t4:
                    truth_pool = ["What fell you for me?", "Most attractive thing about me?", "Biggest secret?",
                                  "Future dream?"]
                    sel_t = st.selectbox("Pick a Truth Challenge", truth_pool)
                    if st.button("Send Truth"):
                        db.send_message(user, partner, f"TRUTH: {sel_t}")

                with t5:
                    st.write("### 📝 Leave a Love Note")
                    note = st.text_area("Write something sweet...")
                    if st.button("Post Note"):
                        if note:
                            db.send_message(user, partner, f"NOTE: {note}")
                            st.success("Note posted!")

            # Love Score Display
            match_count, _ = db.count_matches(user, partner)
            st.markdown(f"<div class='score-box'>🔥 Love Score: {match_count * 50 + 100}</div>", unsafe_allow_html=True)

            # Messages Display (Showing Notes separately)
            st.markdown("---")
            st.subheader("📬 Recent Activity")
            msgs = db.get_messages(user)
            for s, m in msgs[::-1][:6]:
                if "NOTE:" in m:
                    st.markdown(f"<div class='note-paper'><b>{s} wrote:</b><br>{m.replace('NOTE:', '')}</div>",
                                unsafe_allow_html=True)
                elif "MOOD:" in m:
                    st.warning(f"🎭 {s} is feeling: {m.split(':')[1]}")
                elif "SENT_GIFT:" in m:
                    st.success(f"🎁 {s} sent a {m.replace('SENT_GIFT:', '')}")
                elif "TRUTH:" in m:
                    st.error(f"🎲 Truth Challenge: {m.replace('TRUTH:', '')}")
                else:
                    st.info(f"**{s}:** {m}")

            # 🤖 ADVISOR
            st.markdown("---")
            st.subheader("🤖 Couple Advisor")
            user_q = st.text_input("Ask advice (Fight, Date, Gift...)")
            if st.button("Get Advice"):
                if user_q: st.info(get_rule_based_advice(user_q))

        if st.sidebar.button("Logout"):
            st.session_state.user = None;
            st.rerun()