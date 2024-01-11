import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import shutil
import tempfile

@st.cache_data(show_spinner="Работает модель",ttl=3)
def runningModel(text):
    os.system('docker compose up')

# Поставить путь для image2video
os.chdir(r'C:\Users\Edit-PC2\Documents\DeepFake\models\image2video\VideoCrafter')
st.set_page_config(page_title='Создание видео')
st.subheader('Загрузи фото лектора(фото должно быть шириной 512, высотой 320 пикселей)')
uplode_image = st.file_uploader('', ['png'])
if (uplode_image is not None):
    # Путь куда положить входные файлы
    with open ('C:/Users/Edit-PC2/Documents/DeepFake/models/image2video/VideoCrafter/inputs/image.png','wb') as f:
        f.write(uplode_image.read())
    st.subheader('Вы успешно загрузили файл, модель уже начала генерировать видео....')
    runningModel(uplode_image.name)
    # Путь где будут результаты
    with open('C:/Users/Edit-PC2/Documents/DeepFake/models/image2video/VideoCrafter/results/i2v_512_test/videoFromImage.mp4','rb') as result_file:
        st.subheader('Модель закончила работу. Можете посмотреть и скачать видео')
        st.download_button(label = 'Видео',data = result_file,file_name='videoFromImage.mp4')
        st.video(result_file,format='mp4')
if st.button(label = 'К предыдущему шагу'):
    switch_page('Создание_аудиодорожки')
if st.button(label = 'К следующему шагу'):
    switch_page('Создание_лекции')