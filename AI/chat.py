from AI.init import asistant, manager
import datetime as dt
import json
import os
from dotenv import load_dotenv
import sqlite3
import csv
import xlsxwriter



load_dotenv()


async def new_text_message(user_text):
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_text += f"Дата сообщения: {time}"

    manager.add_user_message(user_text)
    response = await asistant.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=manager.read(),
        max_tokens=1000
    )

    gpt_text = response.choices[0].message.content

    unsupported_html_tags = [
        "<html>", "</html>",  # Корневой тег HTML
        "<head>", "</head>",  # Заголовок документа
        "<title>", "</title>",  # Заголовок страницы
        "<body>", "</body>",  # Тело документа
        "<div>", "</div>",  # Блочный контейнер
        "<span>", "</span>",  # Строчный контейнер
        "<p>", "</p>",  # Абзац
        "<h1>", "</h1>", "<h2>", "</h2>", "<h3>", "</h3>", "<h4>", "</h4>", "<h5>", "</h5>", "<h6>", "</h6>",  # Заголовки
        "<a>", "</a>",  # Ссылки
        "<img>", "</img>",  # Изображения
        "<table>", "</table>",  # Таблицы
        "<tr>", "</tr>",  # Строка таблицы
        "<td>", "</td>",  # Ячейка таблицы
        "<th>", "</th>",  # Заголовок таблицы
        "<ul>", "</ul>",  # Ненумерованный список
        "<ol>", "</ol>",  # Нумерованный список
        "<li>", "</li>",  # Элемент списка
        "<form>", "</form>",  # Форма
        "<input>", "</input>",  # Поле ввода
        "<button>", "</button>",  # Кнопка
        "<textarea>", "</textarea>",  # Многострочное поле ввода
        "<select>", "</select>",  # Выпадающий список
        "<option>", "</option>",  # Элемент выпадающего списка
        "<iframe>", "</iframe>",  # Встроенный фрейм
        "<script>", "</script>",  # Скрипты
        "<style>", "</style>",  # Стили
        "<meta>", "</meta>",  # Мета-теги
        "<link>", "</link>",  # Ссылки на внешние ресурсы
        "<nav>", "</nav>",  # Навигация
        "<header>", "</header>",  # Шапка
        "<footer>", "</footer>",  # Подвал
        "<section>", "</section>",  # Секция
        "<article>", "</article>",  # Статья
        "<aside>", "</aside>",  # Боковая панель
        "<main>", "</main>",  # Основное содержимое
        "<figure>", "</figure>",  # Изображение с подписью
        "<figcaption>", "</figcaption>",  # Подпись к изображению
        "<canvas>", "</canvas>",  # Холст для рисования
        "<svg>", "</svg>",  # Векторная графика
        "<video>", "</video>",  # Видео
        "<audio>", "</audio>",  # Аудио
        "<source>", "</source>",  # Источник мультимедиа
        "<track>", "</track>",  # Треки для мультимедиа
        "<embed>", "</embed>",  # Встраиваемый контент
        "<object>", "</object>",  # Встраиваемый объект
        "<param>", "</param>",  # Параметры для встраиваемого объекта
        "<map>", "</map>",  # Карта изображений
        "<area>", "</area>",  # Область карты изображений
        "<base>", "</base>",  # Базовый URL
        "<dialog>", "</dialog>",  # Диалоговое окно
        "<details>", "</details>",  # Детали
        "<summary>", "</summary>",  # Сводка деталей
        "<menu>", "</menu>",  # Меню
        "<menuitem>", "</menuitem>",  # Элемент меню
        "<meter>", "</meter>",  # Индикатор
        "<progress>", "</progress>",  # Прогресс
        "<rp>", "</rp>",  # Резервный текст для ruby
        "<rt>", "</rt>",  # Аннотация ruby
        "<ruby>", "</ruby>",  # Ruby-аннотация
        "<bdi>", "</bdi>",  # Изоляция текста
        "<bdo>", "</bdo>",  # Направление текста
        "<wbr>", "</wbr>",  # Возможный перенос строки
        "<picture>", "</picture>",  # Изображение с адаптивным выбором
        "<template>", "</template>",  # Шаблон
        "<slot>", "</slot>",  # Слот
        "<shadow>", "</shadow>",  # Тень (устаревший)
        "<content>", "</content>",  # Контент (устаревший)
        "<element>", "</element>",  # Элемент (устаревший)
        "<isindex>", "</isindex>",  # Индекс (устаревший)
        "<applet>", "</applet>",  # Апплет (устаревший)
        "<acronym>", "</acronym>",  # Акроним (устаревший)
        "<bgsound>", "</bgsound>",  # Фоновый звук (устаревший)
        "<dir>", "</dir>",  # Список директорий (устаревший)
        "<frame>", "</frame>",  # Фрейм (устаревший)
        "<frameset>", "</frameset>",  # Набор фреймов (устаревший)
        "<noframes>", "</noframes>",  # Альтернатива фреймам (устаревший)
        "<plaintext>", "</plaintext>",  # Простой текст (устаревший)
        "<strike>", "</strike>",  # Зачёркнутый текст (устаревший)
        "<xmp>", "</xmp>",  # Пример текста (устаревший)
        "<br>", "</br>",  # Перенос строки
        "<pre>", "</pre>",  # Преформатированный текст
        "<code>", "</code>",  # Код
        "*",  # Звездочка (не HTML-тег, но добавлена в список)
        "<u>", "</u>",  # Подчеркнутый текст
    ]

    for tag in unsupported_html_tags:
        gpt_text = gpt_text.replace(tag, '')

    # Добавляем ответ ассистента в менеджер
    if "[" in gpt_text:
        for z in "`python":
            gpt_text = gpt_text.replace(z, '')
        array = [int(c) for c in gpt_text[1:-1].split(", ")]
        print(array)
        gpt_text = f"По моим подсчетам у меня получилось {sum(array)}"

    manager.add_assistant_message(gpt_text)
    return gpt_text


