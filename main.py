

import streamlit as st
from PyPDF2 import PdfReader
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

TEMPLATE = """""questions": [
{
    "id":1, 
    "question":"What is the purpose of assembler directives?",
    "options":[
    " A. To define segments and allocate space for variables",
    " B. To represent specific machine instructions",
    " C. To simplify the programmer's tack",
    " D. To provide information to the assembler"
    ],
    "correct_answer": " D. To provide information to the assembler"
},
{
    "id":2, 
    "question":"what are opcodes?",
    "options":[
    " A. Instrustions for integer addition and subtraction",
    " B. Instructions for memory access",
    " C. Instructions for directing the assembler",
    " D. Mbenonic codes represinting specific machine instructions"
    ],
    "correct_answer": " D. Mbenonic codes represinting specific machine instructions"

}]}"""


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text

def get_questions(text,num_questions=5 , level="Medium"):
    prompt = f"""
            Act as a teacher who is preparing a quiz for college students and create {num_questions} questions that is in {level} level. 
            The questions should be multiple-choice questions with four options for each question based on the text delimated by four backquots, 
            the responce must be formatted in JSON. Each question contains id, question, options as list, correct_answer.
            this is an example of the resoonce: {TEMPLATE}

            the text is: ''''{text}''''
             """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
        ],
    )
    return json.loads(response["choices"][0]["message"]["content"])

def display_questions(questions):
    for question in questions:
        question_id = str(question["id"])

        st.write(
            f"## Q.{question_id} \ {question['question']}",
        )



        options_text = ""
        options = question["options"]
        for option in options:
            options_text += f"-{option} \n"

        st.write(options_text)

        with st.expander("Show answer", expanded=False):
            st.write(question["correct_answer"])

        st.divider()
    st.subheader("End of questions")
    st.write("***Best of Luck💕!***")


def main():
    st.set_page_config(page_title='Quizlet_app',page_icon="📚")
    st.title(":blue[_Quizlet App_]")
    st.write("***Welcome to the simple quizlet app!***") #you can add markdown
    st.divider()

    with st.form(key="upload_file"):
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        num_of_questions = st.number_input("Number of questions", min_value=1, max_value=10, value=5)

        
        level = st.selectbox(
        "Please select the level of your quiz",
         ("Easy", "Medium", "Hard"),
         index=None,
        placeholder="Select quiz level...",
        )

        
        submitted_button = st.form_submit_button(label="Start my quiz", type='primary')

    if submitted_button:
      if uploaded_file:
            text = extract_text_from_pdf(uploaded_file)
            with st.spinner("In progress..."):
              questions = get_questions(text, num_of_questions)["questions"]
            display_questions(questions)

      else:
         st.error("Please upload a pdf file")
    

if __name__ == "__main__":
    main()