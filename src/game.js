import * as THREE from "https://unpkg.com/three@0.166.1/build/three.module.js";

const state = {
  budget: 500000,
  facilityLevel: 1,
  morale: 70,
  focus: "balanced",
  raceRunning: false,
  roster: [
    { name: "Noa de Vries", stamina: 72, technique: 75, sprint: 70, selected: true },
    { name: "Lars Bos", stamina: 78, technique: 68, sprint: 74, selected: true },
    { name: "Mila Kuipers", stamina: 66, technique: 80, sprint: 72, selected: true },
    { name: "Jens Slagter", stamina: 70, technique: 63, sprint: 82, selected: false },
    { name: "Sara Groen", stamina: 84, technique: 71, sprint: 65, selected: false },
  ],
};

const ui = {
  budget: document.querySelector("#budget"),
  facilityLevel: document.querySelector("#facilityLevel"),
  morale: document.querySelector("#morale"),
  focusLabel: document.querySelector("#focusLabel"),
  trainingFocus: document.querySelector("#trainingFocus"),
  trainButton: document.querySelector("#trainButton"),
  upgradeButton: document.querySelector("#upgradeButton"),
  startRaceButton: document.querySelector("#startRaceButton"),
  roster: document.querySelector("#roster"),
  raceStatus: document.querySelector("#raceStatus"),
  leaderboard: document.querySelector("#leaderboard"),
  sceneContainer: document.querySelector("#sceneContainer"),
};

function focusText(focus) {
  return {
    balanced: "Balans",
    stamina: "Uithoudingsvermogen",
    technique: "Techniek",
    sprint: "Sprint",
  }[focus];
}

function applyTraining(skater) {
  const boost = 1 + state.facilityLevel * 0.3;
  if (state.focus === "stamina") skater.stamina = Math.min(skater.stamina + 2 * boost, 99);
  if (state.focus === "technique") skater.technique = Math.min(skater.technique + 2 * boost, 99);
  if (state.focus === "sprint") skater.sprint = Math.min(skater.sprint + 2 * boost, 99);
  if (state.focus === "balanced") {
    skater.stamina = Math.min(skater.stamina + 0.7 * boost, 99);
    skater.technique = Math.min(skater.technique + 0.7 * boost, 99);
    skater.sprint = Math.min(skater.sprint + 0.7 * boost, 99);
  }
}

function renderRoster() {
  ui.roster.innerHTML = "";
  state.roster.forEach((s, index) => {
    const li = document.createElement("li");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = s.selected;
    checkbox.addEventListener("change", () => {
      const selectedCount = state.roster.filter((r) => r.selected).length;
      if (checkbox.checked && selectedCount >= 3) {
        checkbox.checked = false;
        return;
      }
      s.selected = checkbox.checked;
      renderRoster();
    });

    const detail = document.createElement("span");
    detail.textContent = `${s.name} • U${Math.round(s.stamina)} T${Math.round(s.technique)} S${Math.round(s.sprint)}`;

    li.append(detail, checkbox);
    ui.roster.appendChild(li);
  });
}

function renderStats() {
  ui.budget.textContent = Math.round(state.budget).toLocaleString("nl-NL");
  ui.facilityLevel.textContent = String(state.facilityLevel);
  ui.morale.textContent = String(Math.round(state.morale));
  ui.focusLabel.textContent = focusText(state.focus);
  renderRoster();
}

ui.trainingFocus.addEventListener("change", (event) => {
  state.focus = event.target.value;
  renderStats();
});

ui.trainButton.addEventListener("click", () => {
  if (state.budget < 5000) return;
  state.budget -= 5000;
  state.morale = Math.min(100, state.morale + 2);
  state.roster.forEach(applyTraining);
  renderStats();
});

ui.upgradeButton.addEventListener("click", () => {
  if (state.budget < 100000) return;
  state.budget -= 100000;
  state.facilityLevel += 1;
  state.morale = Math.min(100, state.morale + 5);
  renderStats();
});