async def create_db():
    manager.add_user_message("Создай SQL код для добавления всех данных из твоей памяти (бери только актуальную информацию) в таблицу Finance, поля в таблице: NAME(STRING), CATEGORY(STRING), SUB_CATEGORY(STRING), PRICE(INT). Напиши только SQL запрос, ничего лишнего")
    response = await asistant.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=manager.read(),
        max_tokens=1000
    )

    gpt_text = response.choices[0].message.content
    
    for z in "`sql":
        gpt_text = gpt_text.replace(z, '')
    gpt_text = gpt_text.replace('\n', ' ')
    
    manager.add_assistant_message(gpt_text)
    
    db = sqlite3.connect("db/database.db")
    cur = db.cursor()
    cur.execute("DELETE FROM Finance")
    db.commit()
    cur.execute(gpt_text)
    db.commit()


async def new_photo_message(text):
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text += "Отправляю тебе информацию с чека. Необходимо найти здесь мою трату и обработать её как обычно. Дата сообщения: " + time
    manager.add_user_message(text)
    response = await asistant.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=manager.read(),
    )

    gpt_text = response.choices[0].message.content

    unsupported_html_tags = [
        "<html>", "</html>",  # Корневой тег HTML
        "<head>", "</head>",  # Заголовок документа
        "<title>", "</title>",  # Заголовок страницы
        "<body>", "</body>",  # Тело документа
        "<div>", "</div>",  # Блочный контейнер
        "<span>", "</span>",  # Строчный контейнер
        "<p>", "</p>",  # Абзац
        "<h1>", "</h1>", "<h2>", "</h2>", "<h3>", "</h3>", "<h4>", "</h4>", "<h5>", "</h5>", "<h6>", "</h6>",  # Заголовки
        "<a>", "</a>",  # Ссылки
        "<img>", "</img>",  # Изображения
        "<table>", "</table>",  # Таблицы
        "<tr>", "</tr>",  # Строка таблицы
        "<td>", "</td>",  # Ячейка таблицы
        "<th>", "</th>",  # Заголовок таблицы
        "<ul>", "</ul>",  # Ненумерованный список
        "<ol>", "</ol>",  # Нумерованный список
        "<li>", "</li>",  # Элемент списка
        "<form>", "</form>",  # Форма
        "<input>", "</input>",  # Поле ввода
        "<button>", "</button>",  # Кнопка
        "<textarea>", "</textarea>",  # Многострочное поле ввода
        "<select>", "</select>",  # Выпадающий список
        "<option>", "</option>",  # Элемент выпадающего списка
        "<iframe>", "</iframe>",  # Встроенный фрейм
        "<script>", "</script>",  # Скрипты
        "<style>", "</style>",  # Стили
        "<meta>", "</meta>",  # Мета-теги
        "<link>", "</link>",  # Ссылки на внешние ресурсы
        "<nav>", "</nav>",  # Навигация
        "<header>", "</header>",  # Шапка
        "<footer>", "</footer>",  # Подвал
        "<section>", "</section>",  # Секция
        "<article>", "</article>",  # Статья
        "<aside>", "</aside>",  # Боковая панель
        "<main>", "</main>",  # Основное содержимое
        "<figure>", "</figure>",  # Изображение с подписью
        "<figcaption>", "</figcaption>",  # Подпись к изображению
        "<canvas>", "</canvas>",  # Холст для рисования
        "<svg>", "</svg>",  # Векторная графика
        "<video>", "</video>",  # Видео
        "<audio>", "</audio>",  # Аудио
        "<source>", "</source>",  # Источник мультимедиа
        "<track>", "</track>",  # Треки для мультимедиа
        "<embed>", "</embed>",  # Встраиваемый контент
        "<object>", "</object>",  # Встраиваемый объект
        "<param>", "</param>",  # Параметры для встраиваемого объекта
        "<map>", "</map>",  # Карта изображений
        "<area>", "</area>",  # Область карты изображений
        "<base>", "</base>",  # Базовый URL
        "<dialog>", "</dialog>",  # Диалоговое окно
        "<details>", "</details>",  # Детали
        "<summary>", "</summary>",  # Сводка деталей
        "<menu>", "</menu>",  # Меню
        "<menuitem>", "</menuitem>",  # Элемент меню
        "<meter>", "</meter>",  # Индикатор
        "<progress>", "</progress>",  # Прогресс
        "<rp>", "</rp>",  # Резервный текст для ruby
        "<rt>", "</rt>",  # Аннотация ruby
        "<ruby>", "</ruby>",  # Ruby-аннотация
        "<bdi>", "</bdi>",  # Изоляция текста
        "<bdo>", "</bdo>",  # Направление текста
        "<wbr>", "</wbr>",  # Возможный перенос строки
        "<picture>", "</picture>",  # Изображение с адаптивным выбором
        "<template>", "</template>",  # Шаблон
        "<slot>", "</slot>",  # Слот
        "<shadow>", "</shadow>",  # Тень (устаревший)
        "<content>", "</content>",  # Контент (устаревший)
        "<element>", "</element>",  # Элемент (устаревший)
        "<isindex>", "</isindex>",  # Индекс (устаревший)
        "<applet>", "</applet>",  # Апплет (устаревший)
        "<acronym>", "</acronym>",  # Акроним (устаревший)
        "<bgsound>", "</bgsound>",  # Фоновый звук (устаревший)
        "<dir>", "</dir>",  # Список директорий (устаревший)
        "<frame>", "</frame>",  # Фрейм (устаревший)
        "<frameset>", "</frameset>",  # Набор фреймов (устаревший)
        "<noframes>", "</noframes>",  # Альтернатива фреймам (устаревший)
        "<plaintext>", "</plaintext>",  # Простой текст (устаревший)
        "<strike>", "</strike>",  # Зачёркнутый текст (устаревший)
        "<xmp>", "</xmp>",  # Пример текста (устаревший)
        "<br>", "</br>",  # Перенос строки
        "<pre>", "</pre>",  # Преформатированный текст
        "<code>", "</code>",  # Код
        "*",  # Звездочка (не HTML-тег, но добавлена в список)
        "<u>", "</u>",  # Подчеркнутый текст
    ]

    for tag in unsupported_html_tags:
        gpt_text = gpt_text.replace(tag, '')

    # Добавляем ответ ассистента в менеджер
    manager.add_assistant_message(gpt_text)

    # Возвращаем текст ответа
    return gpt_text


