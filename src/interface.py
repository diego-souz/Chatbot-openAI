import streamlit as st
import openfinance

def streamlit_interface():
    st.set_page_config(page_title="Chatbot Financeiro", page_icon=":money_with_wings:")
    st.title("Chatbot de cotação de ações📈")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    #Histórico de messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        elif msg["role"] == "assistant":
            if msg["content"]:
                st.chat_message("assistant").markdown(msg["content"])
    
    #Entrada de mensagem do usuário
    user_input = st.chat_input("Digite sua pergunta sobre cotação de ações: ")
    if user_input:
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)
        
        # Processa a mensagem
        st.session_state.messages = openfinance.text_gen(st.session_state.messages)

        # Exibe a resposta do chatbot
        last_message = st.session_state.messages[-1]
        if last_message["role"] == "assistant":
            st.chat_message("assistant").markdown(last_message["content"])


if __name__ == "__main__":

    streamlit_interface()