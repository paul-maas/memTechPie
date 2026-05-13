---
id: 
type: audit-entry
date: 
operator: 
playbook: 
action: 
target_vault: 
target_paths: []
confidence_before: 
confidence_after: 
status_before: 
status_after: 
sources: []
reasoning: 
escalated: false
status: reviewed
tags: []
---

# Audit: {{date}} — {{action}} on {{target_paths}}

## Что сделано

Краткое описание изменения (одно-два предложения).

## Основание

Почему это сделано: ссылка на источник, на запрос Pavel'я, на триггер плейбука.

- Источники: см. `sources`
- Связанные карточки: [[...]]

## Цепочка изменений

Если затронуто несколько файлов — перечислить:

- `{{path 1}}`: {{что изменилось}}
- `{{path 2}}`: {{что изменилось}}

## Эскалация

Если `escalated: true` — какой `inbox/`-файл создан для review Pavel'я, что в нём.

---

<!--
ПРАВИЛА для audit-entry:

- Один файл `audit/YYYY-MM-DD.md` агрегирует записи за день, либо одна папка `audit/YYYY-MM-DD/` с файлами на каждое действие — на этапе (г) выберем удобный формат.
- Append-only. Никаких правок задним числом.
- `operator`: claude-opus-4-7 | claude-sonnet-4-6 | human (если Pavel правит вручную)
- `action`: create-draft | update-card | merge-cards | delete | promote-confidence | demote-confidence | dedup | rename | ...
- `target_vault`: kb-knowledge | kb-clients | kb-ops
- `confidence_*` и `status_*` заполнены только если действие меняло эти поля; иначе пустые.
-->