async def category_check():

    response = await asistant.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": f"Вот данные: {manager.read()}. Предоставь мне все категории и подкатегории в виде словаря типа Категория: список подкатегорий. Пришли только словарь."},
        ],
    )

    gpt_text = response.choices[0].message.content

    data = json.loads(gpt_text.replace('`', '').replace('python', ''))

    print(data)

    if len(data.keys()) > 7:
        manager.add_assistant_message(
            "ВНИМАНИЕ! Количество ваших категорий превышает 7!")
        return "ВНИМАНИЕ! Количество ваших категорий превышает 7!"

    for key, value in data.items():
        if len(data[key]) > 7:
            manager.add_assistant_message(
                f"ВНИМАНИЕ! Количество ваших подкатегорий в категории {key} превышает 7!")
            return f"ВНИМАНИЕ! Количество ваших подкатегорий в категории {key} превышает 7!"


async def new_table(user_text):
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_text = "СОЗДАЙ ТАБЛИЦУ. Если ты не понимаешь, какую таблицу хочет Владислав, посмотри его последние сообщения в памяти. Таблицы должны быть в формате CSV с разделителем ;. Заголовки: Название, Категория, Подкатегория, Стоимость, Дата. Владислав может добавлять столбцы. Никакого форматирования или HTML-тегов в таблицах! Запрос пользователя: " + user_text + "Дата сообщения: " + time
    manager.add_user_message(user_text)
    response = await asistant.chat.completions.create(
        model="gpt-4o-mini",
        messages=manager.read()
    )
    
    gpt_text = response.choices[0].message.content
    
    gpt_text = gpt_text.replace('`', '')
    
    with open("bot/files/table.csv", "w", encoding="utf-8") as f:
        f.write(gpt_text)
    
    workbook = xlsxwriter.Workbook("bot/files/table.xlsx")
    worksheet = workbook.add_worksheet()

    with open("bot/files/table.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row_index, row in enumerate(reader):
            for col_index, value in enumerate(row):
                worksheet.write(row_index, col_index, value)

    workbook.close()