import streamlit as st
from recognition_vkop import vkop_list
from vkop_plot import draw_plot
from io import BytesIO
from parameters_vkop import *
import pandas as pd
from pathlib import Path
from re import findall
from interpolate import forming_formula as ff
import json
from interpolate import kpd_find
st.set_page_config(layout="wide")
def json_fo(infoss):
        return json.dumps(infoss)
st.markdown('<h1>ПОДБОР ВКОП</h1>', unsafe_allow_html=True)
# z = st.columns(2)
st.sidebar.markdown('<h1>Общая информация</h1>', unsafe_allow_html=True)
st.session_state.filial = st.sidebar.selectbox("Филиал", options=("ВЕЗА-Москва", "ВЕЗА-СПБ"))
st.session_state.object = st.sidebar.text_input("Объект")
st.session_state.orderer = st.sidebar.text_input("Заказчик")
st.session_state.innumber = st.sidebar.text_input("Номер проекта")
st.session_state.fromnum = '.'.join(str(st.sidebar.date_input('от')).split("-")[::-1])
c = st.columns(4)
st.session_state.system = c[0].text_input("Номер системы")
if st.session_state.filial == "ВЕЗА-СПБ":
    st.session_state.manager = st.sidebar.selectbox("Менеджер", options=tuple(map(lambda x: ' '.join(x.split()[:2]),("Барсукова Ксения", "Бельчикова Евгения", "Биктимиров Руслан", "Валеева Разалия", "Василец Алексей",
                                                                                                                    "Волкова Анна","Голованов Павел", "Горшков Дмитрий","Жигадло Полина",
                                                                                                                    "Загуменнов Алексей", "Ильина Анастасия", "Качан Максим", "Квашненков Михаил","Комлева Лилия",  "Кондин Михаил","Кузнецов Сергей", "Ляшенко Владимир","Матвеева Алла",
                                                                                                                    "Микалаускене Валерия","Никифоров Сергей", "Слюсарев Артём","Рогачев Дмитрий", "Ромов Виктор","Терехина Карина","Феоктистов Владислав"))))
    st.session_state.engineer = st.sidebar.selectbox("Выполнил", options=tuple(map(lambda x: ' '.join(x.split()[:2]),("Назаров Шохназар", "Семенов Дмитрий",
                                                                                                                      "Ткаченко Ксения", "Шмелева Валерия", "Каск Андрей", "Пономарев Роман", "Тумасян Николай","Фисун София", "Бороздкина Дарья", "Васильева Елена", "Дружинин Михаил", "Федоренко Анна","Пичулин Александр",
                                                                                                                      "Язынина Анастасия", "Федюкин Андрей", "Александров Вячеслав", "Филиппова Татьяна", "Глухов Евгений", "Матвеев Виталий", "Максимов Егор", "Бунаков Артемий", "Гостев Виталий", "Зайцев Иван", "Сирин Арсений", "Тихопой Игорь", "Еремин Дмитрий"
                                                                                                                     ))))
elif st.session_state.filial == "ВЕЗА-Москва":
    st.session_state.manager = st.sidebar.selectbox("Менеджер", options=tuple(map(lambda x: ' '.join(x.split()[:2]),('Азаров Владислав Евгеньевич','Варданян Тигран Арамович','Петров Михаил Александрович','Бахтеев Павел Юрьевич','Кохно Георгий Андреевич','Калантаров Андрей Викторович','Гаврилов Константин Валерьевич','Гулина Наталья Александровна','Денисов Денис Владимирович','Грибач Павел Александрович','Здейкович Стефан','Мельников Ефим Владимирович','Влазнев Константин Александрович','Моклюк Максим Олегович','Пращук Андрей Юрьевич','Кондратьев Александр Иванович','Муханчиков Иван Михайлович','Гулин Сергей Михайлович','Дутов Александр Васильевич','Життеев Тимур Юрьевич','Бычков Максим Юрьевич','Каспир Евгений Владимирович','Мякиньков Виктор Сергеевич','Тагиров Максим Адимович','Данилов Павел Валерьевич','Мумладзе Александр Мевлудиевич','Омельченко Юрий Анатольевич','Горбунов Максим Максимович', "Цуканов Роман Евгеньевич", "Лоскутов Глеб"))))
    st.session_state.engineer = st.sidebar.selectbox("Выполнил", options=tuple(map(lambda x: ' '.join(x.split()[:2]),('Гарифов Руслан Расилевич','Колесова Вероника Александровна','Мануйлова Анастасия Олеговна','Петрова Татьяна Сергеевна','Иванов Дмитрий Анатольевич','Гришина Регина Эдуардовна','Бубнова Александра Валерьевна','Игнащенко Антон Павлович','Кушхова Наталья Владимировна','Малахов Никита Александрович','Петелин Павел Владимирович','Прохоренко Ольга Сергеевна','Царьков Игорь Владиславович','Бурын Федор Александрович', 'Саломатникова Светлана', 'Сухов Дмитрий Сергеевич'))))
