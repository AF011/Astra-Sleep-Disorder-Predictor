import pickle as pkl 
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Astra: The Sleep Predictor",
    page_icon="🏥",
    layout='wide',
    initial_sidebar_state="collapsed")

gender_mapping = {
    "Female": 0,
    "Male": 1
}

occupation_mapping = {
    "Accountant": 0,
    "Doctor": 1,
    "Engineer": 2,
    "Lawyer": 3,
    "Manager": 4,
    "Nurse": 5,
    "Sales Representative": 6,
    "Salesperson": 7,
    "Scientist": 8,
    "Software Engineer": 9,
    "Teacher": 10
}

body_type_mapping = {
    "Normal": 0,
    "Normal Weight": 1,
    "Obese": 2,
    "Overweight": 3,
}

blood_pressure_mapping = {
    "115/75": 0,
    "115/78": 1,
    "117/76": 2,
    "118/75": 3,
    "118/76": 4,
    "119/77": 5,
    "120/80": 6,
    "121/79": 7,
    "122/80": 8,
    "125/80": 9,
    "125/82": 10,
    "126/83": 11,
    "128/84": 12,
    "128/85": 13,
    "129/84": 14,
    "130/85": 15,
    "130/86": 16,
    "131/86": 17,
    "132/87": 18,
    "135/88": 19,
    "135/90": 20,
    "139/91": 21,
    "140/90": 22,
    "140/95": 23,
    "142/92": 24,
}

sleep_disorder = {
    "Insomnia": 0,
    "Your are Healthy": 1,
    "Sleep Apnea": 2
}

bot_avatar = "🤖"  # Bot emoji
user_avatar = "🧑"  # User emoji

with open('sleep_disorder_pred_RF.pickle', 'rb') as f:
  RF_Model = pkl.load(f)

questions = [
    ("Gender", "Select your Gender", list(gender_mapping.keys()), "selectbox"),
    ("Age", "Enter your age", (10, 100), "number_input"),
    ("Occupation", "Select your Occupation", list(occupation_mapping.keys()), "selectbox"),
    ("Sleep_Duration", "Sleep Duration per Day", (1, 20), "number_input"),
    ("Quality_of_Sleep", "Quality of Sleep", (1, 10), "slider"),
    ("Physical_Activity_Level", "Physical Activity Level", (30, 90), "slider"),
    ("Stress_Level", "Stress Level", (1, 10), "slider"),
    ("BMI_Category", "Select the Body Type", list(body_type_mapping.keys()), "selectbox"),
    ("Blood_Pressure", "Select the Blood Pressure", list(blood_pressure_mapping.keys()), "selectbox"),
    ("Heart_Rate", "Enter your Heart Rate", (30, 250), "number_input")
]

def predict(responses):
    # Convert categorical responses to their numerical mappings
    responses["Gender"] = gender_mapping[responses["Gender"]]
    responses["Occupation"] = occupation_mapping[responses["Occupation"]]
    responses["BMI_Category"] = body_type_mapping[responses["BMI_Category"]]
    responses["Blood_Pressure"] = blood_pressure_mapping[responses["Blood_Pressure"]]

    # Ensure the order of features matches the model's expected input
    ordered_responses = [
        responses["Gender"],
        responses["Age"],  # Assuming Age is directly input as a numerical value
        responses["Occupation"],
        responses["Sleep_Duration"],  # Assuming directly input as a numerical value
        responses["Quality_of_Sleep"],  # Assuming directly input as a numerical value
        responses["Physical_Activity_Level"],  # Assuming directly input as a numerical value
        responses["Stress_Level"],  # Assuming directly input as a numerical value
        responses["BMI_Category"],
        responses["Blood_Pressure"],
        responses["Heart_Rate"]  # Assuming directly input as a numerical value
    ]

    # Convert to a 2D NumPy array
    response_arr = np.array([ordered_responses])

    # Perform prediction
    prediction = RF_Model.predict(response_arr)
    return prediction

def footer():
    # Footer Section
    st.markdown('<style>div.block-container{padding-bottom: 100px;}</style>', unsafe_allow_html=True)
    st.markdown("""---""")
    st.markdown("""
        ### 🚀 Let's Connect!
        This Application is Developed by **Abdul Faheem** with 💡 and 🥤. If you have any questions or just want to connect, feel free to reach out!
        
        <p align="left">
          <a href="https://www.linkedin.com/in/abdulfaheem011/" target="_blank">
            <img src="https://img.icons8.com/fluent/48/000000/linkedin.png" alt="LinkedIn" style="width:40px;"/>
          </a>
          <a href="https://github.com/abdulfaheemaf" target="_blank">
            <img src="https://img.icons8.com/fluent/48/000000/github.png" alt="GitHub" style="width:40px;"/>
          </a>
          <a href="mailto:abdulfaheemaf11@gmail.com">
            <img src="https://img.icons8.com/fluent/48/000000/mail.png" alt="Email" style="width:40px;"/>
          </a>
        </p>
        
        Cheers,
        
        -AF011
    """, unsafe_allow_html=True)

def main():
    col1, col2 = st.columns(2)
    col1.title('DreamCatcher: Your Guardian of Nightly Peace')
    col1.caption('### RestAssured: Your Sleep Wellness Companion')
    col2.image('sleep_disorder.png', use_column_width=False, width=300)
    
    st.divider()
    
    st.write("Hi, I'm Astra, your guide to better sleep. Let's get started on understanding your sleep health.")

    # Initialize or update the current question index
    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = 0
    if 'responses' not in st.session_state:
        st.session_state['responses'] = {}
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Display chat history
    for msg in st.session_state['chat_history']:
        st.write(msg)

    current_question = st.session_state['current_question']
    responses = st.session_state['responses']

    if current_question < len(questions):
        var, label, lst, choice = questions[current_question]
        res = None
        if choice == 'selectbox':            
            res = st.selectbox(f"{bot_avatar} {label}", lst)
        elif choice == 'number_input':
            res = st.number_input(f"{bot_avatar} {label}", lst[0], lst[1])
        elif choice == 'slider':
            res = st.slider(f"{bot_avatar} {label}", max_value=lst[1], min_value=lst[0], value=lst[0])

        if st.button("Hey Astra, Next Question...!"):
            question_msg = f"{bot_avatar} {label}"
            response_msg = f"{user_avatar} {res}"
            st.session_state['chat_history'].append(question_msg)
            st.session_state['chat_history'].append(response_msg)
            
            responses[var] = res  # Store response
            st.session_state['current_question'] += 1  # Increment question index for next question
            
            # Use rerun or directly proceed to next question
            st.experimental_rerun()
    else:
        # Once all questions have been asked
        st.write("You've completed all the questions. Here are your responses:")
        # You can add your prediction logic here using the 'responses' list

        result = predict(responses)

        if result == 1:  # If the sleep disorder is 1
            color = "green"
            st.balloons()
        else:
            color = "red"
        
        sleep_disorder_result = list(sleep_disorder.keys())[list(sleep_disorder.values()).index(result)]

        larger_text = f"<h2 style='color: {color};'>The Condition of your health as per your details is {sleep_disorder_result} 🛏</h2>"
        st.markdown(larger_text, unsafe_allow_html=True)
        st.warning(
            "Note: This M.L application only based on your details as our model achieved 89% accuracy. However, it's always recommended to consult a doctor for a comprehensive evaluation if you are dealing with any disorder.")
        hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
        st.markdown(hide_menu_style, unsafe_allow_html=True)

    footer()
        
if __name__ == '__main__':
    main()
