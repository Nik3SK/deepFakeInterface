import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import tempfile
import tqdm


@st.cache_data(show_spinner="Работает модель")
def runningModel(text):
    st.info(st.session_state['info_for_user1'])
    time.sleep(3)
    # os.system('docker compose up')




# Путь модели tts
os.chdir(r"C:\Users\Edit-PC2\Documents\DeepFake\models\tts3_docker_16_10")
st.set_page_config(page_title='Создание аудиодорожки')
st.title('Генерация аудиодорожки')
st.divider()
st.header('Модель text-to-speech преобразует файл с текстом в аудио.'+
          'На данном этапе генерация возможна только с голосом одного спикера мужского пола')
st.divider()
st.subheader('Загрузи тексовый файл, к примеру конспект лекции')
uplode_text = st.file_uploader('',['txt'])
st.session_state['castomize']='no'
if (uplode_text is not None):
    with open (r'C:\Users\Edit-PC2\Documents\DeepFake\models\tts3_docker_16_10\text.txt','wb') as f:
        f.write(uplode_text.read())
    st.session_state['info_for_user1']='Вы успешно загрузили файл, модель уже начала генерировать аудио....'
    st.session_state['info_for_user2']='Модель закончила работу. Можете послушать и скачать вашу аудиодорожку'
    runningModel(uplode_text.name)
    st.success(st.session_state['info_for_user2'])
    with open('output.wav','rb') as result_file:
        st.download_button(label = 'Аудиодорожка',data = result_file,file_name='output.wav')
        st.audio(result_file,format='wav')
    st.session_state['castomize']='yes'
    st.divider()
if st.session_state['castomize']=='yes':
    st.subheader('Теперь можно кастомизировать аудиодорожку')
    # путь с папкой весов модели(они должны лежать в файлах модели)
    os.chdir(r"C:\Users\Edit-PC2\Documents\DeepFake\RVC\Retrieval-based-Voice-Conversion-WebUI\assets\weights")
    all_weights_row=os.listdir()
    all_weights=[]
    for i in all_weights_row:
        if i.find('.pth')!=-1:
            all_weights.append(i[:i.find('.pth'):])
    col1, col2= st.columns(2,gap="large")
    with col1:
        st.subheader("Выберите модель для кастомизации:")
        option = st.selectbox('Список моделей', all_weights)

    with col2:
        st.subheader("Кастомизировать полученной аудио?")
        if option!=None and st.button('Да', type='primary',use_container_width=True):
            #Путь к папке с индексами
            os.chdir(fr'C:\Users\Edit-PC2\Documents\DeepFake\examplesForModels\indexesForRVC\{option}')
            index_file=os.listdir()[0]
            #Путь к папке с RVC
            os.chdir(r'C:\Users\Edit-PC2\Documents\DeepFake\RVC\Retrieval-based-Voice-Conversion-WebUI')
            os.system('python tools\infer_cli.py --f0up_key=0 '
                    #   путь к результирующему файлу tts
                      '--input_path="C:\Users\Edit-PC2\Documents\DeepFake\models\tts3_docker_16_10\output.wav"'
                    #   путь к индекс файлам
                      ' --index_path="C:\Users\Edit-PC2\Documents\DeepFake\examplesForModels\indexesForRVC\\'+option+ '\\'+index_file+ '"'
                    # путь для конечного, кастомизированного файла
                      '--opt_path="output_RVC.wav" '
                      '--model_name="' + option +'" '
                      ' --index_rate=0.66 --device=cuda:0 '
                      '--is_half=True '
                      '--filter_radius=3 '
                      '--resample_sr=0 '
                      '--rms_mix_rate=1'
                      ' --protect=0.33')
        else:
            st.error('Ты не выбрал модель')
    


if st.button(label = 'К следующему шагу'):
    switch_page('Создание_видео')
