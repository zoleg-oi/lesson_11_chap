import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import time


class pars_img:
    '''
    Данный класс реализует соединение с сайтом bestmats.ru парсинг и загрузку изображений,
    а так же модификацию изображений по размеру и формату (формат png, размер 400х400 px).
    Изображения загружаются в отдельную папку с названием  - IMG, где производятся требуемые преобразования.
    Создается диаграмма использования видов товаров по моделям автомобилей
    атрибуты:
    file
        наименование файла списка загружаемых изображений, полученных с сайта в результате парсинга
    Методы:
    __init__
        получает параметр с URL адресом страницы
    get_url
        осуществляет подключение к сайту по полученному адресу и составляет список изображений,
        которые находятся по данному адресу, список сохраняется в файл spisok.csv
    save_image
        создает папку IMG, если ее нет, и сохраняет изображения в соответствии с полученным списком.
    diagram
        создает диаграмму в соответствии со списком, в котором хранятся количество видов
        товаров по маркам автомобилей
    modifi_img
        модифицирует изображения в соответствии с заданием в формат - png и размер 400x400 px
    vis_file
        преобразует список полученный парсером с сайта - spisok.csv
        в следующие списки:
        spisok_img.csv  - данный файл содержит список изображений, полученный путем
            устранения дубликатов строк, используется при модификации изображений
        count_model.csv - данный файл содержит список количества видов по моделям автомобилей.
            Файл получен путем подсчета количества вхождений видов товара по маркам автомобилей, используется при
            построении диаграммы.
        spisok.xlsx
            в соответствии с заданием список конвертируется в таблицу Excel.

    Для осуществления данной задачи использовались подключаемые библиотеки
    requests
        с помощью данной библиотеки осуществляется подключение к сайтам, производится загрузка информации.
    BeautifulSoup
        с помощью данной библиотеки осуществляется форматирование и фильтрация поступившей информации с сайта.
    pandas
        с помощью данной библиотеки осуществлялась обработка форматированных данных записанных в файлах.
        данные загружались в Dataframe где над ними осуществлялись манипуляции, требуемые для выполнения задания.
    matplotlib
        c помощью данной библиотеки осуществлялся вывод и форматирование диаграммы в соответствии с полученными данными
    numpy
        данная библиотека использовалась для создания массивов данных и форматирования этих данных, для последующего
        формирования диаграммы.
    pillaw
        при помощи данной библиотеки осуществлялось форматирование изображений.

    '''
    file = 'spisok.csv'

    def __init__(self, pars_url):
        self.pu = pars_url

    def get_url(self):
        p = requests.get(self.pu)
        # Принимаем поток данных и форматируем его в удобную форму
        # забираем все что находится под тэгом img
        s = BeautifulSoup(p.text, 'html.parser')
        list_img = s.findAll('img')
        f = open(self.file, 'w+', encoding='UTF8')
        name = 'Марка'
        link = 'Ссылка'
        f.write(f'{name};{link}\n')
        for p in list_img:
            pp = str(p).split(" ")
            name = ''
            link = ''

            for i in pp:
                # из полученных данных вырезаем неподходящие строки по условиям
                if "alt=" in i:
                    if (i != 'alt="Крепежные' and i != 'alt="Универсальные'
                            and i != 'alt="Яндекс.Метрика"'
                            and i != 'alt=""'
                            and i != 'alt="Автоковры"'):
                        name = i[5:len(i) - 1]
                elif "src=" in i:
                    link = i[5:len(i) - 1]
                if len(link) > 0 and len(name) > 0:
                    f.write(f'{name};{link}\n')
        f.close()

    def save_image(self):
        # Проверяем наличие файла и папки
        if os.path.exists('spisok_img.csv'):
            file = 'spisok_img.csv'
        else:
            file = self.file
        if not os.path.exists('IMG'):
            os.makedirs('IMG')
        # в соответствии с имеющимся списком получаем и сохраняем изображения
        with open(file, encoding='UTF8') as f:
            os.chdir('IMG')
            for line in f:
                link = line[line.find(';') + 1:len(line) - 1]
                if line.rfind('/') >= 0:
                    img_name = line[line.rfind('/') + 1:len(line) - 1]
                else:
                    continue
                img = requests.get(link)  # получаем изображение с сайта
                with open(img_name, 'wb') as file:
                    file.write(img.content)  # сохраняем изображение
                    print(f'Записываем изображение {img_name}')

    def diagram(self):
        list_model = []
        list_count = []
        os.chdir('..')

        if os.path.exists('count_model.csv'):
            # Открываем файл и заполняем списки для формирования диаграммы
            # расзбираем строки по спискам
            with open('count_model.csv', encoding='UTF8') as f:
                for line in f:
                    lm = line[0: line.find(';')]
                    lc = line[line.find(';') + 1:len(line) - 1]
                    list_count.append(lc)
                    list_model.append(lm)
            # удаляем заголовки
            list_count.pop(0)
            list_model.pop(0)
            list_count = list(map(int, list_count))  # преобразовываем список в тип int
            # форматируем диаграмму и сортируем списки, предварительно
            # помести списки в массив данных
            plt.figure(1, figsize=(18, 10), dpi=80)
            x = np.array(list_model)
            y = np.array(list_count)
            st = y.argsort()
            plt.xticks(rotation=90)
            plt.yticks(np.arange(min(y), max(y) + 1, 1.0))
            plt.xlabel('Модели автомобилей')
            plt.ylabel('Количество')
            plt.title('Количество видов по моделям')
            plt.grid(True)
            plt.bar(x[st], y[st], label='Количество в модельном ряде')
            plt.show()  # вывести конечную диаграмму
        else:
            print('Файл count_model.csv не найден')
            return

    def vis_file(self):
        # Загружаем в dataframe данные, полученные с сайта и сохраненные в файл csv
        df = pd.read_csv(self.file, sep=';')
        df.to_excel("spisok.xlsx", index=False)  # конвертируем и сохраняем в формате Excel
        print(df.head(5))  # Выводим первые пять строк для понимания того, что все работает
        print()
        # подсчитываем  количество вхождений по маркам автомобилей и сохраняем результат в отдельный файл
        count_m = df['Марка'].value_counts()
        count_m.to_csv('count_model.csv', sep=';')
        img_str = df.drop_duplicates()  # удаляем  дубликаты строк и выводим в отдельный файл
        img_str.to_csv('spisok_img.csv', sep=';', index=False)

    def modifi_img(self):
        if os.path.exists('spisok_img.csv'):
            file = 'spisok_img.csv'
        else:
            file = self.file
        with open(file, encoding='UTF8') as f:
            os.chdir('IMG')
            for line in f:
                img_name = line[line.rfind('/') + 1:len(line) - 1]
                if os.path.exists(img_name):
                    image = Image.open(img_name)
                    img_resiz = image.resize((400, 400))  # изменяем размер файла изображения
                    img_name = img_name[:img_name.find('.')].replace('300x300', '400x400')  # меняем имя файла
                    img_resiz.save(img_name + '.png', 'png')  # сохраняем и конвертируем в формат png
            print('Преобразование изображений выполнено')


sr = pars_img('http://bestmats.ru/shop/')
pand = sr.vis_file()
im = sr.save_image()
diag = sr.diagram()
imm = sr.modifi_img()
