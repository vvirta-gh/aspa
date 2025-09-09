# 03 — Pomodoro‑ajastin

Pomodoro‑ajastin tarjoaa tekstipohjaisen (Rich) käyttöliittymän, jossa voit:

- Aloittaa työjakson (oletus 25 min)
- Päättää työjakson ja aloittaa tauon (lyhyt 5 min, pitkä 15 min)
- Muokata asetuksia
- Tarkastella perusstatistiikkaa

Käynnistys: `aspa timer pomo` → päävalikko.

## Päävalikko

Valikossa näkyvät kuluvan päivän istuntomäärät ja kokonais‑“worktime”. Vaihtoehdot:

1. Start a new session — aloittaa työjakson
2. View settings — näytä ja muokkaa asetuksia
3. View stats — näytä tilastot taulukkona
4. Exit — palaa komentoriville

## Asetukset (oletukset)

- `work_duration`: 25 minuuttia
- `short_break`: 5 minuuttia
- `long_break`: 15 minuuttia
- `long_break_interval`: 4 (joka neljännen työjakson jälkeen pitkä tauko)

Näitä arvoja voi muuttaa suoraan konsolista (valinta 2). Sovellus validoi arvot kokonaisluvuiksi.

## Istunnon kulku

1. Työjakso käynnistyy ja näytölle piirtyy ajastin.
2. Enterin painalluksella (työjakson aikana) voit keskeyttää ja siirtyä taukokysymykseen.
3. Työjakson päätyttyä kysytään haluatko tauolle (lyhyt tai pitkä riippuen intervallista).
4. Tauon jälkeen paluu valikkoon tai uuteen istuntoon.

## Tilastot

- `pomodoros_today`: suoritettujen työjaksojen määrä tänään
- `sessions_today`: aloitettujen istuntojen määrä tänään
- `total_worktime`: kaikkien tähän mennessä tehtyjen työjaksojen minuutit
- Näytetään taulukkona; jos istuntoja on ≥ 1, lasketaan myös keskiarvo `Avg Work per Session`.

## Monialustainen syöte (non‑blocking)

Työjakson aikana sovellus kuuntelee näppäimistöä ilman, että ajastin pysähtyy:

- Windows: `msvcrt.kbhit()` ja `msvcrt.getch()`
- Linux/Mac: `select.select()` `sys.stdin`‑virtaan; kun syöte on saatavilla, luetaan `sys.stdin.readline()`

Tämä mahdollistaa Enterin painamisen “kesken ajastuksen” ilman pysäytystä.

## Tunnetut rajoitteet / TODO

- Ajastimen reaaliaikainen “rivin päivitys” riippuu päätteen ominaisuuksista; eri terminaalit voivat renderöidä kursoria eri tavoin.
- Konsoli on tilaton käynnistysten välillä; statsit nollautuvat sovelluksen sammuttua. Persistenssi on hyvä jatkokehitysidea.
- Korjattu: ajastimen rivin tunniste on nyt dynaaminen (esim. “Work” / “Short Break”).

Lisätiedot toteutuksesta: [04‑Arkkitehtuuri](04-Arkkitehtuuri.md).
