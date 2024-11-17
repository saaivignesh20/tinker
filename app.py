import streamlit as st
from PIL import Image
from include.model import ConversationModel
from include.prepare_input import read_from_pdf, read_from_image, read_from_excel

# Initialize ConversationModel
conversation_model = ConversationModel()

# Streamlit app setup
st.title("Conversational Bot with File Support")
st.write("Upload a document or ask a follow-up question!")

# Display the conversation history
if conversation_model.memory.get_messages():
    st.subheader("Conversation History")
    for entry in conversation_model.memory.get_messages():
        if entry['role'] == 'user':
            st.write(f"**You**: {entry['content']}")
        else:
            st.write(f"**Bot**: {entry['content']}")

# File upload widget
uploaded_file = st.file_uploader("Upload a file (PDF, Image, Excel)", type=[
    "pdf", "jpg", "jpeg", "png", "xls", "xlsx"])


# Handle file uploads
if uploaded_file:
    try:
        if uploaded_file.type == "application/pdf":
            content = read_from_pdf(uploaded_file)
        elif uploaded_file.type in ["image/jpeg", "image/png"]:
            content = read_from_image(image=Image.open(uploaded_file))
        elif uploaded_file.type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            content = read_from_excel(uploaded_file)
        else:
            content = None

        if content:
            st.success("File content processed successfully!")
            st.text_area("Extracted Text", content, height=200)
            conversation_model.memory.add_message(
                "user", f"Here is the document: {content}")
        else:
            st.error(
                "Failed to process the file. Unsupported file type or content.")

    except Exception as e:
        st.error(f"Error processing file: {e}")


# Text input for follow-up question
# question = st.text_input("Your Question", "")

if 'selected_question' in st.session_state:
    # Update the question in the text input field
    question = st.text_input(
        "Your Question", st.session_state.selected_question)
else:
    # Default to empty if no question is selected
    question = st.text_input("Your Question", "")


# Handle button click for submitting a question
if st.button("Submit") or getattr(st.session_state, "selected_question", "").strip():
    if not question.strip() or not getattr(st.session_state, "selected_question", "").strip() and not uploaded_file:
        st.error("Please enter a question or upload a file.")
    else:

        if getattr(st.session_state, "selected_question", "").strip():
            input_text = st.session_state.selected_question
        elif question.strip():
            input_text = question
        else:
            input_text = content

        # Add the user message and get a response from the bot
        conversation_model.memory.add_message("user", input_text)
        response = conversation_model.get_response(input_text)

        # Add bot response to the conversation memory
        conversation_model.memory.add_message("bot", response)

        # Display the bot response (JSON format)
        # if "response" in response:
        #     st.success(f"**tinker**: {response['response']}")
        #     if "questions" in response:
        #         st.button(
        #             f"**Think more**: {', '.join(response['questions'])}")
        # else:
        #     st.warning("Error: Could not generate a valid JSON response.")

        if "response" in response:
            # cleaned_response = response['response'].replace('```', '')
            st.success(
                f"**tinker**: {response['response']}")
            if "questions" in response:
                st.write("***Tink more !!!!***")
                for question in response['questions']:
                    st.button(f"{question}")
                    st.session_state.selected_question = question
        else:
            st.warning("Error: Could not generate a valid JSON response.")
