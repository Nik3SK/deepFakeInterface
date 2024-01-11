import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import tempfile


@st.cache_data
def runningModel(video,audio):
    time.sleep(3)
    os.system('docker compose up')

# Путь для wav2lip
os.chdir(r"C:\Users\Edit-PC2\Documents\DeepFake\models\wav2lip")
st.set_page_config(page_title='Создание лекции')
st.subheader('Загрузи видео и аудио')
uplode_video = st.file_uploader('',['mp4'])
uplode_audio = st.file_uploader('',['mp3'])
if (uplode_video is not None) and (uplode_audio is not None):
    with open ('C:/Users/Edit-PC2/Documents/DeepFake/models/wav2lip/inputs/voice.mp3','wb') as f:
        f.write(uplode_audio.read())
    with open('C:/Users/Edit-PC2/Documents/DeepFake/models/wav2lip/inputs/video.mp4','wb') as f:
        f.write(uplode_video.read())
    st.subheader('Вы успешно загрузили файлы, модель уже начала генерировать аудио....')
    runningModel(uplode_audio.name,uplode_video.name)
    with open('results/result_voice.mp4','rb') as result_file:
        st.subheader('Модель закончила работу. Можете посмотреть и скачать вашу лекцию')
        st.download_button(label = 'Видеолекция',data = result_file,file_name='result.mp4')
        st.video(result_file,format='mp4')
if st.button(label = 'Начать сначала'):
    switch_page('Знакомство')