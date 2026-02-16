# Speedskating Manager (desktop-first prototype)

Je had helemaal gelijk: dit is nu **geen browsergame** meer.

Deze repository bevat nu een **native-gerichte simulatiekern** in Python die je later aan een echte engine (bijv. Godot/Unity/Unreal) kunt koppelen.

## Wat is aangepast t.o.v. vorige versie

- Browser UI verwijderd.
- Race-model aangepast naar **langebaanschaatsen-regels**:
  - 400m ovaal baanmodel.
  - Exact **2 schaatsers** per rit.
  - **Lane switch op kruisingen** (elke 200m).
  - Alleen **vaste officiële afstanden**: 500, 1000, 1500, 3000, 5000, 10000.

## Structuur

- `speedskating_manager/models.py` – team/schaatser/distance modellen.
- `speedskating_manager/track.py` – 400m baan en crossover-logica.
- `speedskating_manager/race.py` – head-to-head racesimulatie met splits.
- `main.py` – demo-run in CLI.
- `tests/` – regressietests op de kernregels.

## Run

```bash
python3 main.py
```

## Tests

```bash
python3 -m pytest -q
```

## Volgende stap (richting volledige game)

- Deze kern direct koppelen aan een native 3D client (bijv. Godot), inclusief:
  - echte ovale 400m baanmesh;
  - twee-schaatser ritpresentatie + lane-crossovers;
  - seizoen/kalender/contracts/sponsors.
