const performanceProfiles = {
  silent: {
    label: 'Silent',
    cpuTemp: 61,
    gpuLoad: 42,
    acoustics: 27,
    powerDraw: 380,
    psuHeadroom: 62,
    timeline: [
      { title: 'BIOS X780E 2.04', status: 'Installé il y a 2 jours' },
      { title: 'vBIOS RTX 5090 1.3', status: 'Disponible' },
      { title: 'Lighting Firmware 4.2', status: 'Synchronisé' },
    ],
    curves: {
      cpu: [
        [0, 10],
        [20, 18],
        [40, 26],
        [60, 35],
        [80, 46],
        [100, 58],
      ],
      gpu: [
        [0, 14],
        [20, 22],
        [40, 30],
        [60, 42],
        [80, 55],
        [100, 68],
      ],
      psu: [
        [0, 6],
        [20, 11],
        [40, 18],
        [60, 26],
        [80, 33],
        [100, 40],
      ],
    },
  },
  balanced: {
    label: 'Balanced',
    cpuTemp: 67,
    gpuLoad: 58,
    acoustics: 30,
    powerDraw: 480,
    psuHeadroom: 52,
    timeline: [
      { title: 'BIOS X780E 2.04', status: 'Installé il y a 2 jours' },
      { title: 'Ryzen Microcode Patch 1.11', status: 'Planifié ce soir' },
      { title: 'vBIOS RTX 5090 1.3', status: 'Disponible' },
      { title: 'RGB Controler', status: 'Synchronisé' },
    ],
    curves: {
      cpu: [
        [0, 15],
        [20, 25],
        [40, 35],
        [60, 48],
        [80, 60],
        [100, 72],
      ],
      gpu: [
        [0, 18],
        [20, 28],
        [40, 40],
        [60, 53],
        [80, 66],
        [100, 80],
      ],
      psu: [
        [0, 8],
        [20, 16],
        [40, 24],
        [60, 33],
        [80, 44],
        [100, 55],
      ],
    },
  },
  turbo: {
    label: 'Turbo',
    cpuTemp: 77,
    gpuLoad: 92,
    acoustics: 35,
    powerDraw: 640,
    psuHeadroom: 36,
    timeline: [
      { title: 'BIOS X780E 2.05 Beta', status: 'Test en cours' },
      { title: 'Ryzen Curve Optimizer', status: 'Appliqué' },
      { title: 'vBIOS RTX 5090 1.4', status: 'Poussé il y a 4 h' },
      { title: 'RGB Controller', status: 'Synchronisé' },
    ],
    curves: {
      cpu: [
        [0, 25],
        [20, 38],
        [40, 50],
        [60, 63],
        [80, 78],
        [100, 90],
      ],
      gpu: [
        [0, 24],
        [20, 38],
        [40, 55],
        [60, 70],
        [80, 86],
        [100, 100],
      ],
      psu: [
        [0, 10],
        [20, 20],
        [40, 35],
        [60, 50],
        [80, 66],
        [100, 82],
      ],
    },
  },
};

const showroomScenes = {
  silentSapphire: {
    label: 'Silent Sapphire',
    description:
      'Atmosphère feutrée bleutée, synchronisée avec le profil Silent pour démontrer le châssis silencieux &lt;32 dBA.',
    lighting: 'Température de couleur : 6200 K · Accent or profond',
    highlights: [
      'Mise en avant du fingerprint scanner avec halo bleu',
      'Overlay de storytelling sur la garantie concierge 5 ans',
      'Hotspot interactif sur le double USB4 frontal',
    ],
    hue: 210,
  },
  turboEmber: {
    label: 'Turbo Ember',
    description:
      'Ambiance chaude et énergique synchronisée au profil Turbo avec projection des courbes de puissance.',
    lighting: 'Température de couleur : 3400 K · Accent rouge-or',
    highlights: [
      'Animation des ventilateurs vapor loop',
      'Projection HUD des performances RTX 5090',
      'CTA direct vers la configuration Turbo pour les démos IA',
    ],
    hue: 24,
  },
  partnerSignature: {
    label: 'Partner Signature',
    description:
      'Mode vitrine personnalisable co-brandé avec import d’actifs partenaires et éclairage programmable.',
    lighting: 'Température de couleur : 4600 K · Accent champagne',
    highlights: [
      'Zone de dépôt pour logos partenaires (protection du logo EternaDream)',
      'Playlist de scènes automatisées pour showroom',
      'Formulaire de capture de leads connecté au CRM partenaire',
    ],
    hue: 48,
  },
};

