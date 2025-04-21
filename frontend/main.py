from time import time
import requests
import streamlit as st

AUTH_SERVICE_URL = "http://auth-service:8000"
RAG_SERVICE_URL = "http://rag-service:8000"

def login(username: str, password: str):
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/token",
            data={"username": username, "password": password}
        )
        return response.json()["access_token"]
    except:
        return None

def streamlit_prompt():
    st.title("RAG ассистент по ресурсам БГУИР")

    # if 'token' not in st.session_state:
    #     with st.form("auth"):
    #         username = st.text_input("Username")
    #         password = st.text_input("Password", type="password")
    #         if st.form_submit_button("Login"):
    #             token = login(username, password)
    #             if token:
    #                 st.session_state.token = token
    #                 st.success("Logged in successfully!")
    #             else:
    #                 st.error("Invalid credentials")
    #     st.stop()

    question = st.text_input("Задайте вопрос касающийся нашего университета:")

    if st.button("Получить ответ"):
        if question:
            with st.spinner("Генерируем ответ..."):
                start_time = time()
                try:
                    response = requests.post(
                        f"{RAG_SERVICE_URL}/generate",
                        json={"question": question},
                        headers={}#"Authorization": f"Bearer {st.session_state.token}"}
                    )
                    answer = response.json()["answer"]
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    return
                
                end_time = time()
                elapsed_time = end_time - start_time

            st.success(f"Ответ был сгенерирован за {elapsed_time:.2f} секунд!")
            st.write(answer)
        else:
            st.warning("Пожалуйста введите интересующий Вас вопрос перед отправкой.")

if __name__ == "__main__":
    streamlit_prompt()