# scripts

Утилиты сопровождения KB.

## validate_frontmatter.py

Проходит по vault'ам, проверяет соответствие frontmatter схеме (типы, обязательные поля, допустимые значения enum-полей `status`, `confidence`, `type`).

**Использование:**

```bash
python scripts/validate_frontmatter.py kb-knowledge
python scripts/validate_frontmatter.py kb-knowledge kb-clients kb-ops
python scripts/validate_frontmatter.py --all
```

Выход:
- Код 0: все ноты прошли валидацию
- Код 1: найдены проблемы (выводятся в stderr с путями и описанием)

**Зависимости:** Python 3.10+, `pyyaml`. Запускать через `uv run` или активированный venv.
