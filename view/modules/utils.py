import os
import pandas as pd
import streamlit as st
import pdfplumber
from enum import Enum
class DataType(int, Enum):
    PDF = 1
    TEXT = 2
    CSV = 3
    EXCEL = 4
    VIDEO = 5

    def getDataType(datatype: str):
        if datatype in ['pdf', '.pdf']:
            return DataType.PDF
        if datatype in ['txt', '.txt', 'text']:
            return DataType.TEXT
        if datatype in ['csv', '.csv']:
            return DataType.CSV
        if datatype in ['xlsx',  '.xlsx', 'xls', '.xls']:
            return DataType.EXCEL
        

class Utilities:

    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or 
        from the user's input and returns it
        """
        if not hasattr(st.session_state, "api_key"):
            st.session_state.api_key = None
        #you can define your API key in .env directly
        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
            st.sidebar.success("API key loaded from .env", icon="🚀")
        else:
            if st.session_state.api_key is not None:
                user_api_key = st.session_state.api_key
                st.sidebar.success("API key loaded from previous input", icon="🚀")
            else:
                user_api_key = st.sidebar.text_input(
                    label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
                )
                if user_api_key:
                    st.session_state.api_key = user_api_key

        return user_api_key

    
    @staticmethod
    def handle_upload(file_types):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """
        text_data = ""
        data_type = 0
        uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        if uploaded_file is not None:
            
            def show_csv_file(uploaded_file):
                file_container = st.expander("Your CSV file :")
                uploaded_file.seek(0)
                shows = pd.read_csv(uploaded_file)
                file_container.write(shows)
                return shows

            def show_pdf_file(uploaded_file):
                file_container = st.expander("Your PDF file :")
                with pdfplumber.open(uploaded_file) as pdf:
                    pdf_text = ""
                    for page in pdf.pages:
                        pdf_text += page.extract_text() + "\n\n"
                file_container.write(pdf_text)
                return pdf_text
            
            def show_txt_file(uploaded_file):
                file_container = st.expander("Your TXT file:")
                uploaded_file.seek(0)
                content = uploaded_file.read().decode("utf-8")
                file_container.write(content)
                return content
            
            def get_file_extension(uploaded_file):
                return os.path.splitext(uploaded_file)[1].lower()
            
            file_extension = get_file_extension(uploaded_file.name)
            # Show the contents of the file based on its extension
            if file_extension== ".pdf" : 
                show_pdf_file(uploaded_file)
                data_type  = DataType.getDataType(file_extension)
            elif file_extension== ".txt" : 
                show_txt_file(uploaded_file)
            
            data_type  = DataType.getDataType(file_extension)

        else:
            st.session_state["reset_chat"] = True
        
        return uploaded_file, data_type


    
