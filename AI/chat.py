from AI.init import asistant, manager
import pandas as pd
import datetime as dt


async def new_text_message(user_text):
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_text += f"Дата сообщения: {time}"
    
    response = await asistant.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Определи, хочет ли пользователь добавить трату в базу данных. Если Да — ответь 1, иначе 0."},
            {"role": "user", "content": user_text}
        ]
    )
    
    gpt_text = response.choices[0].message.content
    
    if int(gpt_text):
        user_text = "@@@" + user_text
    manager.add_user_message(user_text)
    response = await asistant.chat.completions.create(
        model="gpt-4o-mini",
        messages=manager.read()
    )
        
    gpt_text = response.choices[0].message.content
    
    
    unsupported_html_tags = [
        "<html>",  # Корневой тег HTML
        "<head>",  # Заголовок документа
        "<title>",  # Заголовок страницы
        "<body>",  # Тело документа
        "<div>",  # Блочный контейнер
        "<span>",  # Строчный контейнер
        "<p>",  # Абзац (хотя текст внутри абзаца будет отображаться, сам тег игнорируется)
        "<h1>", "<h2>", "<h3>", "<h4>", "<h5>", "<h6>",  # Заголовки
        "<a>",  # Ссылки (Telegram использует Markdown для ссылок)
        "<img>",  # Изображения (Telegram требует отдельного метода для отправки изображений)
        "<table>",  # Таблицы
        "<tr>",  # Строка таблицы
        "<td>",  # Ячейка таблицы
        "<th>",  # Заголовок таблицы
        "<ul>",  # Ненумерованный список
        "<ol>",  # Нумерованный список
        "<li>",  # Элемент списка
        "<form>",  # Форма
        "<input>",  # Поле ввода
        "<button>",  # Кнопка
        "<textarea>",  # Многострочное поле ввода
        "<select>",  # Выпадающий список
        "<option>",  # Элемент выпадающего списка
        "<iframe>",  # Встроенный фрейм
        "<script>",  # Скрипты
        "<style>",  # Стили
        "<meta>",  # Мета-теги
        "<link>",  # Ссылки на внешние ресурсы
        "<nav>",  # Навигация
        "<header>",  # Шапка
        "<footer>",  # Подвал
        "<section>",  # Секция
        "<article>",  # Статья
        "<aside>",  # Боковая панель
        "<main>",  # Основное содержимое
        "<figure>",  # Изображение с подписью
        "<figcaption>",  # Подпись к изображению
        "<canvas>",  # Холст для рисования
        "<svg>",  # Векторная графика
        "<video>",  # Видео
        "<audio>",  # Аудио
        "<source>",  # Источник мультимедиа
        "<track>",  # Треки для мультимедиа
        "<embed>",  # Встраиваемый контент
        "<object>",  # Встраиваемый объект
        "<param>",  # Параметры для встраиваемого объекта
        "<map>",  # Карта изображений
        "<area>",  # Область карты изображений
        "<base>",  # Базовый URL
        "<dialog>",  # Диалоговое окно
        "<details>",  # Детали
        "<summary>",  # Сводка деталей
        "<menu>",  # Меню
        "<menuitem>",  # Элемент меню
        "<meter>",  # Индикатор
        "<progress>",  # Прогресс
        "<rp>",  # Резервный текст для ruby
        "<rt>",  # Аннотация ruby
        "<ruby>",  # Ruby-аннотация
        "<bdi>",  # Изоляция текста
        "<bdo>",  # Направление текста
        "<wbr>",  # Возможный перенос строки
        "<picture>",  # Изображение с адаптивным выбором
        "<template>",  # Шаблон
        "<slot>",  # Слот
        "<shadow>",  # Тень (устаревший)
        "<content>",  # Контент (устаревший)
        "<element>",  # Элемент (устаревший)
        "<isindex>",  # Индекс (устаревший)
        "<applet>",  # Апплет (устаревший)
        "<acronym>",  # Акроним (устаревший)
        "<bgsound>",  # Фоновый звук (устаревший)
        "<dir>",  # Список директорий (устаревший)
        "<frame>",  # Фрейм (устаревший)
        "<frameset>",  # Набор фреймов (устаревший)
        "<noframes>",  # Альтернатива фреймам (устаревший)
        "<plaintext>",  # Простой текст (устаревший)
        "<strike>",  # Зачёркнутый текст (устаревший)
        "<xmp>",  # Пример текста (устаревший)
        "<br>",
        "<pre>",
        "<code>"
    ]
    
    for tag in unsupported_html_tags:
        gpt_text = gpt_text.replace(tag, '')
    
    # Добавляем ответ ассистента в менеджер
    manager.add_assistant_message(gpt_text)
    
    # Возвращаем текст ответа
    return gpt_text

async def may_be_u_want_table(user_text):
    if "таблиц" in user_text.lower():
        return 1
    return 0