const playbookTemplates = [
  {
    title: 'Maintenance trimestrielle',
    description:
      'Rappel service TIM métal liquide et validation acoustique Silent &lt; 32 dBA.',
  },
  {
    title: 'Surge Watch',
    description: 'Analyse automatique des journaux 2 kV et création de ticket partenaire.',
  },
  {
    title: 'Update Express',
    description: 'Propagation groupée du BIOS X780E et vérification TPM chiffrée.',
  },
];

const fleetSystems = [
  {
    asset: 'EDX-771',
    site: 'Paris Flagship',
    profile: 'Turbo Ember',
    firmware: 'BIOS 2.05β',
    alerts: 2,
    status: 'warning',
    coords: [68, 42],
  },
  {
    asset: 'EDX-772',
    site: 'Paris Flagship',
    profile: 'Silent Sapphire',
    firmware: 'BIOS 2.04',
    alerts: 0,
    status: 'healthy',
    coords: [66, 55],
  },
  {
    asset: 'EDX-810',
    site: 'Tokyo Gallery',
    profile: 'Partner Signature',
    firmware: 'BIOS 2.04',
    alerts: 1,
    status: 'warning',
    coords: [85, 38],
  },
  {
    asset: 'EDX-515',
    site: 'Dubai Lounge',
    profile: 'Silent Sapphire',
    firmware: 'BIOS 2.04',
    alerts: 0,
    status: 'healthy',
    coords: [80, 60],
  },
  {
    asset: 'EDX-120',
    site: 'Lyon Partner Lab',
    profile: 'Balanced',
    firmware: 'BIOS 2.03',
    alerts: 0,
    status: 'healthy',
    coords: [60, 48],
  },
  {
    asset: 'EDX-421',
    site: 'Remote Demo Van',
    profile: 'Turbo Ember',
    firmware: 'BIOS 2.02',
    alerts: 3,
    status: 'offline',
    coords: [40, 62],
  },
];

const state = {
  activeConcept: 'concept-a',
  performanceProfile: 'balanced',
  boostLevel: 35,
  telemetryInterval: null,
  showroomScene: 'silentSapphire',
  tourCount: 0,
  offlineMode: false,
  fleetFilter: 'all',
  fleetSearch: '',
  playbooks: [...playbookTemplates],
};

const modeButtons = document.querySelectorAll('.mode-switcher__btn');
const conceptSections = document.querySelectorAll('.concept');
const profileButtons = document.querySelectorAll('[data-profile]');
const activeProfileChip = document.querySelector('[data-active-profile]');
const telemetryElements = {
  cpuTemp: document.querySelector('[data-telemetry="cpuTemp"]'),
  gpuLoad: document.querySelector('[data-telemetry="gpuLoad"]'),
  acoustics: document.querySelector('[data-telemetry="acoustics"]'),
  powerDraw: document.querySelector('[data-telemetry="powerDraw"]'),
  psuHeadroom: document.querySelector('[data-telemetry="psuHeadroom"]'),
};
const curvePlot = document.querySelector('[data-curve-plot]');
const powerBar = document.querySelector('[data-power-bar]');
const otaList = document.querySelector('[data-ota-list]');
const boostRange = document.getElementById('boostRange');
const boostValue = document.getElementById('boostValue');
const toast = document.querySelector('[data-toast]');

