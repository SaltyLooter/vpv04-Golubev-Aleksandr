# Localization JSON Auditor

## 1) Что это
Утилита на Python для проверки файлов локализации в формате JSON: находит пропущенные и лишние ключи, пустые строки и расхождения в плейсхолдерах (`{name}`, `{{count}}`). Также поддерживает загрузку JSON-словарей по HTTP(S)-ссылке через `requests`.

## 2) Как запустить

### macOS / Linux
1. Клонируйте репозиторий и перейдите в папку проекта:
   `git clone [https://github.com/SaltyLooter/vpv04-Golubev-Aleksandr.git](https://github.com/SaltyLooter/vpv04-Golubev-Aleksandr.git) && cd vpv04-Golubev-Aleksandr`
2. Создайте и активируйте виртуальное окружение:
   `python3 -m venv venv && source venv/bin/activate`
3. Установите зависимости:
   `pip install -r requirements.txt`
4. Запустите проверку локализации:
   `python3 src/locale_auditor.py --base examples/en.json --target examples/ru.json`

### Windows (PowerShell / CMD)
1. Клонируйте репозиторий и перейдите в папку проекта:
   `git clone [https://github.com/SaltyLooter/vpv04-Golubev-Aleksandr.git](https://github.com/SaltyLooter/vpv04-Golubev-Aleksandr.git)` и `cd vpv04-Golubev-Aleksandr`
2. Создайте и активируйте виртуальное окружение:
   `python -m venv venv` и затем `.\venv\Scripts\Activate.ps1` (в PowerShell) или `venv\Scripts\activate.bat` (в CMD)
3. Установите зависимости:
   `pip install -r requirements.txt`
4. Запустите проверку локализации:
   `python src\locale_auditor.py --base examples\en.json --target examples\ru.json`

## 3) Как проверить, что работает

Запустите команду:
`python3 src/locale_auditor.py --base examples/en.json --target examples/ru.json`

Ожидаемый результат: скрипт покажет количество ключей, пример первого ключа (`'Task Tracker'`), пустой перевод `actions.delete` и расхождение в плейсхолдере `{count}` для `actions.items_count`.

## 4) Что я сделал(а) в этом уроке
- Настроил виртуальное окружение `venv`, установил `requests` и разобрался с запуском Python-скриптов на macOS.
- Написал парсер и аудитор локализации в `src/locale_auditor.py` и подготовил тестовые JSON-словари в `examples/`.
- Инициализировал Git-репозиторий, добавил `.gitignore` и `requirements.txt`, чтобы исключить `venv/` и лишние файлы.
- Зафиксировал изменения коммитами и отправил репозиторий на GitHub.

## 5) Что было сложным / что понял(а)
Все было понятно.
