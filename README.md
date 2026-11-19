# Raspored repetitora – problem zadovoljenja ograničenja (CSP)

Projekt iz kolegija *Deklarativno programiranje* (FOI, 2023./2024.).

Program traži raspored **3 repetitora (bazne stanice)** na mreži 10 × 10 koji pokriva
10 gradova s različitim brojem stanovnika. Problem je modeliran **deklarativno**:
opisana su ograničenja koja rješenje mora zadovoljiti, a pretragu obavlja
CSP solver iz biblioteke `python-constraint`.

## Ograničenja
| Ograničenje | Opis |
|---|---|
| Razmak | repetitori moraju biti međusobno udaljeni najmanje 2 jedinice |
| Pokrivenost | barem **85 %** ukupnog stanovništva mora biti unutar dometa (polumjer 3) |
| Kapacitet | jedan repetitor može pokriti najviše **90 000** stanovnika |

Varijable su koordinate `(x, y)` svakog repetitora, a domena su cjelobrojne točke mreže.

## Grafičko sučelje (Tkinter)
- prikazuje gradove (plava točka, naziv i broj stanovnika) i repetitore (crvena točka, oznaka R1–R3)
- crveni krug označava domet repetitora, a plavi krug minimalni razmak
- kapacitet i postotak pokrivenosti mogu se mijenjati u sučelju, a gumb
  **„Nanovo izračunaj“** ponovno pokreće solver s novim ograničenjima

## Pokretanje
Potreban je Python 3.

```bash
pip install python-constraint
python3 csp_repetitori.py
```

Tkinter je obično dio standardne instalacije Pythona. Ako nedostaje, na Debianu ili Ubuntuu instalira se naredbom:

```bash
sudo apt install python3-tk
```

> Postotak pokrivenosti unosi se kao decimalni broj (npr. `0.85` za 85 %).

## Tehnologije
Python 3 · python-constraint · Tkinter

## Licenca
GPL-3.0