const sceneButtons = document.querySelectorAll('[data-scene]');
const sceneTitle = document.querySelector('[data-scene-title]');
const sceneDescription = document.querySelector('[data-scene-description]');
const sceneLighting = document.querySelector('[data-scene-lighting]');
const sceneHighlights = document.querySelector('[data-scene-highlights]');
const sceneCount = document.querySelector('[data-scene-count]');
const conciergeStatus = document.querySelector('[data-concierge-status]');
const offlineIndicator = document.querySelector('[data-offline-indicator]');
const tourProgress = document.querySelector('[data-tour-progress]');
const themeFilename = document.querySelector('[data-theme-filename]');
const themePreview = document.querySelector('[data-theme-preview]');
const lightingHue = document.getElementById('lightingHue');
const lightingHueValue = document.getElementById('lightingHueValue');

const fleetFilterButtons = document.querySelectorAll('[data-fleet-filter]');
const fleetSearchInput = document.querySelector('[data-fleet-search]');
const fleetTableBody = document.querySelector('[data-fleet-table]');
const fleetMap = document.querySelector('[data-fleet-map]');
const fleetCount = document.querySelector('[data-fleet-count]');
const securityAlerts = document.querySelector('[data-security-alerts]');
const slaValue = document.querySelector('[data-sla-value]');
const playbookList = document.querySelector('[data-playbook-list]');
const supportLog = document.querySelector('[data-support-log]');
const securityChip = document.querySelector('[data-security-chip]');
const networkChip = document.querySelector('[data-network-chip]');

const performanceButtons = {
  turbo: document.querySelector('[data-activate-turbo]'),
  sync: document.querySelector('[data-sync-lighting]'),
};

const ctaButtons = {
  maintenance: document.querySelector('[data-open-maintenance]'),
  startTour: document.querySelector('[data-start-tour]'),
  toggleOffline: document.querySelector('[data-toggle-offline]'),
  openMqtt: document.querySelector('[data-open-mqtt]'),
  exportMetrics: document.querySelector('[data-export-metrics]'),
  createPlaybook: document.querySelector('[data-create-playbook]'),
  openSupport: document.querySelector('[data-open-support]'),
};

const showToast = (message) => {
  if (!toast) return;
  toast.textContent = message;
  toast.hidden = false;
  toast.classList.add('toast--visible');
  setTimeout(() => {
    toast.classList.remove('toast--visible');
    toast.hidden = true;
  }, 3000);
};

const updateMode = (targetId) => {
  state.activeConcept = targetId;
  conceptSections.forEach((section) => {
    const isActive = section.id === targetId;
    section.classList.toggle('concept--active', isActive);
    section.setAttribute('aria-hidden', String(!isActive));
  });

  modeButtons.forEach((button) => {
    const isActive = button.dataset.target === targetId;
    button.classList.toggle('is-active', isActive);
  });

  if (targetId === 'concept-a') {
    startTelemetry();
  } else {
    stopTelemetry();
  }
};

const applyDrift = (value, variance) => {
  const drift = (Math.random() - 0.5) * variance;
  return Math.max(0, value + drift);
};

