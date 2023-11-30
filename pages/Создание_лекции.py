import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import tempfile


@st.cache_data
def runningModel(video,audio):
    time.sleep(3)
    # os.system('docker compose up')

# Путь для wav2lip
os.chdir('C:')
st.set_page_config(page_title='Создание лекции')
st.subheader('Загрузи видео и аудио')
uplode_video = st.file_uploader('',['mp4'])
uplode_audio = st.file_uploader('',['mp3'])
if (uplode_video is not None) and (uplode_audio is not None):
    # Пути для помещения входных данных
    with open ('/inputs/video.mp3','wb') as f:
        f.write(uplode_video.read())
    with open ('/inputs/audio.mp3','wb') as f:
        f.write(uplode_audio.read())
    st.subheader('Вы успешно загрузили файл, модель уже начала генерировать аудио....')
    runningModel(uplode_video.name,uplode_audio.name)
    # Путь для подбора результата
    with open('/results/video.mp4','rb') as result_file:
        st.subheader('Модель закончила работу. Можете посмотреть и скачать вашу лекцию')
        st.download_button(label = 'Видеолекция',data = result_file,file_name='output.mp4')
        st.video(result_file,format='wav')
if st.button(label = 'Начать сначала'):
    switch_page('Знакомство')