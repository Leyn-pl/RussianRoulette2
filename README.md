# Russian Roulette 2
Игру создал LEYN :)

![Экран победы](https://media.discordapp.net/attachments/1353438795869196358/1358503826780324061/2F353360-8853-40BE-85A1-977F82630FFC.png?ex=67f414c8&is=67f2c348&hm=a4d9a95c4aac5ce6c1a0a69ce83c64a31543bd2caedb5a3c02dcbc3f3d53b2fc&=&format=webp&quality=lossless&width=1573&height=800 "Экран победы в 50 ходов")

Вы играете в русскую рулетку с привидением. Каждый ход вы можете выстрелить в противника или в себя, а привидение повторит ваше действие. В начале хода вы бросаете два кубика. Кубики - способ получить предметы и подсматривать в револьвер. Если вы используете предмет, привидение восстановит здоровье.

В отличае от Buckshot Roulette, здесь вы напрямую влияете на револьвер. Вы можете заряжать патроны, а также каждый выстрел урон револьвера увеличивается на 1. Здоровье привидения - 60, игрока - 30. Нужно переиграть бота с помощью своего мозга и кубиков.

Всё происходящее описано в окне текста. Если будут какие-то вопросы, напиште мне в дискорде или телеграме: **leyn1092**

# [>>> СКАЧАТЬ <<<](https://github.com/Leyn-pl/RussianRoulette2/archive/refs/heads/main.zip)
###### ^^^ кто впервые видит гитхаб

## Что нужно для работы:
- [Python 3.12+](https://www.python.org/downloads/)
  - Выбираете версию, листаете вниз до Files, а дальше разберётесь
- (библиотека) [rusrul_lib](https://pypi.org/project/rusrul-lib/)
  - `pip install rusrul-lib` < в командной строке
- (библиотека) [colored](https://pypi.org/project/colored/)
  - `pip install colored` < в командной строке

## Как запустить
1. Скачайте и **распакуйте архив**
2. Запустите `main.py` или `run.bat`

## Возможные проблемы и способы решения
- Не получается скачать библиотеки:
  - Проверьте интернет
  - Заного откройте установщик, выберите "Modify" и включите "**pip**"
  - Скачайте и запустите [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
- Не работает `run.bat`:
  - Запустите `main.py` напрямую
  - Заного откройте установщик, выберите "Modify" и включите "**Add Python to PATH**" / "**Add Python to environmental variables**"
- Не видно часть игры, элементы игры обрезаны, остаётся видна часть прошлого кадра, много пространства справа:
  - Вручную измените размер окна консоли, чтобы всё ровно влезало
  - Откройте настройки консоли и поставьте размер 120x30
    - 11 винда: **ctrl+,** или стрелка вниз рядом с плюсом, "Размер для запуска", сделайте 120х30
    - 10 винда: ПКМ по верхней панели, "Свойства", "Расположение", пункт "Размер окна", сделайте 120х30
- Другая проблема:
  - Напишите мне в дискорде или телеграме: **leyn1092**
