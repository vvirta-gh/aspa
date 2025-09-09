ASPA — Henkilökohtainen CLI‑sovelmien kokoelma
================================================

ASPA on komentoriviltä ajettava kokoelma pieniä apuohjelmia. Ensimmäinen valmis osa on ajanhallintaan liittyvä osio, jossa on kellonaika‑komento ja interaktiivinen Pomodoro‑ajastin.

- Asenna: `pip install -e .` (projektin juuressa)
- Aja: `aspa` tai `python -m app.cli`
- Pikaesimerkit:
  - Nykyinen aika: `aspa timer now`
  - Pomodoro‑konsoli: `aspa timer pomo`

Dokumentaatio
-------------
Projektin dokumentaatio on Markdown‑muodossa hakemistossa `docs/` (yhteensopiva Obsidianin ja Joplinin kanssa):

- [01‑Yleiskatsaus](docs/01-Yleiskatsaus.md)
- [02‑CLI](docs/02-CLI.md)
- [03‑Pomodoro](docs/03-00-Pomodoro.md)
- [03.01‑Pomodoro sekvenssikaavio](docs/03-01-Pomodoro_sekvenssikaavio.md)
- [04‑Arkkitehtuuri](docs/04-Arkkitehtuuri.md)
- [TODO / Roadmap](docs/TODO.md)

Lisenssi
--------
Tämä on kehitysvaiheessa; lisenssi voidaan lisätä myöhemmin.
