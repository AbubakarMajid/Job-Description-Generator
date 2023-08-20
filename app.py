import streamlit as st
import langchain
from langchain.llms import OpenAI
import os
import re

# api key
os.environ['OPENAI_API_KEY'] = "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"
llm = OpenAI(temperature=0, model="text-davinci-003", max_tokens=500)
st.title("Job Description Generator")
st.sidebar.subheader("Chat")

conversation = st.sidebar.empty()

# getiing inital
role_title = st.text_input("Job Role", key="job role")
if role_title:
    with st.chat_message("User"):
        st.markdown(f"Job Role: {role_title}")

job_description = st.text_input("Job Description", key="job description")
job_description = job_description.rstrip(".")
if job_description:
    with st.chat_message("User"):
        st.markdown(f"Job Description: {job_description}")

question_list = f"""Can you provide a high-level overview of the {role_title} role and its importance to the company?
What are the top 3-5 critical responsibilities for this role?
Does this role involve managing others? If so please provide some details (e.g. number of people reporting to this role, etc.)
What technical skills, such as proficiency in programming languages, data analysis tools, or ML frameworks, are crucial for this role?
What educational background or certifications are essential or desirable for this position?
Aside from technical skills, what other skills or experience are significant for this role?
What will be the key performance indicators for this role? How will their success be measured?
Can you describe a typical workday for the {role_title}?
What specific software, tools, or equipment should the candidate be proficient with?
What types of projects will the {role_title} typically be involved in?
How does this role contribute to the overall objectives of the department and the company?
To whom will the {role_title} be reporting? How does the team structure look like?
Who will the {role_title} be collaborating with frequently?
How much knowledge of our industry is required for this role?
Has this role been filled previously? If yes, what were the strengths and weaknesses of the person who previously filled this role?
What interpersonal or soft skills are crucial for this role?
What type of individual would best fit within the team and company culture?
What potential growth opportunities exist for this role within the company?
What are your expectations for this role in the first 30, 60, and 90 days?
What is the budget for this role? What is the expected salary range?
What will the selection and interview process look like for this role?
For each of the skills and experiences we've discussed, could you specify which are 'must-haves' and which are 'nice-to-haves'?
Can you describe the company's culture and values? What makes the company stand out as an employer?
What are the key benefits and perks associated with this role that we can highlight to potential candidates?
Are there any significant, high-impact projects that the {role_title} will get to work on? This can often be a significant draw for candidates.
Can you give us the email or link where people can apply for the job? Any application deadline?"""

def display_messages(messages):
    chat_text = ""
    for message in messages:
        chat_text += f"**{message['sender']}:** {message['message']}\n\n"
    return chat_text

# Check if the "Generate" button has been pressed
if not hasattr(st.session_state, 'generate_pressed'):
    st.session_state.generate_pressed = False

