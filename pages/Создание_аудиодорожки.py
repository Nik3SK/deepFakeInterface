import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import tempfile
os.chdir('C:/tts3_docker_16_10')
st.set_page_config(page_title='Создание аудиодорожки')
uplode_text = st.file_uploader('Загрузи конспект', ['txt','docx'])
if (uplode_text is not None):
    with open ('C:/tts3_docker_16_10/text.txt','wb') as f:
        f.write(uplode_text.read())
    st.subheader('Вы успешно загрузили файл, модель уже начала генерировать аудио....')
    with st.spinner('Работает модель'):
        os.system('docker compose up')
    with open('output.wav','rb') as result_file:
        st.subheader('Модель закончила работу. Можете посмотреть и скачать вашу лекцию')
        st.download_button(label = 'Аудиодорожка',data = result_file,file_name='output.wav')
        st.audio(result_file,format='wav')
if st.button(label = 'К предыдущему шагу'):
    switch_page('Знакомство')