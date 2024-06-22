import os
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = 'sk-proj-NiU7UWn24sHd6XeVyku2T3BlbkFJSZ1pV9ZBk4wn5cc7wUzW'



client = OpenAI()

# Set your OpenAI API key



st.title("Condense Learning")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.text("")
topic = st.selectbox(
    "What do you want to learn?",
    ("Pride & Prejudice", "New England Trees", "The Story of the Heavens", "Yeast", "Romeo & Juliet", "Susan B. Anthony by Alma Lutz"))

st.text("")
slider_amount_of_time = st.slider("How much time would you like to spend?", 10, 120, 10, 10)
st.text("")

#The average speed of reading is 1500 characters per minute. High-speed reading means reading 5000 characters. And if a person reads more than 10,000 characters per minute, they have an ultra-fast reading speed. But is it possible to learn to read so fast?
text_length = slider_amount_of_time * 1500


pre_text = "The book title is " + str(topic) + ". The desired reading time is" + str(slider_amount_of_time) + " minutes"

condense_prompt = "Summarize the book " + str(topic) + " in " + str(text_length) + "characters. Try to return the exactly " + str(text_length) + "characters."
#condense_prompt = "Create a condensed version of " + str(topic) + "Act as a literary editor, condensing the text while preserving its core narrative and essence. Extracts: The number of extracts should depend on the desired reading time. Average reading speed is 200-250 words per minute. Calculate the total word count based on the desired reading time. For example, if the desired reading time is 5 minutes, aim for around 1000-1250 words (5 minutes * 200-250 words per minute). Use the formula: Total words = Desired reading time (in minutes) * 200-250 words per minute. Divide the total word count by 50 (the approximate word count per extract) to determine the number of extracts needed. Ensure there is a minimum of 10 extracts per chapter. Word Count: Aim for each chapter to be condensed to the calculated total word count. Each extract should be around 50 words. Integration: Ensure that the most famous passages are seamlessly integrated into the narrative. Just return chapter 1. "

st.text("")
if st.button('Condense It!'):
    with st.spinner("thinking..."):
        result = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": condense_prompt}
            ],
            max_tokens=4096,
            temperature=0.7)
        response = result.choices[0].message.content




    with st.chat_message('AI'):
        st.markdown(response)



#conversation
prompt = st.chat_input("Need to know more. Condense chat Here!")

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message('user'):
            st.markdown(message.content)
    else:
        with st.chat_message('AI'):
            st.markdown(message.content)

if prompt is not None and prompt != "":
    st.session_state.chat_history.append(HumanMessage(prompt))

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.spinner("thinking..."):
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role":"user","content":pre_text + prompt}
            ],
            max_tokens=50,
            temperature=0.7)
        response = result['choices'][0]['message']['content']

    with st.chat_message('AI'):
        st.markdown(response)

    st.session_state.chat_history.append(AIMessage(response))

