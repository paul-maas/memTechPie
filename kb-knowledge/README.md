# kb-knowledge

Vault домена: конституция метода, онтология школ, атомарные карточки знаний, источники, плейбуки оператора.

## Структура папок

```
00 Мета/
  Шаблоны/         — frontmatter-шаблоны по типам документов
constitution/      — Constitution.md (методология Pavel'я) + версии
ontology/
  schools/         — узлы школ (Gestalt, CBT, ICF, Erickson, Coactive, ...)
  paradigms/       — узлы парадигм (cognitive, behavioral, systemic, humanistic, ...)
cards/
  concepts/        — карточки концепций
  techniques/      — карточки техник
  frameworks/      — карточки фреймворков и моделей
  conflicts/       — карточки concept-conflict (явные методические противоречия)
  borrowed/        — карточки заимствованных элементов
sources/           — сырая библиотека: source-записи (метаданные)
  raw/             — полные тексты книг/статей/расшифровок (.md), сырьё для экстракции
playbooks/         — плейбуки оператора (ingest, groom, conflict-resolve, content-production, ...)
```

> Очередь изменений на review (`inbox/`) и audit log живут в `kb-ops`, не здесь. Draft-карточки находятся прямо в `cards/{type}/` со `status: draft` (фильтр `fm_status:draft`), отдельной inbox-папки для них нет.

## Frontmatter-схема

Каждая карточка несёт обязательный frontmatter. Полная схема — в шаблонах `00 Мета/Шаблоны/`. Ключевые поля:

- `id`, `title`, `type` (concept | technique | framework | concept-conflict | borrowed)
- `school`, `paradigm` (ссылки на узлы онтологии)
- `status` (draft | reviewed | canonical), `confidence` (low | medium | high)
- `sources`, `related`, `similar`, `conflicts_with`
- `extracted_by`, `last_verified`, `version`

Все ключевые поля индексируются в ChromaDB как `fm_*` через `obsidian-intelligence` >= 0.2.2 и доступны для фильтрации через `where_metadata` в `semantic_search`.

## Правила гигиены

- Канонизация (`draft → reviewed → canonical`) — только через явное действие Pavel'я, AI не повышает confidence сам
- Любое изменение `canonical`-карточки → bump `version` + обновление `last_verified` + запись в audit (`kb-ops/audit/`)
- Wikilinks в frontmatter: для фильтруемых полей (`school`, `paradigm`) хранить чистое имя без скобок; wikilink делать в теле карточки