st.session_state.VKOP = c[0].selectbox("Какой ВКОП нужен?", options=("ВКОП 0", "ВКОП 1"))
st.session_state.climate = c[0].selectbox("Климатическое исполнение", options=("У1", "УХЛ1", "Т1"))
st.session_state.Q = c[1].number_input('Расход, м³/ч', step=1)
st.session_state.p = c[1].number_input('Статическое давление, Па', step=1)
w = 270
if st.session_state.VKOP == "ВКОП 0":
    c[-1].image("https://i.postimg.cc/qMQ4vrZD/image.png", width=w, caption='ВКОП 0')
else:
    c[-1].image("https://i.postimg.cc/V6RbR6RQ/image.png", width=w, caption='ВКОП 1')
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
    kluch = item[0]
    # item[2] = ff(df[kluch], list_p, st.session_state.Q)
    qus = [itt for itt in df[kluch] if itt!=None]
    pus = list_p[:len(qus)]
    kpd_Q, kpd_p = list(map(lambda x: int(round(x, 0)), kpd_find(qus, pus, st.session_state.Q, st.session_state.p)))
    item[2] = kpd_p
    item[1] = kpd_Q
    cols[-1].write(f"Статическое давление (расчётное) {kpd_p} Па")
    cols[-1].write(f"Расход (расчётный) {kpd_Q} м³/ч")
    cols[-1].image(image_vkop[st.session_state.VKOP])
    gdf = gaba_vkop[st.session_state.VKOP][item[0]]
    gdf = {key:[str(gdf[key])] for key in gdf.keys()}
    cols[-1].dataframe(gdf)
    if st.session_state.VKOP[-1]=='0':
        st.session_state.pek = cols[-1].selectbox('Переходник крышный', options=(f"ПЕК-ОСА-{item[0].split('-')[0]}-С", "Без переходника"))
        if st.session_state.pek != "Без переходника":
            st.session_state.stam = cols[-1].selectbox('Стакан', options = (f"СТАМ 200-{stam[item[0].split('-')[0]]}-Н", f"СТАМ 401-{stam[item[0].split('-')[0]]}-Н-MV220",f"СТАМ 401-{stam[item[0].split('-')[0]]}-Н-MV220У",f"СТАМ 400-{stam[item[0].split('-')[0]]}-Н",f"СТАМ 405-{stam[item[0].split('-')[0]]}-Н", "Без стакана"))
        if st.session_state.pek == "Без переходника":
            dops = []
        elif st.session_state.stam == "Без стакана":
            dops = ["Дополнительное оборудование", f"Переходник крышный {st.session_state.pek}"]
        else:
            dops = ["Дополнительное оборудование", f"Стакан монтажный {st.session_state.stam}", f"Переходник крышный {st.session_state.pek}"]
    else:
        dops = []
    from temp_fill import doc_fil
    try:
        st.download_button('Скачать лист подбора', data=doc_fil([f"{st.session_state.innumber} от {st.session_state.fromnum}",st.session_state.orderer,st.session_state.object,st.session_state.system,st.session_state.manager,st.session_state.engineer,f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}",st.session_state.Q,st.session_state.p,item[1],item[2],image_vkop[st.session_state.VKOP],st.session_state.plot,gdf,dops], filial=st.session_state.filial), file_name=f"{st.session_state.system}.docx")
        st.download_button("Скачать JSON", data=json_fo({"project_num":st.session_state.innumber, "project_date":st.session_state.fromnum,
 "client": st.session_state.orderer, "object_name": st.session_state.object,
 "system_number":st.session_state.system, "manager":st.session_state.manager, 
 "engineer":st.session_state.engineer, "fan_name": f"{st.session_state.VKOP}-{item[0]}-{st.session_state.climate}", 
 "given_Q":st.session_state.Q, "given_p":st.session_state.p, "real_Q":item[1], "real_p":item[2], "extra":dops
}), file_name=f"{st.session_state.system}.json")
    except Exception as AAA:
        st.write(AAA)
except Exception as er:
    pass
    st.toast(f":red[{er}]")
    # st.write(er)
