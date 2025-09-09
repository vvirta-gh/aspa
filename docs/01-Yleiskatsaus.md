# 01 — Yleiskatsaus

ASPA on komentorivisovellus (CLI), joka kokoaa yhteen pieniä arkikäyttöön sopivia työkaluja. Tässä vaiheessa mukana on:

- Ajan näyttäminen (`timer now`)
- Interaktiivinen Pomodoro‑ajastin (`timer pomo`)

Sovellus on kirjoitettu Pythonilla ja käyttää käyttöliittymäkomponentteihin Rich‑kirjastoa sekä Clickiä komentorakenteen määrittelyyn. Lokitukseen käytetään Logurua.

## Asennus

1. Varmista, että käytössäsi on Python 3.10+
2. Asenna riippuvuudet ja kehitystilassa itse paketti:

   ```bash
   pip install -e .
   ```

3. Käynnistä CLI:

   ```bash
   aspa
   ```

   tai

   ```bash
   python -m app.cli
   ```

## Pika-aloitus

- Näytä nykyinen aika:

  ```bash
  aspa timer now
  ```

- Käynnistä Pomodoro‑konsoli:

  ```bash
  aspa timer pomo
  ```

## Toiminnot lyhyesti

- **Nykyinen aika:** Tulostaa päivän ja kellonajan (muoto `YYYY-MM-DD HH:MM:SS`).
- **Pomodoro‑ajastin:** Interaktiivinen ajastinkonsoli, jossa voi aloittaa työjaksoja ja niiden perään lyhyitä tai pitkiä taukoja. Asetuksia voi muokata konsolista, ja perusstatistiikkaa näytetään istunnon aikana.

Lisätiedot: [02‑CLI](02-CLI.md), [03‑Pomodoro](03-Pomodoro.md), [04‑Arkkitehtuuri](04-Arkkitehtuuri.md).