const renderTelemetry = () => {
  const profile = performanceProfiles[state.performanceProfile];
  if (!profile) return;

  const boostFactor = 1 + (state.boostLevel - 35) / 200;
  const cpuTemp = applyDrift(profile.cpuTemp * boostFactor, 2).toFixed(1);
  const gpuLoad = Math.min(100, applyDrift(profile.gpuLoad * boostFactor, 4)).toFixed(0);
  const acoustics = applyDrift(profile.acoustics + (state.boostLevel - 35) * 0.06, 1).toFixed(1);
  const powerDraw = applyDrift(profile.powerDraw * boostFactor, 15).toFixed(0);
  const headroom = Math.max(
    0,
    100 - Math.round((Number(powerDraw) / 1000) * 100)
  );

  telemetryElements.cpuTemp.textContent = `${cpuTemp}°C`;
  telemetryElements.gpuLoad.textContent = `${gpuLoad}%`;
  telemetryElements.acoustics.textContent = `${acoustics} dBA`;
  telemetryElements.powerDraw.textContent = `${powerDraw} W`;
  telemetryElements.psuHeadroom.textContent = `${headroom}%`;

  const powerPercent = Math.min(100, Math.round((Number(powerDraw) / 1000) * 100));
  if (powerBar) {
    powerBar.style.setProperty('--power-percent', `${powerPercent}`);
    powerBar.style.width = '100%';
    powerBar.setAttribute('aria-valuenow', String(powerPercent));
    powerBar.setAttribute('aria-valuemin', '0');
    powerBar.setAttribute('aria-valuemax', '100');
  }
};

const buildPath = (points) =>
  points
    .map((point, index) => {
      const [x, y] = point;
      const prefix = index === 0 ? 'M' : 'L';
      return `${prefix}${x},${60 - y}`;
    })
    .join(' ');

const renderCurves = () => {
  const profile = performanceProfiles[state.performanceProfile];
  if (!profile || !curvePlot) return;
  curvePlot.innerHTML = '';

  const createPath = (points, className) => {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', buildPath(points));
    path.setAttribute('class', className);
    curvePlot.appendChild(path);
  };

  createPath(profile.curves.cpu, 'curve curve--cpu');
  createPath(profile.curves.gpu, 'curve curve--gpu');
  createPath(profile.curves.psu, 'curve curve--psu');
};

const renderTimeline = () => {
  if (!otaList) return;
  otaList.innerHTML = '';
  const profile = performanceProfiles[state.performanceProfile];
  profile.timeline.forEach((item) => {
    const li = document.createElement('li');
    const title = document.createElement('span');
    title.className = 'timeline__title';
    title.textContent = item.title;
    const meta = document.createElement('span');
    meta.className = 'timeline__meta';
    meta.textContent = item.status;
    li.append(title, meta);
    otaList.appendChild(li);
  });
};

const setPerformanceProfile = (profileKey) => {
  if (!performanceProfiles[profileKey]) return;
  state.performanceProfile = profileKey;
  profileButtons.forEach((btn) => {
    const isActive = btn.dataset.profile === profileKey;
    btn.classList.toggle('is-active', isActive);
  });
  activeProfileChip.textContent = `Profil actif : ${performanceProfiles[profileKey].label}`;
  renderTelemetry();
  renderCurves();
  renderTimeline();
};

const startTelemetry = () => {
  renderTelemetry();
  renderCurves();
  renderTimeline();
  if (state.telemetryInterval) return;
  state.telemetryInterval = window.setInterval(renderTelemetry, 3500);
};

const stopTelemetry = () => {
  if (!state.telemetryInterval) return;
  window.clearInterval(state.telemetryInterval);
  state.telemetryInterval = null;
};

const updateScene = (sceneKey) => {
  const scene = showroomScenes[sceneKey];
  if (!scene) return;
  state.showroomScene = sceneKey;
  sceneButtons.forEach((btn) => {
    const isActive = btn.dataset.scene === sceneKey;
    btn.classList.toggle('is-active', isActive);
  });
  sceneTitle.textContent = scene.label;
  sceneDescription.innerHTML = scene.description;
  sceneLighting.textContent = scene.lighting;
  sceneHighlights.innerHTML = '';
  scene.highlights.forEach((highlight) => {
    const li = document.createElement('li');
    li.textContent = highlight;
    sceneHighlights.appendChild(li);
  });
  themePreview.style.setProperty('--scene-hue', scene.hue);
};

const refreshSceneCount = () => {
  sceneCount.textContent = Object.keys(showroomScenes).length.toString();
};

