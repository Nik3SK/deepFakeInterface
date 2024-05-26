import os
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import tempfile
import shutil
import subprocess
import docker
import datetime
client = docker.from_env()


# путь до tts модели
way_tts="C:/Users/Edit-PC2/Documents/DeepFake/teratts_model/teratts"
# путь до входного файла tts модели
way_tts_input_file='C:/Users/Edit-PC2/Documents/DeepFake/teratts_model/teratts/inputOutput/text.txt'
# путь до выходного файла tts модели
way_tts_output_file="C:/Users/Edit-PC2/Documents/DeepFake/teratts_model/teratts/inputOutput/final.wav"
# путь до RVC модели
way_RVC="C:/Users/Edit-PC2/Documents/DeepFake/RVC/Retrieval-based-Voice-Conversion-WebUI"
# путь до директории для входного файла RVC
way_RVC_inputs="C:/Users/Edit-PC2/Documents/DeepFake/RVC/Retrieval-based-Voice-Conversion-WebUI/inputs"
# путь до директории весов для RVC модели
way_RVC_weights="C:/Users/Edit-PC2/Documents/DeepFake/RVC/Retrieval-based-Voice-Conversion-WebUI/assets/weights"
# путь до директории с индексами для RVC
way_RVC_indexes='C:/Users/Edit-PC2/Documents/DeepFake/examplesForModels/indexesForRVC'
# путь до директории с выходным файлом RVC
way_RVC_outputs="C:/Users/Edit-PC2/Documents/DeepFake/RVC/Retrieval-based-Voice-Conversion-WebUI/outputs"
@st.cache_data(show_spinner='Вы успешно загрузили файл, модель генерирует аудио')
def runningModel(text):
    # placeholder.info(st.session_state['info_for_user1'])
    client.containers.run('tera',volumes=['C:/Users/Edit-PC2/Documents/DeepFake/teratts_model/teratts/inputOutput:/code/data',],auto_remove=True)
# Путь до модели tts
os.chdir(way_tts)
st.set_page_config(page_title='Создание аудиодорожки')
st.title('Генерация аудиодорожки')
st.divider()
st.header('Модель text-to-speech преобразует файл с текстом в аудио.'+
          ' В данной реализации возможна генерация голосом одного спикера женского пола и кастомизация аудиофайла')
st.divider()
st.subheader('Загрузите тексовый файл, к примеру конспект лекции')
uplode_text = st.file_uploader('',['txt'])
st.session_state['castomize']='no'
if (uplode_text is not None):
    with open (way_tts_input_file,'wb') as f:
        f.write(uplode_text.read())
    st.session_state['info_for_user2']='Модель закончила работу. Можете послушать и скачать вашу аудиодорожку'
    placeholder=st.empty()
    runningModel(uplode_text.name)
    placeholder.empty()
    st.success(st.session_state['info_for_user2'])
    with open(way_tts_output_file,'rb') as result_file:
        st.download_button(label = 'Аудиодорожка',data = result_file,file_name='output.wav',key='TTSfile')
        st.audio(result_file,format='wav')
    st.session_state['castomize']='yes'
    st.divider()
if st.session_state['castomize']=='yes':
    # ПЕРЕКИДЫВАНИЕ ФАЙЛА TTS В ДИРЕКТОРИЮ RVC
    os.chdir(way_RVC_inputs)
    if len(os.listdir(way_RVC_inputs)) != 0:
        os.remove('input_file.wav')
    source = way_tts_output_file
    destination =way_RVC_inputs
    shutil.copy2(source, destination)
    os.rename('final.wav','input_file.wav') 
    st.subheader('Теперь можно кастомизировать аудиодорожку')
    #в директорию весов для RVC модели
    os.chdir(way_RVC_weights)
    all_weights_row=os.listdir()
    all_weights=[]
    for i in all_weights_row:
        if '.pth' in i:
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
            os.chdir(way_RVC_indexes+'/'+option)
            index_file=os.listdir()[0]
            #Путь к папке с RVC
            os.chdir(way_RVC)
            # ЗАПУСК RVC КОНТЕЙНЕРА для генерирования кастомизированной аудио, сразу после выполнения контейнер останавливается
            commnand='python tools/infer_cli.py --f0up_key=0 --input_path="inputs_volume/input_file.wav"'\
                     ' --index_path="indexes_volume/'+option+'/'+index_file+'"'\
                    ' --f0method=harvest --opt_path="outputs_volume/output_RVC.wav" --model_name="'+option+'.pth" '\
                    '--index_rate=0.66 --device=cuda:0 --is_half=True --filter_radius=3 --resample_sr=0 --rms_mix_rate=1 --protect=0.33'
            
            with st.spinner('Модель кастомизирует аудио...'):
                client.containers.run('rvc_final_version',commnand,volumes=['C:\\Users\Edit-PC2\Documents\DeepFake\RVC\Retrieval-based-Voice-Conversion-WebUI\inputs:/app/inputs_volume',
                                                            'C:\\Users\Edit-PC2\Documents\DeepFake\RVC\Retrieval-based-Voice-Conversion-WebUI\outputs:/app/outputs_volume',
                                                            'C:\\Users\Edit-PC2\Documents\DeepFake\RVC\Retrieval-based-Voice-Conversion-WebUI\\assets\weights:/app/assets/weights',
                                                            'C:\\Users\Edit-PC2\Documents\DeepFake\examplesForModels\indexesForRVC:/app/indexes_volume'],  
                                                            device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])],auto_remove=True)
            #путь к папке с output
            os.chdir(way_RVC_outputs)
            with open('output_RVC.wav','rb') as result_file:
                st.download_button(label = 'Аудиодорожка',data = result_file,file_name='output_RVC.wav',key='RVCfile')
                st.audio(result_file,format='wav')
if st.button(label = 'К следующему шагу'):
    switch_page('Создание_видео')
