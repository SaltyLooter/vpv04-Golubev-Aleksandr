# Localization JSON Auditor

Утилита на Python для проверки файлов локализации в формате JSON: находит пропущенные или лишние ключи, пустые строки и расхождения в плейсхолдерах (`{name}`, `{{count}}`). Также поддерживает загрузку JSON-словарей по HTTP(S)-ссылке через `requests`.

## Структура проекта

- `src/locale_auditor.py` — логика парсинга и аудита файлов локализации;
- `examples/en.json` — эталонный словарь локализации;
- `examples/ru.json` — проверяемый словарь с примерами расхождений;
- `requirements.txt` — зависимости проекта;
- `.gitignore` — исключения для Git (`venv`, `.DS_Store` и др.);
- `README.md` — инструкция по запуску и проверке.

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:
   `git clone https://github.com/SaltyLooter/vpv04-Golubev-Aleksandr.git && cd vpv04-Golubev-Aleksandr`
2. Создайте и активируйте виртуальное окружение:
   `python3 -m venv venv && source venv/bin/activate`
3. Установите зависимости:
   `pip install -r requirements.txt`
4. Запустите проверку локализации:
   `python3 src/locale_auditor.py --base examples/en.json --target examples/ru.json`

## Ожидаемый результат проверки

Скрипт выведет количество ключей, пример первого ключа и найденные замечания: пустой перевод для `actions.delete` и отсутствие плейсхолдера `{count}` в `actions.items_count`.