if role_title and job_description:
    if not st.session_state.generate_pressed:

        if st.button("GENERATE JOB DESCRIPTION", key = "gen1"):

            st.session_state.generate_pressed = True
            st.session_state.messages = []
            st.session_state.messages.append({"sender": "user", "message": f"Job Role: {role_title}, Job Description: {job_description}"})
            conversation.write(display_messages(st.session_state.messages))
            with open('CONTEXT.txt', "w", encoding="utf-8") as f:
                f.write(f"Job Role: {role_title}\n\njob_description: {job_description}\n\n")

    # Rest of the code continues to run based on user input
    if st.session_state.generate_pressed:
        Questions = llm.predict(f""""Here is the Job Description:\n{job_description}\nHere are the list of questions\n{question_list}\n\nAfter thoroughly reading the job description, Make a breakdown that which questions are not answered in the job description.""")
        
        if Questions:
            print(Questions)
            # Rest of the code for handling questions and answers
            # ...
            unanswered = "There are some unanswered questions in the job description. Kindly answer the questions"
            exists = any(message['message'] == unanswered for message in st.session_state.messages)
            with st.chat_message("Assistant"):
                    st.markdown("There are some unanswered questions in the job description. Kindly answer the questions")
                    
            if not exists:
                    st.session_state.messages.append({"sender": "Assistant", "message": "There are some unanswered questions in the job description. Kindly answer the questions"})
                    conversation.write(display_messages(st.session_state.messages))
            role_description = Questions
            if re.findall(r'\d+\.\s(.+)', role_description):
                 questions = re.findall(r'\d+\.\s(.+)', role_description)
            else:
                 questions = re.findall(r'- (.+\?)', role_description)
            list_questions = []
            for question in range(len(questions)):
                        
                               
                        answer = st.text_input(f'Question: {questions[question]}', key = f"{question}+++")
                                        
                        if answer:
                            list_questions.append(answer)
                            conversation.empty()
                            exists = any(message['message'] == answer for message in st.session_state.messages)
                            if not exists:
                                st.session_state.messages.append({"sender": "user", "message": f"{questions[question]}: {answer}"})
                            conversation.write(display_messages(st.session_state.messages))
                            with st.chat_message("user"):
                                st.write(answer)
                            with open('CONTEXT.txt', "a") as f:
                                f.write("\nQuestion:" + questions[question] + "\n" + "Answer:" + answer + "\n\n")

            with open("CONTEXT.txt", "r") as f:
                context_raw = f.read()
            context_raw = context_raw.split("\n\n")
            context_cleaned = []
            for i in context_raw:
                     if i in context_cleaned:
                          continue
                     else:
                          context_cleaned.append(i)

            context_normalized = "\n\n".join(context_cleaned)
                

            if st.button("GENERATE JOB DESCRIPTION", key = "gen2"):


                    

                
                    final_response = llm.predict(f"""Using the {context_normalized} provided, act as a specialized HR consultant to generate a thorough and compelling job description. You are required to STRICTLY utilize the information given in the context to create the job description. Here is the structure your response should follow:

                Job Title: Review the job title provided in the context. If it's clear, concise, and accurately reflects the role, keep it. If not, modify it to better match the role requirements and be easily understood by qualified candidates. Use industry-standard or recognizable job titles.

                Company Information: Based on the provided job description, write a paragraph of 3 to 4 sentences describing the company's culture, values, and industry. Use this information to portray the company as an attractive workplace.

                Job Overview & Expectations: From the provided job description, distill a paragraph of 3 to 4 sentences that give a succinct overview of the role and outline the company's expectations from the successful candidate.

                Job Duties and Responsibilities: Based on the initial job description, write 4 to 7 bullet points that clearly define the core tasks and duties involved in the role. These should be specific, actionable, and strongly tied to the job title.

                Qualifications and Skills: Divide this section into two parts based on the information given in the context. For Required qualifications and skills, list 4 to 7 bullet points of the necessary qualifications or skills for the role. For Preferred qualifications and skills, state 2 to 5 bullet points of desirable but not compulsory skills or qualifications.

                Call to Action: Generate 1 to 2 motivating sentences that include the application deadline, and an email address and/or a link for applications.

                The goal is to enhance the given job description while emphasizing the importance of the job title in attracting suitable applicants. Utilize clear, professional, and compelling language to create a job description that is appealing and easy to understand for the qualified candidates. Also follow the following best practices:
                - Replace ‘the ideal candidate’ with ‘you’
                - delete buzzwords and unnecessary qualifications
                - Use engaging subheads (e.g. “What we expect of you”)
                - Describe a day in the life 
                - Talk problems and projects
                - Set reasonable requirements
                - Use clear language
                - Avoid words related to Sexism, Racism, Tokenism, Ableism, Ageism, Elitism, Religion
                """) 
                    with st.chat_message("assistant"):
                        st.session_state.messages.append({"sender": "assistant", "message": f"{final_response}"})
                        conversation.write(display_messages(st.session_state.messages))               
                        st.write(final_response)
