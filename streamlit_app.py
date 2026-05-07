import random
import time
import streamlit as st


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="CatGPT",
    page_icon="🐾",
    layout="centered",
)

st.title("🐾 CatGPT")
st.caption("Unlimited messages 24/7.")


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Sidebar controls
# -----------------------------
with st.sidebar:
    st.header("Settings")

    min_meows = st.slider("Minimum meows", 1, 20, 3)
    max_meows = st.slider("Maximum meows", min_meows, 100, 25)

    delay_style = st.selectbox(
        "Reasoning speed",
        ["Balanced", "Fast", "Deep thinking"],
        index=0,
    )

    show_reasoning = st.toggle("Show reasoning simulation", value=True)

    if st.button("Clear chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "meow",
            }
        ]
        st.rerun()


# -----------------------------
# Helpers
# -----------------------------
def get_delay_range(style: str) -> tuple[float, float]:
    if style == "Fast":
        return 0.25, 1.0
    if style == "Deep thinking":
        return 1.5, 4.0
    return 0.75, 2.25


def make_meow_response(min_words: int, max_words: int) -> str:
    count = random.randint(min_words, max_words)
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
        min_delay, max_delay = get_delay_range(delay_style)
        thinking_time = random.uniform(min_delay, max_delay)

        if show_reasoning:
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
        else:
            time.sleep(thinking_time)

        response = make_meow_response(min_meows, max_meows)

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