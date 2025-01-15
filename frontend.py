import streamlit as st
import requests

# Adjust to match your running Flask backend
BACKEND_URL = "http://127.0.0.1:5000"

def main():
    st.title("Model Comparison Demo")

    # Prompt input (up to ~8K chars)
    user_prompt = st.text_area(
        "Please type your prompt here (up to ~8K characters):",
        height=150,
        max_chars=8000
    )

    # 'Compare' button
    compare_button = st.button("Compare")

    # Lay out three columns for the model responses side by side
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("LLM-JP-172B model")
        # Create a text_area placeholder in advance
        llm_jp_172b_placeholder = st.empty()

    with col2:
        st.subheader("GPT-4o model")
        # Create a text_area placeholder in advance
        gpt_4o_placeholder = st.empty()

    with col3:
        st.subheader("Llama3-405B model")
        # Create a text_area placeholder in advance
        llama3_405b_placeholder = st.empty()

    # Once 'Compare' is clicked, fetch responses and populate the boxes
    if compare_button:
        # Initialize empty strings in case an error occurs
        result_jp = ""
        result_gpt4o = ""
        result_llama = ""

        # Call LLM-JP-172B (placeholder)
        with st.spinner("Calling LLM-JP-172B model..."):
            try:
                resp_jp = requests.post(
                    f"{BACKEND_URL}/api/llm_jp_172b",
                    json={"prompt": user_prompt},
                    timeout=60
                )
                result_jp = resp_jp.json().get("result", "No result key found.")
            except Exception as e:
                result_jp = f"Error: {e}"

        # Call GPT-4o
        with st.spinner("Calling GPT-4o model..."):
            try:
                resp_gpt4o = requests.post(
                    f"{BACKEND_URL}/api/gpt4o",
                    json={"prompt": user_prompt},
                    timeout=60
                )
                result_gpt4o = resp_gpt4o.json().get("result", "No result key found.")
            except Exception as e:
                result_gpt4o = f"Error: {e}"

        # Call Llama3-405B
        with st.spinner("Calling Llama3-405B model..."):
            try:
                resp_llama = requests.post(
                    f"{BACKEND_URL}/api/llama3_405b",
                    json={"prompt": user_prompt},
                    timeout=60
                )
                result_llama = resp_llama.json().get("result", "No result key found.")
            except Exception as e:
                result_llama = f"Error: {e}"

        # Update the three text areas with the results
        llm_jp_172b_placeholder.text_area(
            label="LLM-JP-172B model response",
            value=result_jp,
            height=200
        )
        gpt_4o_placeholder.text_area(
            label="GPT-4o model response",
            value=result_gpt4o,
            height=200
        )
        llama3_405b_placeholder.text_area(
            label="Llama3-405B model response",
            value=result_llama,
            height=200
        )

if __name__ == "__main__":
    main()
