import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import tempfile
import tqdm
import shutil


@st.cache_data(show_spinner="Работает модель")
def runningModel(text):
    placeholder.info(st.session_state['info_for_user1'])
    time.sleep(3)
    # os.system('docker compose up')
# Путь до модели tts
os.chdir(r"C:\tts3_docker_16_10")
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
    with open (r'C:\tts3_docker_16_10\text.txt','wb') as f:
        f.write(uplode_text.read())
    st.session_state['info_for_user1']='Вы успешно загрузили файл, модель уже начала генерировать аудио....'
    st.session_state['info_for_user2']='Модель закончила работу. Можете послушать и скачать вашу аудиодорожку'
    placeholder=st.empty()
    runningModel(uplode_text.name)
    placeholder.empty()
    st.success(st.session_state['info_for_user2'])
    with open('output.wav','rb') as result_file:
        st.download_button(label = 'Аудиодорожка',data = result_file,file_name='output.wav',key='TTSfile')
        st.audio(result_file,format='wav')
    st.session_state['castomize']='yes'
    st.divider()
if st.session_state['castomize']=='yes':
    # ПЕРЕКИДЫВАНИЕ ФАЙЛА TTS В ДИРЕКТОРИЮ RVC
    os.chdir(r"C:\Users\Никита\Desktop\interface\deepFakeInterface\inputs")
    os.remove('input_file.wav')
    source = r"C:\tts3_docker_16_10\output.wav"
    destination = r"C:\Users\Никита\Desktop\interface\deepFakeInterface\inputs"
    shutil.copy2(source, destination)
    os.rename('output.wav','input_file.wav') 
    st.subheader('Теперь можно кастомизировать аудиодорожку')
    #в директорию весов для RVC модели
    os.chdir(r"C:\Users\Никита\Desktop\interface\deepFakeInterface\weights")
    all_weights_row=os.listdir()
    all_weights=[]
    for i in all_weights_row:
        all_weights.append(i[:i.find('.pth'):])
    col1, col2= st.columns(2,gap="large")
    with col1:
        if len(all_weights)==0:
            st.error('Весов для RVC моделей не обнаружено')
        else:
            st.subheader("Выберите модель для кастомизации:")
            option = st.selectbox('Список моделей', all_weights)
    with col2:
        st.subheader("Кастомизировать полученной аудио?")
        if option!=None and st.button('Да', type='primary',use_container_width=True):
            #Путь к папке с индексами
            os.chdir(fr'C:\Users\Никита\Desktop\interface\deepFakeInterface\indexes\{option}')
            index_file=os.listdir()[0]
            #Путь к папке с RVC
            # os.chdir()
            # ЗАПУСК КОНТЕЙНЕРА В ИНТЕРАКТИВНОМ РЕЖИМЕ
            command_docker_run=r"docker run -v C:\Users\Edit-PC2\Documents\DeepFake\RVC\Retrieval-based-Voice-Conversion-WebUI\inputs:/app/inputs_volume"\
            r" -v C:\Users\Edit-PC2\Documents\DeepFake\RVC\Retrieval-based-Voice-Conversion-WebUI\outputs:/app/outputs_volume "\
            r"-v C:\Users\Edit-PC2\Documents\DeepFake\RVC\Retrieval-based-Voice-Conversion-WebUI\assets\weights:/app/assets/weights"\
            r" -v C:\Users\EditPC2\Documents\DeepFake\examplesForModels\indexesForRVC:/app/indexes_volume --gpus all -it b3c15aa5f38d"
            # os.system(command_docker_run)
            # ИСПОЛНЕНИЕ КОМАНДЫ КАСТОМИЗАЦИИ
            # os.system('python tools\infer_cli.py --f0up_key=0 '
            #         #   путь к результирующему файлу tts
            #           '--input_path=""'
            #         #   путь к индекс файлам
            #           ' --index_path="C:\Users\Edit-PC2\Documents\DeepFake\examplesForModels\weightsForRVC\\'+option+'.pth'+ '\\'+index_file+ '"'
            #         # путь для конечного, кастомизированного файла
            #           '--opt_path="test_v2.wav" '
            #           '--model_name="' + option +'" '
            #           ' --index_rate=0.66 --device=cuda:0 '
            #           '--is_half=True '
            #           '--filter_radius=3 '
            #           '--resample_sr=0 '
            #           '--rms_mix_rate=1'
            #           ' --protect=0.33')
            # ВЫХОД ИЗ КОНТЕЙНЕРА
            # os.system('exit')
            time.sleep(1)
            #путь к папке с output
            os.chdir(r"C:\Users\Никита\Desktop\interface\deepFakeInterface\outputs")
            with open('output_RVC.wav','rb') as result_file:
                st.download_button(label = 'Аудиодорожка',data = result_file,file_name='output_RVC.wav',key='RVCfile')
                st.audio(result_file,format='wav')
if st.button(label = 'К следующему шагу'):
    switch_page('Создание_видео')
