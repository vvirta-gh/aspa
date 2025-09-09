# 04 — Arkkitehtuuri

## Pakettirakenne

- `app/cli.py`: Click‑pohjainen komentototeutus ja pääsisäänkäynti (`aspa`).
- `app/commands/time.py`: `get_current_time()` joka palauttaa ajan merkkijonona.
- `app/models/pomodoro.py`: `PomodoroTimer`‑luokka ja koko interaktiivinen konsolilogiikka.
- `app/utils/display.py`: Yhtenäiset tulostusapuohjelmat Richillä.

## Riippuvuudet

- Click — komentorakenteet ja komennot
- Rich — tyylitelty konsolikäyttöliittymä (taulukot/paneelit/värit)
- Loguru — kevyt lokituskirjasto
- Pytest — testien ajamiseen

Kaikki on määritelty `pyproject.toml`‑tiedostossa. Komentorivi‐entry `aspa` osoittaa `app.cli:main`.

## PomodoroTimer lyhyesti

- Asetukset (`settings`): `work_duration`, `short_break`, `long_break`, `long_break_interval`
- Tilastot (`stats`): `total_sessions`, `pomodoros_today`, `sessions_today`, `total_worktime`
- Päätoiminnot: `show_main_menu()`, `start_session()`, `run_timer()`, `configure_settings()`, `view_stats()`
- Non‑blocking input: `is_input_available()` + alustakohtaiset toteutukset

## Lokitus ja diagnostiikka

- CLI:n käynnistyksessä kirjataan `Aspa CLI started` (Loguru).
- Pomodoro‑konsolin käynnistys kirjataan infona.

## Testit

- `tests/test_time.py` varmistaa, että `get_current_time()` palauttaa merkkijonon muodossa `YYYY-MM-DD HH:MM:SS`.

## Mahdollinen jatkokehitys

- Tilastojen pysyvä tallennus (esim. JSON/SQLite)
- Konfiguraation tallennus käyttäjäprofiiliin (esim. `~/.config/aspa/config.toml`)
- Parempi ajastinnäyttö (progress bar, äänimerkki, ilmoitus)
- Unit testejä PomodoroTimerille (aikaan liittyvien toimintojen mockaus)