function createScene(container) {
  const width = container.clientWidth;
  const height = container.clientHeight;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x07101f);

  const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
  camera.position.set(0, 18, 28);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  container.appendChild(renderer.domElement);

  const ambient = new THREE.AmbientLight(0xffffff, 0.8);
  scene.add(ambient);

  const dir = new THREE.DirectionalLight(0xffffff, 0.8);
  dir.position.set(8, 15, 10);
  scene.add(dir);

  const ice = new THREE.Mesh(
    new THREE.RingGeometry(5.3, 11.5, 80),
    new THREE.MeshStandardMaterial({ color: 0x9cd8ff, roughness: 0.12, metalness: 0.1 })
  );
  ice.rotation.x = -Math.PI / 2;
  scene.add(ice);

  const infield = new THREE.Mesh(
    new THREE.CircleGeometry(5.1, 50),
    new THREE.MeshStandardMaterial({ color: 0x1f2937 })
  );
  infield.rotation.x = -Math.PI / 2;
  scene.add(infield);

  const skaterGeometry = new THREE.BoxGeometry(0.45, 0.45, 0.45);
  const colors = [0xf97316, 0x22c55e, 0x3b82f6, 0xeab308, 0xa855f7, 0xef4444];

  const skaters = state.roster
    .filter((r) => r.selected)
    .map((skater, i) => {
      const mesh = new THREE.Mesh(
        skaterGeometry,
        new THREE.MeshStandardMaterial({ color: colors[i % colors.length] })
      );
      mesh.position.set(8.2 + i * 0.5, 0.25, 0);
      scene.add(mesh);

      const baseSpeed =
        (skater.stamina * 0.32 + skater.technique * 0.33 + skater.sprint * 0.35 + state.morale * 0.12) /
        210;

      return {
        name: skater.name,
        mesh,
        lane: 8.2 + i * 0.5,
        t: 0,
        speed: baseSpeed * (0.985 + Math.random() * 0.03),
        progress: 0,
      };
    });

  return { scene, camera, renderer, skaters };
}

function updateLeaderboard(skaters) {
  const ranking = [...skaters].sort((a, b) => b.progress - a.progress);
  ui.leaderboard.innerHTML = "";
  ranking.forEach((s) => {
    const li = document.createElement("li");
    li.textContent = `${s.name} — ${(s.progress * 400).toFixed(0)} m`;
    ui.leaderboard.appendChild(li);
  });
}

function startRace() {
  if (state.raceRunning) return;
  const selected = state.roster.filter((r) => r.selected);
  if (selected.length !== 3) {
    ui.raceStatus.textContent = "Selecteer exact 3 schaatsers";
    return;
  }

  state.raceRunning = true;
  ui.raceStatus.textContent = "Race bezig...";
  ui.sceneContainer.innerHTML = "";

  const { scene, camera, renderer, skaters } = createScene(ui.sceneContainer);
  const laps = 8;

  function animate() {
    let finished = 0;
    skaters.forEach((s, index) => {
      s.t += s.speed * 0.012;
      s.progress = s.t;
      const angle = s.t * Math.PI * 2;
      const wobble = Math.sin(s.t * 18 + index) * 0.05;
      const x = Math.cos(angle) * (s.lane + wobble);
      const z = Math.sin(angle) * (s.lane + wobble);
      s.mesh.position.set(x, 0.25, z);

      if (s.t >= laps) finished += 1;
    });

    updateLeaderboard(skaters);
    renderer.render(scene, camera);

    if (finished === skaters.length) {
      state.raceRunning = false;
      const winner = [...skaters].sort((a, b) => b.progress - a.progress)[0];
      ui.raceStatus.textContent = `Finish! Winnaar: ${winner.name}`;
      state.budget += 45000;
      state.morale = Math.min(100, state.morale + 4);
      renderStats();
      return;
    }

    requestAnimationFrame(animate);
  }

  requestAnimationFrame(animate);
}

ui.startRaceButton.addEventListener("click", startRace);

window.addEventListener("resize", () => {
  if (!ui.sceneContainer.firstChild) return;
  const canvas = ui.sceneContainer.querySelector("canvas");
  if (!canvas) return;
  canvas.style.width = "100%";
  canvas.style.height = "100%";
});

renderStats();
updateLeaderboard([]);
