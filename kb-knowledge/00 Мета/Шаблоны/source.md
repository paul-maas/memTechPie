---
id: 
title: 
type: source
authors: []
year: 
language: 
school: 
paradigm: 
source_type: book
status_kind: primary
themes: []
ingested_at: ""
chunks_indexed: 0
sources: []
related: []
status: reviewed
confidence: high
last_verified: ""
version: "1.0"
tags: []
---

# {{title}}

## Библиографические данные

- Автор(ы): {{authors}}
- Год: {{year}}
- Язык: {{language}}
- Школа / традиция: {{school}}
- Тип: книга / статья / лекция / расшифровка / собственные материалы

## Темы

Ключевые темы (`themes` во frontmatter).

## Кратко о содержании

Что в этом источнике, в одном-двух абзацах. Не пересказ — ориентир.

## Карточки, извлечённые из источника

- [[cards/concepts/...]]
- [[cards/techniques/...]]
- ...

## Заметки коуча

Личные пометки Pavel'я, чем источник важен для метода, какие сомнения, какие места требуют перечтения.

---

<!--
ПРАВИЛА для source:

- `source_type`: book | article | lecture | transcript | own_material | course
- `status_kind`: primary (первоисточник) | retelling (пересказ) | criticism (критика)
- `language`: ru | en | (другое)
- Файл с метаданными живёт в `sources/`. Полный текст книги (если есть) — отдельный файл рядом с тем же id (например `id-full.md`), индексируется MCP, но карточки строятся НЕ из него (anti-echo), а из источника напрямую при первом ингесте.
-->
