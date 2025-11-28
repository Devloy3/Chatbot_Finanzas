import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("Finanzas Chatbot 🏦 ")

st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E;   /* Fondo general */
        color: #00FF00;              /* Texto en verde */
    }
    .stButton>button {
        background-color: #FF5733;   /* Botones en naranja */
        color: white;
    }
    .stSlider>div>div>div {
        background-color: #33FF57;   /* Color del slider */
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.header("⚙️ Configuración")
    temp = st.slider("Temperatura", 0.0, 1.0, 0.7)
    if st.button("🧹 Limpiar historial"):
        st.session_state.mensajes = []
        st.success("Historial borrado. ¡Empieza de nuevo!")

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temp)

# Inicializar el historial de mensajes en session_state
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(f"<span style='color:black; padding:5px; border-radius:5px;'>{pregunta}</span>",unsafe_allow_html=True)
    
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    system_prompt = SystemMessage(content="Responde siempre como un asesor financiero serio y profesional.")
    prompt = [system_prompt] + st.session_state.mensajes
    
    respuesta = chat_model.invoke(prompt)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)