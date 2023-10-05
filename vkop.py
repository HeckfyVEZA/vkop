import streamlit as st
from recognition_vkop import vkop_list
from vkop_plot import draw_plot
from io import BytesIO
from parameters_vkop import *
import pandas as pd
from pathlib import Path
from interpolate import forming_formula as ff
st.set_page_config(layout="wide")
st.markdown('<h1>ПОДБОР ВКОП</h1>', unsafe_allow_html=True)
z = st.columns(2)
st.session_state.object = z[0].text_input("Объект")
st.session_state.system = z[0].text_input("Номер системы")
st.session_state.orderer = z[1].text_input("Заказчик")
st.session_state.innumber = z[1].text_input("Номер проекта")
st.session_state.fromnum = '.'.join(str(z[1].date_input('от')).split("-")[::-1])
c = st.columns(3)
st.session_state.manager = c[0].selectbox("Менеджер", options=tuple(map(lambda x: ' '.join(x.split()[:2]),('Азаров Владислав Евгеньевич','Варданян Тигран Арамович','Петров Михаил Александрович','Бахтеев Павел Юрьевич','Кохно Георгий Андреевич','Калантаров Андрей Викторович','Гаврилов Константин Валерьевич','Гулина Наталья Александровна','Денисов Денис Владимирович','Грибач Павел Александрович','Здейкович Стефан','Мельников Ефим Владимирович','Влазнев Константин Александрович','Моклюк Максим Олегович','Пращук Андрей Юрьевич','Кондратьев Александр Иванович','Муханчиков Иван Михайлович','Гулин Сергей Михайлович','Дутов Александр Васильевич','Життеев Тимур Юрьевич','Бычков Максим Юрьевич','Каспир Евгений Владимирович','Мякиньков Виктор Сергеевич','Тагиров Максим Адимович','Данилов Павел Валерьевич','Мумладзе Александр Мевлудиевич','Омельченко Юрий Анатольевич','Горбунов Максим Максимович', "Цуканов Роман Евгеньевич", "Лоскутов Глеб"))))
st.session_state.engineer = c[0].selectbox("Выполнил", options=tuple(map(lambda x: ' '.join(x.split()[:2]),('Гарифов Руслан Расилевич','Колесова Вероника Александровна','Мануйлова Анастасия Олеговна','Петрова Татьяна Сергеевна','Иванов Дмитрий Анатольевич','Гришина Регина Эдуардовна','Бубнова Александра Валерьевна','Игнащенко Антон Павлович','Кушхова Наталья Владимировна','Малахов Никита Александрович','Петелин Павел Владимирович','Прохоренко Ольга Сергеевна','Царьков Игорь Владиславович','Бурын Федор Александрович','Сухов Дмитрий Сергеевич'))))
st.session_state.VKOP = c[1].selectbox("Какой ВКОП нужен?", options=("ВКОП 0", "ВКОП 1"))
st.session_state.climate = c[1].selectbox("Климатическое исполнение", options=("У1", "УХЛ1", "Т1"))
st.session_state.Q = c[2].number_input('Расход', step=1)
st.session_state.p = c[2].number_input('Статическое давление', step=1)
cols = st.columns(3)
try:
    st.session_state.ops = (f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}" for item in vkop_list(st.session_state.p, st.session_state.Q))
    vlist = vkop_list(st.session_state.p, st.session_state.Q)
    ops = [f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}" for item in vkop_list(st.session_state.p, st.session_state.Q)]
    choice = cols[0].radio("Выбор нужного вентилятора", options=ops)
    item = vlist[ops.index(choice)]
    st.session_state.plot = draw_plot(choice, st.session_state.Q, st.session_state.p)
    cols[1].image(st.session_state.plot)
    prev = pd.read_excel(Path("logs.xlsx")).to_dict()
    prev = {key: [prev[key][i] for i in prev[key].keys()] for key in prev.keys()}
    prevQ = list(map(lambda x: str(int(x)), prev["Расход"]))
    prevp = list(map(lambda x: str(int(x)), prev["Давление"]))
    prevQp = [f"{prevQ[i]}|{prevp[i]}" for i in range(len(prevQ))]
    if f"{str(int(st.session_state.Q))}|{str(int(st.session_state.p))}" in prevQp:
        indexes = [i for i in range(len(prevQp)) if prevQp[i]==f"{str(int(st.session_state.Q))}|{str(int(st.session_state.p))}"]
        if len(indexes)!=0:
            cols[1].write("Ранее под эти параметры подбирали:")
            for i in indexes:
                if prev['Корректность'][i] == "КОРРЕКТНО":
                    cols[1].write(f"{prev['Номенклатура'][i]} ({prev['Инженер'][i]})")
    cols[-1].write('\n')
    cols[-1].write('\n')
    vlist = vkop_list(st.session_state.p, st.session_state.Q)
    ops = [f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}" for item in vkop_list(st.session_state.p, st.session_state.Q)]
    item = vlist[ops.index(choice)]
    cols[-1].write(f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}")
    kluch = findall(r"-(\d\d\d-)", item[0])[0]+'Н'+findall(r"(-\d\d\d\d\d/\d)-", item[0])[0]
    item[2] = ff(df[kluch], list_p, st.session_state.Q)
    cols[-1].write(f"Статическое давление (расчётное) {int(item[2])} Па")
    cols[-1].image(image_vkop[st.session_state.VKOP])
    gdf = gaba_vkop[st.session_state.VKOP][item[0]]
    gdf = {key:[str(gdf[key])] for key in gdf.keys()}
    cols[-1].dataframe(gdf)
    if st.session_state.VKOP[-1]=='0':
        st.session_state.stam = cols[-1].selectbox('Стакан', options = (f"СТАМ 401-{stam[item[0].split('-')[0]]}-Н",f"СТАМ 401-{stam[item[0].split('-')[0]]}-Н-MV220",f"СТАМ 401-{stam[item[0].split('-')[0]]}-Н-MV220У",f"СТАМ 400-{stam[item[0].split('-')[0]]}-Н",f"СТАМ 405-{stam[item[0].split('-')[0]]}-Н",))
        st.session_state.pek = cols[-1].selectbox('Переходник крышный', options=(f"ПЕК-ОСА-{item[0].split('-')[0]}-С",))
        dops = ["Дополнительное оборудование", f"Стакан монтажный {st.session_state.stam}", f"Переходник крышный {st.session_state.pek}"]
    else:
        dops = []
    from temp_fill import doc_fil
    st.write("Нажмите, пожалуйста, на одну из нижеидущих кнопок.")
    corr = st.button("Подобрано корректно")
    uncorr = st.button("Подобрано НЕкорректно")
    st.markdown("---")
    if corr:
        df = pd.read_excel(Path("logs.xlsx")).to_dict()
        df = {key: [df[key][i] for i in df[key].keys()] for key in df.keys()}
        df['Номенклатура'].append(f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}")
        df['Инженер'].append(st.session_state.engineer)
        df['Расход'].append(st.session_state.Q)
        df['Давление'].append(st.session_state.p)
        df['Корректность'].append("Корректно".upper())
        pd.DataFrame(df).to_excel(Path("logs.xlsx"), index=False)
    elif uncorr:
        df = pd.read_excel(Path("logs.xlsx")).to_dict()
        df = {key: [df[key][i] for i in df[key].keys()] for key in df.keys()}
        df['Номенклатура'].append(f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}")
        df['Инженер'].append(st.session_state.engineer)
        df['Расход'].append(st.session_state.Q)
        df['Давление'].append(st.session_state.p)
        df['Корректность'].append("неКорректно".upper())
        pd.DataFrame(df).to_excel(Path("logs.xlsx"), index=False)
    st.download_button('Скачать лист подбора', data=doc_fil([f"{st.session_state.innumber} от {st.session_state.fromnum}",st.session_state.orderer,st.session_state.object,st.session_state.system,st.session_state.manager,st.session_state.engineer,f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}",st.session_state.Q,st.session_state.p,item[1],item[2],image_vkop[st.session_state.VKOP],st.session_state.plot,gdf,dops]), file_name=f"{st.session_state.system}.docx")
except Exception as er:
    pass
    st.write(er)
