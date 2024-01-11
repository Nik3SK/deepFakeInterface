import streamlit as st
import time
st.set_page_config(page_title="Знакомство")
from streamlit_extras.switch_page_button import switch_page
st.title('Генерация видеолекций на основе фото, аудио и конспекта')
st.subheader('Автоматическое создание контента с использование генеративных моделей')
if st.button(label='Хочу попробовать',type='primary'):
    switch_page('Создание_аудиодорожки')
# uplode_audio = st.file_uploader('Загрузи аудио', ['mp3'])
# uplode_text = st.file_uploader('Загрузи конспект', ['txt','docx'])
# if (uplode_audio is not None) or (uplode_text is not None):
#     st.subheader('Вы успешно загрузили все файлы, модель уже начала генерировать видео....')
#     time.sleep(5)
#     result_file = open('Mot.mp4','rb')
#     result_play = result_file.read()
#     st.subheader('Модель закончила работу. Можете посмотреть и скачать вашу лекцию')
#     st.download_button('Видеолекция','Mot.mp4')
#     st.video(result_play)
