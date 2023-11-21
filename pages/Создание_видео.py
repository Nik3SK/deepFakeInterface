import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import shutil
import tempfile
# Поставить путь для wav2lip
os.chdir('C:/tts3_docker_16_10')
st.set_page_config(page_title='Создание видео')
uplode_audio = st.file_uploader('Загрузи аудио', ['mp3'])
uplode_video = st.file_uploader('Загрузи аудио', ['mp4'])
if (uplode_audio is not None) and (uplode_video is not None):
    with open ('C:/tts3_docker_16_10/audio.mp3','wb') as f:
        f.write(uplode_audio.read())
    with open('C:/tts3_docker_16_10/video.mp4','wb') as f:
        f.write(uplode_video.read())
    st.subheader('Вы успешно загрузили файлы, модель уже начала генерировать аудио....')
    with st.spinner('Работает модель'):
        time.sleep(4)
        # os.system('docker compose up')
    with open('results/result.mp4','rb') as result_file:
        st.subheader('Модель закончила работу. Можете посмотреть и скачать вашу лекцию')
        st.download_button(label = 'Видеолекция',data = result_file,file_name='result.mp4')
        st.video(result_file,format='mp4')
if st.button(label = 'В начало'):
    switch_page('Знакомство')