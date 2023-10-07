import streamlit as st


#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Chat-Bot 🤖")


#Contact
with st.sidebar.expander("📬 Contact"):

    st.write("**Mail** : tneurontech@gmail.com")
    st.write("**Created by TNeuronTech**")


#Title
st.markdown(
    """
    <h2 style='text-align: center;'>Chatbot 🤖</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>An intelligent chatbot created by combining 
    the strengths of Langchain and Streamlit. LLM is used to provide
    context-sensitive interactions. The goal is to help you better understand your data.
    Supported data types are PDF, TXT, CSV, Youtube transcript 🧠</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")






