import random
import time
import streamlit as st


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="MeowGPT",
    page_icon="🐾",
    layout="centered",
)

st.title("🐾 MeowGPT")
st.caption("A highly advanced feline reasoning chatbot.")


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Helpers
# -----------------------------
def make_meow_response() -> str:
    count = random.randint(3, 25)
    return " ".join(["meow"] * count)


def stream_response(text: str):
    output = ""

    for token in text.split(" "):
        output += token + " "
        yield output
        time.sleep(random.uniform(0.025, 0.09))


# -----------------------------
# Render previous messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Chat input
# -----------------------------
prompt = st.chat_input("Message MeowGPT...")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        thinking_time = random.uniform(0.75, 2.25)

        thinking_steps = [
            "Reading your question...",
            "Consulting advanced feline intuition...",
            "Pawing through possible answers...",
            "Formulating response...",
        ]

        status_box = st.empty()

        elapsed = 0.0
        while elapsed < thinking_time:
            status_box.info(random.choice(thinking_steps))
            pause = random.uniform(0.35, 0.8)
            time.sleep(pause)
            elapsed += pause

        status_box.empty()

        response = make_meow_response()

        placeholder = st.empty()
        final_text = ""

        for partial in stream_response(response):
            final_text = partial
            placeholder.markdown(final_text + "▌")

        placeholder.markdown(final_text.strip())

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )