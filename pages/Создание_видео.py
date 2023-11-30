import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import shutil
import tempfile

@st.cache_data
def runningModel(image):
    time.sleep(2)
    pass
    # os.system('docker compose up')

# Поставить путь для image2video
os.chdir('C:')
st.set_page_config(page_title='Создание видео')
st.subheader('Загрузи фото лектора')
uplode_image = st.file_uploader('', ['jpeg'])
if (uplode_image is not None):
    # Путь куда положить входные файлы
    with open ('/inputs/image.jpeg','wb') as f:
        f.write(uplode_image.read())
    st.subheader('Вы успешно загрузили файлы, модель уже начала генерировать аудио....')
    runningModel(uplode_image.name)
    # Путь где будут результаты
    with open('/results/video.mp4','rb') as result_file:
        st.subheader('Модель закончила работу. Можете посмотреть и скачать видео')
        st.download_button(label = 'Видео',data = result_file,file_name='result.mp4')
        st.video(result_file,format='mp4')
if st.button(label = 'К предыдущему шагу'):
    switch_page('Создание_аудиодорожки')
if st.button(label = 'К следующему шагу'):
    switch_page('Создание_лекции')