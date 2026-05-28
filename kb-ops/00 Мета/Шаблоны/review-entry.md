---
id: 
type: review-entry
date: 
operator: 
action_kind: promote
target_vault: kb-knowledge
target_paths: []
proposed_change: 
reasoning: 
sources: []
related_digest: ""
blocks: []
status: pending
decision: ""
decided_at: ""
version: "1.0"
tags: []
---

# Review {{date}} — {{action_kind}} on {{target_paths}}

## Что предлагается

Конкретное действие, которое AI просит подтвердить.

## Почему

Обоснование AI: что именно увидел, на основании какого источника, какая confidence.

- Источники: см. `sources`
- Связанные карточки: [[...]]

## Что блокирует пока не решено

Какие действия AI ставит на паузу до ответа. Заполнить `blocks` если что-то реально ждёт.

## Действие Pavel'я

- [ ] approve — провести изменение
- [ ] reject — отменить
- [ ] edit — внести правки и провести (записать в `decision: edit`, описание правок ниже)

---

<!--
ПРАВИЛА для review-entry:

- `action_kind`: promote (draft→reviewed→canonical) | merge | conflict | new-ontology-node | delete | borrowed-add | content-canonical-change
- `target_vault`: kb-knowledge | kb-clients | kb-ops
- `status`: pending → approved | rejected | edited
- Каждая запись BLOCKS соответствующее действие AI до изменения `status` с pending. Это контракт; AI не должен «обходить» pending review.
- После решения: `status` обновляется, `decision` фиксирует выбор, `decided_at` — дата. Запись остаётся в inbox как след истории (можно архивировать вручную раз в месяц).
- Не дублировать с digest — review — это решение, digest — сводка.
-->
