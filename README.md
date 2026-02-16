# Speedskating Manager (native-first, met 3D Godot prototype)

Je feedback is verwerkt:

- **Geen browsergame**.
- Wel een **native 3D component** via Godot.
- Race-regels aangepast naar langebaanschaatsen met juiste basisstructuur.

## Wat zit erin

### 1) Godot 3D prototype (`godot/`)

Een simpele native 3D scène met:
- ovale 400m baanopbouw (2x bocht + 2x recht stuk);
- exact 2 schaatsers in de rit;
- lane switching **1x per 400m ronde**;
- visuele markering van finish-rechte stuk en crossover-rechte stuk.

Startscene:
- `godot/scenes/Main.tscn`
- Script: `godot/scripts/main.gd`

### 2) Simulatiekern in Python (`speedskating_manager/`)

- Team/schaatsermodellen.
- Officiële vaste afstanden: 500/1000/1500/3000/5000/10000.
- 2-schaatser head-to-head races.
- Crossover-logica: één wissel per 400m lap.

## Regels die nu expliciet zijn gemaakt

- 400m langebaan als rondeafstand.
- Ronde opgebouwd uit vier segmenten van 100m.
- Eén kruising/wissel per ronde (dus bij 1000m: op 400 en 800).
- Rit met exact twee schaatsers.
- Afstanden zijn gefixeerd op officiële set.

## Draaien

### Godot (aanbevolen, 3D)
1. Open Godot 4.x.
2. Import `godot/project.godot`.
3. Run project.

### Python demo (alleen simulatie-output)
```bash
python3 main.py
```

## Tests

```bash
python3 -m pytest -q
```
