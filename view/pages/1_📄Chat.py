import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
from modules.restclient import restClient


#To be able to update the changes made to modules in localhost (press r)
def reload_module(module_name):
    import importlib
    import sys
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

history_module = reload_module('modules.history')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')

ChatHistory = history_module.ChatHistory
Layout = layout_module.Layout
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar

st.set_page_config(layout="wide", page_icon="💬", page_title="Chatbot 🤖")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header("PDF, TXT, CSV")

user_api_key = utils.load_api_key()

if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key
    
    uploaded_file, data_type = utils.handle_upload(["pdf", "txt", "csv"])

    if uploaded_file:
        # Check if the file is different or not
        if("datafile" not in st.session_state or st.session_state["datafile"] != uploaded_file.name):
            st.session_state["datafile"] = uploaded_file.name
            # finetune with new data
            with st.spinner("Processing..."):
                st.session_state["session_id"] = restClient.train(
                    user_api_key,
                    uploaded_file,
                    data_type)
            print(f"Session id: {st.session_state['session_id']}")
        st.session_state["ready"] = True

        # Configure the sidebar
        sidebar.show_options()
        sidebar.about()

        
        # Initialize chat history
        history = ChatHistory()
        try:

            if st.session_state["ready"]:
                # Create containers for chat responses and user prompts
                response_container, prompt_container = st.container(), st.container()

                with prompt_container:
                    # Display the prompt form
                    is_ready, user_input = layout.prompt_form()

                    # Initialize the chat history
                    history.initialize(uploaded_file)

                    # Reset the chat history if button clicked
                    if st.session_state["reset_chat"]:
                        history.reset(uploaded_file)

                    if is_ready:
                        # Update the chat history and display the chat messages
                        history.append("user", user_input)
                        
                        old_stdout = sys.stdout
                        sys.stdout = captured_output = StringIO()

                        output = restClient.predict(
                            user_api_key,
                            str(st.session_state["session_id"]),
                            user_input,
                            st.session_state["history"], data_type)
                        
                        sys.stdout = old_stdout

                        history.append("assistant", output)

                        st.session_state["history"].append((user_input, output))

                        # Clean up the agent's thoughts to remove unwanted characters
                        thoughts = captured_output.getvalue()
                        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                        # Display the agent's thoughts
                        with st.expander("Display the agent's thoughts"):
                            st.write(cleaned_thoughts)

                history.generate_messages(response_container)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        print("file is not available")
        st.session_state["datafile"] = ""


