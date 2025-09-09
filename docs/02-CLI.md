# 02 — CLI

CLI on toteutettu Click‑kirjastolla. Pääryhmä on `aspa`, jonka alla on alaryhmä `timer`.

## Komennot

- `aspa timer now`
  - Tulostaa nykyisen päivämäärän ja kellonajan.

- `aspa timer pomo`
  - Käynnistää interaktiivisen Pomodoro‑konsolin (tekstitila, Rich‑pohjainen).

## Käyttöesimerkkejä

```bash
# Nykyinen aika
aspa timer now

# Pomodoro-konsoli
aspa timer pomo
```

## Entry pointit

- Skripti: `app/cli.py`
- Konsolikomento: `aspa` (määritelty `pyproject.toml` → `[project.scripts]`)

## Tulostuksen muotoilu

Tulostus tehdään `app/utils/display.py` kautta, joka käyttää Richin `Console().print`‑metodia yhtenäiseen värimaailmaan.