const updateTourProgress = () => {
  tourProgress.textContent = `${state.tourCount} visiteur${
    state.tourCount > 1 ? 's' : ''
  } guidé${state.tourCount > 1 ? 's' : ''} aujourd'hui`;
};

const setOfflineMode = (enabled, options = {}) => {
  const { silent = false } = options;
  state.offlineMode = enabled;
  offlineIndicator.textContent = enabled ? 'Offline Ready' : 'Online';
  conciergeStatus.textContent = enabled ? 'Concierge AI (hors-ligne)' : 'Concierge AI';
  ctaButtons.toggleOffline.textContent = enabled ? 'Revenir en ligne' : 'Mode hors ligne';
  if (!silent) {
    showToast(enabled ? 'Mode hors ligne activé avec cache showroom.' : 'Connexion rétablie.');
  }
};

const updateThemePreview = () => {
  const hue = Number(lightingHue.value);
  themePreview.style.setProperty('--theme-hue', hue);
  themePreview.style.background = `linear-gradient(135deg, hsl(${hue}, 78%, 58%), hsl(${hue}, 70%, 42%))`;
  lightingHueValue.textContent = `${hue}°`;
};

const renderFleetMap = () => {
  if (!fleetMap) return;
  fleetMap.innerHTML = '';
  fleetSystems.forEach((system) => {
    const marker = document.createElement('span');
    marker.className = `fleet-marker fleet-marker--${system.status}`;
    marker.style.setProperty('--x', `${system.coords[0]}%`);
    marker.style.setProperty('--y', `${system.coords[1]}%`);
    marker.textContent = system.asset;
    marker.title = `${system.asset} – ${system.site}`;
    fleetMap.appendChild(marker);
  });
};

const matchesFilter = (system) => {
  const filterMatch =
    state.fleetFilter === 'all' ? true : system.status === state.fleetFilter;
  const searchText = state.fleetSearch.trim().toLowerCase();
  if (!searchText) return filterMatch;
  const haystack = `${system.asset} ${system.site} ${system.profile} ${system.firmware}`.toLowerCase();
  return filterMatch && haystack.includes(searchText);
};

