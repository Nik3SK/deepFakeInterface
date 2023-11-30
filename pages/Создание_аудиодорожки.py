import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import tempfile


@st.cache_data
def runningModel(text):
    time.sleep(1)
    # os.system('docker compose up')

# Путь модели tts
os.chdir('C:')
st.set_page_config(page_title='Создание аудиодорожки')
st.subheader('Загрузи конспект')
uplode_text = st.file_uploader('',['txt'])
if (uplode_text is not None):
    with open ('/inputs/text.txt','wb') as f:
        f.write(uplode_text.read())
    st.subheader('Вы успешно загрузили файл, модель уже начала генерировать аудио....')
    runningModel(uplode_text.name)
    with open('/results/audio.mp3','rb') as result_file:
        st.subheader('Модель закончила работу. Можете посмотреть и скачать вашу лекцию')
        st.download_button(label = 'Аудиодорожка',data = result_file,file_name='output.wav')
        st.audio(result_file,format='wav')
if st.button(label = 'К следующему шагу'):
    switch_page('Создание_видео')
