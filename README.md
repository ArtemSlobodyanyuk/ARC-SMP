# Advanced Relational Cartography and System Modeling Platform (ARC)

Це репозиторій із GUI-прототипом ARC: редактор "полотна", де можна додавати об’єкти (поки що базові фігури), перетягувати їх, редагувати властивості, а також зберігати/завантажувати сцену.

## Структура

- Основний застосунок (PyQt6): `arc/`
- Сумісність зі старим пакетом: `red2/` (форвардить запуск у `arc`)
- Прототипи/чернетки:
  - PyQt6 (моноліт): `prototypes/beta.py`
  - Tkinter: `prototypes/beta2.py`
- Збереження сцен: `saves/`
- Документація по помічнику: `docs/ARATON.md`

## Запуск (Windows)

1. Створи/активуй virtualenv
2. Встанови залежності:
   - `pip install -r requirements.txt`
3. Запуск:
   - `python -m arc`

## Коротко про функції

- Полотно: `QGraphicsScene` + `QGraphicsView`
- Додавання: Toolbar "Add items" → `Circle / Square / Rectangle`
- Взаємодія:
  - Drag: рух об’єкта
  - Double click: властивості (`name`, `note`, розмір)
  - Delete: видалення зі сцени
  - Save/Load: збереження/завантаження сцени у JSON