const renderFleetTable = () => {
  fleetTableBody.innerHTML = '';
  const filtered = fleetSystems.filter(matchesFilter);
  filtered.forEach((system) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${system.asset}</td>
      <td>${system.site}</td>
      <td>${system.profile}</td>
      <td>${system.firmware}</td>
      <td class="status-pill status-pill--${system.status}">${
        system.alerts
      } alert${system.alerts > 1 ? 'es' : 'e'}</td>
    `;
    fleetTableBody.appendChild(row);
  });
  fleetCount.textContent = filtered.length.toString();
  const totalAlerts = filtered.reduce((sum, system) => sum + system.alerts, 0);
  securityAlerts.textContent = totalAlerts.toString();
  slaValue.textContent = filtered.some((s) => s.status === 'warning') ? '< 36h' : '< 48h';
};

const renderPlaybooks = () => {
  playbookList.innerHTML = '';
  state.playbooks.forEach((playbook, index) => {
    const container = document.createElement('div');
    container.className = 'playbook';
    container.innerHTML = `
      <h4>${playbook.title}</h4>
      <p>${playbook.description}</p>
      <button class="chip chip--mini" data-remove-playbook="${index}">Supprimer</button>
    `;
    playbookList.appendChild(container);
  });
};

const appendSupportLog = (message) => {
  const entry = document.createElement('li');
  const timestamp = new Date().toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
  });
  entry.innerHTML = `<span class="support-log__time">${timestamp}</span>${message}`;
  supportLog.prepend(entry);
};

const bindEvents = () => {
  modeButtons.forEach((button) => {
    button.addEventListener('click', () => updateMode(button.dataset.target));
  });

  profileButtons.forEach((button) => {
    button.addEventListener('click', () => {
      setPerformanceProfile(button.dataset.profile);
    });
  });

  performanceButtons.turbo.addEventListener('click', () => {
    setPerformanceProfile('turbo');
    showToast('Profil Turbo armé avec boost des courbes ventilateur.');
  });

  performanceButtons.sync.addEventListener('click', () => {
    showToast('Synchronisation des zones RGB avec le profil actif.');
  });

  if (boostRange) {
    boostRange.addEventListener('input', (event) => {
      state.boostLevel = Number(event.target.value);
      boostValue.textContent = `${state.boostLevel}%`;
      renderTelemetry();
    });
  }

  ctaButtons.maintenance.addEventListener('click', () => {
    showToast('Créneau OTA ajouté au calendrier partenaire.');
  });

  sceneButtons.forEach((button) => {
    button.addEventListener('click', () => updateScene(button.dataset.scene));
  });

  ctaButtons.startTour.addEventListener('click', () => {
    state.tourCount += 1;
    updateTourProgress();
    showToast('La visite guidée immersive démarre.');
  });

  ctaButtons.toggleOffline.addEventListener('click', () => {
    setOfflineMode(!state.offlineMode);
  });

  document.getElementById('themeUpload')?.addEventListener('change', (event) => {
    const file = event.target.files?.[0];
    themeFilename.textContent = file ? file.name : 'Aucun fichier sélectionné';
    if (file) {
      showToast(`Thème ${file.name} prêt pour la scène partenaire.`);
    }
  });

  if (lightingHue) {
    lightingHue.addEventListener('input', updateThemePreview);
  }

  fleetFilterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      state.fleetFilter = button.dataset.fleetFilter;
      fleetFilterButtons.forEach((btn) => btn.classList.remove('is-active'));
      button.classList.add('is-active');
      renderFleetTable();
    });
  });

  fleetSearchInput.addEventListener('input', (event) => {
    state.fleetSearch = event.target.value;
    renderFleetTable();
  });

  ctaButtons.openMqtt.addEventListener('click', () => {
    appendSupportLog('Console MQTT : abonnement au topic telemetry/eterna/+ confirmé.');
    showToast('Console MQTT ouverte dans un nouvel onglet sécurisé.');
  });

  ctaButtons.exportMetrics.addEventListener('click', () => {
    showToast('Export CSV des métriques lancé (Wi-Fi 7 + 10 GbE).');
  });

  ctaButtons.createPlaybook.addEventListener('click', () => {
    const newPlaybook = {
      title: `Playbook personnalisé ${state.playbooks.length + 1}`,
      description: 'Déclenchement OTA + vérification intrusion automatique.',
    };
    state.playbooks = [newPlaybook, ...state.playbooks];
    renderPlaybooks();
    showToast('Nouveau playbook ajouté au portail partenaire.');
  });

  playbookList.addEventListener('click', (event) => {
    const target = event.target;
    if (target.matches('[data-remove-playbook]')) {
      const index = Number(target.dataset.removePlaybook);
      state.playbooks.splice(index, 1);
      renderPlaybooks();
    }
  });

  ctaButtons.openSupport.addEventListener('click', () => {
    appendSupportLog('Session concierge ouverte · Analyse PSU 1% + capteurs intrusion.');
    showToast('Support concierge connecté.');
  });
};

const init = () => {
  updateMode(state.activeConcept);
  setPerformanceProfile(state.performanceProfile);
  refreshSceneCount();
  updateScene(state.showroomScene);
  updateTourProgress();
  setOfflineMode(false, { silent: true });
  updateThemePreview();
  renderFleetMap();
  renderFleetTable();
  renderPlaybooks();
  appendSupportLog('Bienvenue dans le portail EternaDream Partner.');
  securityChip.textContent = 'TPM 2.0 scellé';
  networkChip.textContent = 'Dual 10 GbE + Wi-Fi 7';
  bindEvents();
};

window.addEventListener('DOMContentLoaded', init);
