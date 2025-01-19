import streamlit as st
import requests

# Adjust to match your running Flask backend
BACKEND_URL = "http://127.0.0.1:5000"

def main():
    st.title("Model Comparison Demo")

    # Initialize session state for the responses if not already present
    if "llm_jp_172b_response" not in st.session_state:
        st.session_state.llm_jp_172b_response = "Waiting for response..."
    if "gpt_4o_response" not in st.session_state:
        st.session_state.gpt_4o_response = "Waiting for response..."
    if "llama3_405b_response" not in st.session_state:
        st.session_state.llama3_405b_response = "Waiting for response..."

    # Prompt input (up to ~8K chars)
    user_prompt = st.text_area(
        "Please type your prompt here (up to ~8K characters):",
        height=150,
        max_chars=8000
    )

    # Lay out three columns for the model responses side by side
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("LLM-JP-172B model")
        st.text_area(
            label="LLM-JP-172B model response",
            value=st.session_state.llm_jp_172b_response,
            height=200,
            key="llm_jp_172b_box"
        )

    with col2:
        st.subheader("GPT-4o model")
        st.text_area(
            label="GPT-4o model response",
            value=st.session_state.gpt_4o_response,
            height=200,
            key="gpt_4o_box"
        )

    with col3:
        st.subheader("Llama3-405B model")
        st.text_area(
            label="Llama3-405B model response",
            value=st.session_state.llama3_405b_response,
            height=200,
            key="llama3_405b_box"
        )

    # 'Compare' button
    compare_button = st.button("Compare")

    # Once 'Compare' is clicked, fetch responses and populate the session state
    if compare_button:
        # Call LLM-JP-172B
        with st.spinner("Calling LLM-JP-172B model..."):
            try:
                resp_jp = requests.post(
                    f"{BACKEND_URL}/api/llm_jp_172b",
                    json={"prompt": user_prompt},
                    timeout=60
                )
                st.session_state.llm_jp_172b_response = resp_jp.json().get(
                    "result", "No result key found."
                )
            except Exception as e:
                st.session_state.llm_jp_172b_response = f"Error: {e}"

        # Call GPT-4o
        with st.spinner("Calling GPT-4o model..."):
            try:
                resp_gpt4o = requests.post(
                    f"{BACKEND_URL}/api/gpt4o",
                    json={"prompt": user_prompt},
                    timeout=60
                )
                st.session_state.gpt_4o_response = resp_gpt4o.json().get(
                    "result", "No result key found."
                )
            except Exception as e:
                st.session_state.gpt_4o_response = f"Error: {e}"

        # Call Llama3-405B
        with st.spinner("Calling Llama3-405B model..."):
            try:
                resp_llama = requests.post(
                    f"{BACKEND_URL}/api/llama3_405b",
                    json={"prompt": user_prompt},
                    timeout=60
                )
                st.session_state.llama3_405b_response = resp_llama.json().get(
                    "result", "No result key found."
                )
            except Exception as e:
                st.session_state.llama3_405b_response = f"Error: {e}"

        # Trigger a rerun to update the UI with new responses
        st.rerun()

if __name__ == "__main__":
    main()
