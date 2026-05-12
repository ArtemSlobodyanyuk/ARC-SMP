# Mods

Мод = папка в `mods/` з Python-пакетом.

Мінімальна структура:

```
mods/my_mod/
  __init__.py
  mod.json
  mod.py
```

`mod.json` приклад:

```json
{
  "id": "my_mod",
  "name": "My Mod",
  "version": "0.1.0",
  "entrypoint": "mod:register"
}
```

Точка входу `mod.py` повинна мати `register(api)`.

