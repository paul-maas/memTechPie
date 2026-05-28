---
id: 
type: digest-entry
date: 
operator: 
session_kind: ingest
status: reviewed
version: "1.0"
tags: []
sources_processed: []
cards_created: 0
escalations_count: 0
related_audit: ""
related_decisions: []
---

# Digest {{date}} — {{session_kind}}

## Что сделано

Краткая сводка сессии — 2–4 предложения, чтобы Pavel мог пробежать глазами.

## Созданные карточки

- `[[cards/{type}/{id}]]` — однострочная аннотация
- ...

(Полный список — фильтр `fm_status:draft fm_extracted_by:<этой_сессии>`.)

## Найденные дубликаты / расширения

- {{ссылка на decision-запись в kb-ops/inbox/}} — что предложено

## Конфликты (concept-conflict)

- {{ссылка на decision-запись}}

## Пробелы онтологии

- {{какая школа/парадигма обнаружена впервые}} → {{ссылка на decision}}

## Связанное

- Audit-запись: `[[kb-ops/audit/{date}]]`
- Decisions, ждущие review: см. `related_decisions`

---

<!--
ПРАВИЛА для digest-entry:

- Один файл на сессию или на день (батчево).
- `session_kind`: ingest | groom | conflict-resolve | content-production
- `cards_created`, `escalations_count` — численные счётчики для метрик здоровья базы.
- Digest НЕ блокирует. Если требуется решение Pavel'я — оно живёт в `kb-ops/inbox/` (review-entry), а здесь только ссылка.
- Не дублировать содержание audit log — digest это user-facing сводка, audit — машинно-читаемый журнал.
-->
