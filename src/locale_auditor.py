cat << 'EOF' > src/locale_auditor.py
import argparse
import json
import re
from pathlib import Path
import requests


PLACEHOLDER_RE = re.compile(r"\{[a-zA-Z0-9_]+\}|\{\{[a-zA-Z0-9_]+\}\}")


def flatten_dict(data: dict, prefix: str = "") -> dict[str, str]:
    """Превращает вложенный словарь локализации в плоский вид: 'app.title' -> 'Title'."""
    items: dict[str, str] = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            items.update(flatten_dict(value, full_key))
        else:
            items[full_key] = "" if value is None else str(value)
    return items


def load_locale_source(source: str) -> tuple[str, dict]:
    """Загружает JSON-словарь из локального файла или по HTTP(S)-ссылке."""
    if source.startswith(("http://", "https://")):
        response = requests.get(source, timeout=10)
        response.raise_for_status()
        return f"HTTP {response.status_code}", response.json()

    path = Path(source)
    content = json.loads(path.read_text(encoding="utf-8"))
    return "LOCAL FILE", content


def extract_placeholders(text: str) -> set[str]:
    """Извлекает плейсхолдеры вида {username} или {{count}}."""
    return set(PLACEHOLDER_RE.findall(text))


def audit_locales(base_map: dict[str, str], target_map: dict[str, str]) -> dict:
    """Находит пропущенные и лишние ключи, пустые значения и расхождения в плейсхолдерах."""
    missing_keys = sorted(set(base_map.keys()) - set(target_map.keys()))
    extra_keys = sorted(set(target_map.keys()) - set(base_map.keys()))
    empty_keys = sorted(k for k, v in target_map.items() if not v.strip())

    placeholder_mismatches: list[str] = []
    for key in sorted(set(base_map.keys()) & set(target_map.keys())):
        base_ph = extract_placeholders(base_map[key])
        target_ph = extract_placeholders(target_map[key])
        if base_ph != target_ph:
            placeholder_mismatches.append(
                f"{key}: ожидалось {sorted(base_ph) or '[]'}, найдено {sorted(target_ph) or '[]'}"
            )

    return {
        "missing_keys": missing_keys,
        "extra_keys": extra_keys,
        "empty_keys": empty_keys,
        "placeholder_mismatches": placeholder_mismatches,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Парсер и аудитор JSON-файлов локализации")
    parser.add_argument(
        "--base",
        default="examples/en.json",
        help="Эталонный файл локализации или URL",
    )
    parser.add_argument(
        "--target",
        default="examples/ru.json",
        help="Проверяемый файл локализации или URL",
    )
    args = parser.parse_args()

    try:
        base_status, base_raw = load_locale_source(args.base)
        target_status, target_raw = load_locale_source(args.target)

        base_flat = flatten_dict(base_raw)
        target_flat = flatten_dict(target_raw)
        report = audit_locales(base_flat, target_flat)

        print(f"Эталон: {base_status} | Ключей: {len(base_flat)}")
        print(f"Перевод: {target_status} | Ключей: {len(target_flat)}")
        if base_flat:
            first_key = next(iter(base_flat))
            print(f"Первый ключ ({first_key}): {base_flat[first_key]!r}")

        print(f"Пропущено ключей: {len(report['missing_keys'])}")
        for key in report["missing_keys"]:
            print(f"  - [MISSING] {key}")

        print(f"Пустых переводов: {len(report['empty_keys'])}")
        for key in report["empty_keys"]:
            print(f"  - [EMPTY] {key}")

        print(f"Расхождений в плейсхолдерах: {len(report['placeholder_mismatches'])}")
        for item in report["placeholder_mismatches"]:
            print(f"  - [PLACEHOLDER] {item}")

        if report["extra_keys"]:
            print(f"Лишних ключей: {len(report['extra_keys'])}")
            for key in report["extra_keys"]:
                print(f"  - [EXTRA] {key}")
    except (requests.RequestException, OSError, json.JSONDecodeError) as error:
        print("Ошибка при проверке локализации:", error)


if __name__ == "__main__":
    main()
EOF