async def new_table(user_text):
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_text += f"Дата сообщения: {time}"
    manager.add_user_message(user_text)
    response = await asistant.chat.completions.create(
        model="gpt-4o-mini",
        messages=manager.read()
    )
    
    gpt_text = response.choices[0].message.content
    
    gpt_text = gpt_text.replace('`', '')
    
    with open("bot/files/table.csv", "w", encoding="utf-8") as f:
        f.write(gpt_text)
    
    df = pd.read_csv("bot/files/table.csv", encoding='utf-8', delimiter=';')
    df.to_excel("bot/files/table.xlsx", index=False)
    
async def new_photo_message(text):
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = "@@@" + text + "Отправляю тебе информацию с чека. Необходимо найти здесь мою трату и обработать её как обычно. Дата сообщения: " + time
    manager.add_user_message(text)
    response = await asistant.chat.completions.create(
        model="gpt-4o-mini",
        messages=manager.read()
    )
    
    gpt_text = response.choices[0].message.content
    
    unsupported_html_tags = [
        "<html>",  # Корневой тег HTML
        "<head>",  # Заголовок документа
        "<title>",  # Заголовок страницы
        "<body>",  # Тело документа
        "<div>",  # Блочный контейнер
        "<span>",  # Строчный контейнер
        "<p>",  # Абзац (хотя текст внутри абзаца будет отображаться, сам тег игнорируется)
        "<h1>", "<h2>", "<h3>", "<h4>", "<h5>", "<h6>",  # Заголовки
        "<a>",  # Ссылки (Telegram использует Markdown для ссылок)
        "<img>",  # Изображения (Telegram требует отдельного метода для отправки изображений)
        "<table>",  # Таблицы
        "<tr>",  # Строка таблицы
        "<td>",  # Ячейка таблицы
        "<th>",  # Заголовок таблицы
        "<ul>",  # Ненумерованный список
        "<ol>",  # Нумерованный список
        "<li>",  # Элемент списка
        "<form>",  # Форма
        "<input>",  # Поле ввода
        "<button>",  # Кнопка
        "<textarea>",  # Многострочное поле ввода
        "<select>",  # Выпадающий список
        "<option>",  # Элемент выпадающего списка
        "<iframe>",  # Встроенный фрейм
        "<script>",  # Скрипты
        "<style>",  # Стили
        "<meta>",  # Мета-теги
        "<link>",  # Ссылки на внешние ресурсы
        "<nav>",  # Навигация
        "<header>",  # Шапка
        "<footer>",  # Подвал
        "<section>",  # Секция
        "<article>",  # Статья
        "<aside>",  # Боковая панель
        "<main>",  # Основное содержимое
        "<figure>",  # Изображение с подписью
        "<figcaption>",  # Подпись к изображению
        "<canvas>",  # Холст для рисования
        "<svg>",  # Векторная графика
        "<video>",  # Видео
        "<audio>",  # Аудио
        "<source>",  # Источник мультимедиа
        "<track>",  # Треки для мультимедиа
        "<embed>",  # Встраиваемый контент
        "<object>",  # Встраиваемый объект
        "<param>",  # Параметры для встраиваемого объекта
        "<map>",  # Карта изображений
        "<area>",  # Область карты изображений
        "<base>",  # Базовый URL
        "<dialog>",  # Диалоговое окно
        "<details>",  # Детали
        "<summary>",  # Сводка деталей
        "<menu>",  # Меню
        "<menuitem>",  # Элемент меню
        "<meter>",  # Индикатор
        "<progress>",  # Прогресс
        "<rp>",  # Резервный текст для ruby
        "<rt>",  # Аннотация ruby
        "<ruby>",  # Ruby-аннотация
        "<bdi>",  # Изоляция текста
        "<bdo>",  # Направление текста
        "<wbr>",  # Возможный перенос строки
        "<picture>",  # Изображение с адаптивным выбором
        "<template>",  # Шаблон
        "<slot>",  # Слот
        "<shadow>",  # Тень (устаревший)
        "<content>",  # Контент (устаревший)
        "<element>",  # Элемент (устаревший)
        "<isindex>",  # Индекс (устаревший)
        "<applet>",  # Апплет (устаревший)
        "<acronym>",  # Акроним (устаревший)
        "<bgsound>",  # Фоновый звук (устаревший)
        "<dir>",  # Список директорий (устаревший)
        "<frame>",  # Фрейм (устаревший)
        "<frameset>",  # Набор фреймов (устаревший)
        "<noframes>",  # Альтернатива фреймам (устаревший)
        "<plaintext>",  # Простой текст (устаревший)
        "<strike>",  # Зачёркнутый текст (устаревший)
        "<xmp>",  # Пример текста (устаревший)
        "<br>",
        "<pre>",
        "<code>"
    ]
    
    for tag in unsupported_html_tags:
        gpt_text = gpt_text.replace(tag, '')
    
    # Добавляем ответ ассистента в менеджер
    manager.add_assistant_message(gpt_text)
    
    # Возвращаем текст ответа
    return gpt_text