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

const autonomyBackups = [
  {
    id: 'AUTO_BACKUP_20240419_123000',
    path: 'Eterna\\Backups\\2024-04-19_1230',
    size: '2.1 GB',
    status: 'Stable',
    timestamp: '12:30',
  },
  {
    id: 'AUTO_BACKUP_20240418_231200',
    path: 'Eterna\\Backups\\2024-04-18_2312',
    size: '1.9 GB',
    status: 'Stable',
    timestamp: '23:12',
  },
  {
    id: 'AUTO_BACKUP_20240418_092540',
    path: 'Eterna\\Backups\\2024-04-18_0925',
    size: '1.8 GB',
    status: 'Stable',
    timestamp: '09:25',
  },
];

const autonomyWatchers = [
  {
    scope: 'web/',
    focus: 'UI & front-end',
    events: '6 changements monitorés ce matin',
    status: 'healthy',
  },
  {
    scope: 'services/backend/',
    focus: 'FastAPI sandbox & orchestration',
    events: 'Tests intégration terminés',
    status: 'healthy',
  },
  {
    scope: 'models/emotion/',
    focus: 'Modèles émotionnels & intents',
    events: 'Validation requise avant déploiement',
    status: 'warning',
  },
];

const autonomyQueue = [
  {
    id: 'AUTO_PATCH_20240419_142315',
    title: 'Optimiser la visualisation des courbes ventilateur',
    scope: 'web/app.js',
    category: 'UI',
    description:
      'Lissage des interpolations SVG pour éviter les oscillations lors des boosts Turbo.',
    requiresValidation: false,
  },
  {
    id: 'AUTO_PATCH_20240419_101842',
    title: 'Renforcer la sandbox FastAPI',
    scope: 'services/backend/',
    category: 'Sécurité',
    description:
      'Ajout de restrictions de réseau et de quotas CPU avant exécution des scripts générés.',
    requiresValidation: true,
  },
  {
    id: 'AUTO_PATCH_20240418_214410',
    title: 'Actualiser le module d’analyse émotionnelle',
    scope: 'models/emotion/',
    category: 'IA',
    description:
      'Intégration des nouveaux jeux de données vocaux pour améliorer la détection d’énergie.',
    requiresValidation: true,
  },
];

const autonomyLogs = [
  {
    id: 'AUTO_PATCH_20240418_223015',
    message: 'Rollback réussi vers AUTO_BACKUP_20240418_092540 après échec test mémoire.',
    type: 'rollback',
  },
  {
    id: 'AUTO_PATCH_20240418_174200',
    message: 'Déploiement sandbox des scripts UI validé (18/18 checks).',
    type: 'success',
  },
  {
    id: 'AUTO_PATCH_20240418_081002',
    message: 'Validation manuelle requise pour patch sécurité FastAPI.',
    type: 'alert',
  },
];

const autonomySteps = [
  'observation',
  'proposition',
  'validation',
  'application',
  'verification',
  'memorisation',
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
  autonomyValidation: 'manual',
  autonomyStep: 'observation',
  emotionLevel: 48,
  sandboxState: {
    status: 'OK',
    lastRun: new Date(Date.now() - 12 * 60 * 1000),
    passed: 18,
    total: 18,
  },
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

const backupList = document.querySelector('[data-backup-list]');
const backupCountChip = document.querySelector('[data-backup-count]');
const lastBackupValue = document.querySelector('[data-last-backup]');
const lastBackupPath = document.querySelector('[data-last-backup-path]');
const validationStateValue = document.querySelector('[data-validation-state]');
const sandboxStatusValue = document.querySelector('[data-sandbox-status]');
const sandboxUpdatedValue = document.querySelector('[data-sandbox-updated]');
const sandboxScoreValue = document.querySelector('[data-sandbox-score]');
const sandboxMetaValue = document.querySelector('[data-sandbox-meta]');
const watchersList = document.querySelector('[data-watchers-list]');
const queueList = document.querySelector('[data-queue-list]');
const processNextButton = document.querySelector('[data-process-next]');
const emotionSlider = document.querySelector('[data-emotion-slider]');
const emotionLabel = document.querySelector('[data-emotion-label]');
const emotionGuidance = document.querySelector('[data-emotion-guidance]');
const autonomyLogList = document.querySelector('[data-autonomy-log]');
const exportLogsButton = document.querySelector('[data-export-logs]');
const runBackupButtons = document.querySelectorAll('[data-run-backup]');
const validationToggleButtons = document.querySelectorAll('[data-toggle-validation]');
const runSandboxButtons = document.querySelectorAll('[data-run-sandbox]');
const cycleContainer = document.querySelector('[data-cycle-steps]');

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

const padNumber = (value) => value.toString().padStart(2, '0');

const buildTimestampId = (prefix) => {
  const now = new Date();
  const datePart = `${now.getFullYear()}${padNumber(now.getMonth() + 1)}${padNumber(
    now.getDate()
  )}`;
  const timePart = `${padNumber(now.getHours())}${padNumber(now.getMinutes())}${padNumber(
    now.getSeconds()
  )}`;
  return `${prefix}_${datePart}_${timePart}`;
};

const formatRelativeTime = (date) => {
  if (!(date instanceof Date)) return '';
  const diffMs = Date.now() - date.getTime();
  const diffMinutes = Math.max(0, Math.round(diffMs / 60000));
  if (diffMinutes === 0) return "à l'instant";
  if (diffMinutes === 1) return 'il y a 1 min';
  if (diffMinutes < 60) return `il y a ${diffMinutes} min`;
  const diffHours = Math.round(diffMinutes / 60);
  return diffHours === 1 ? 'il y a 1 h' : `il y a ${diffHours} h`;
};

const setAutonomyStep = (step) => {
  if (!cycleContainer) return;
  const currentIndex = autonomySteps.indexOf(step);
  if (currentIndex === -1) return;
  state.autonomyStep = step;
  const steps = cycleContainer.querySelectorAll('.autonomy-cycle__step');
  steps.forEach((element) => {
    const elementStep = element.dataset.step;
    const elementIndex = autonomySteps.indexOf(elementStep);
    if (elementIndex === -1) return;
    element.classList.toggle('is-active', elementIndex === currentIndex);
    element.classList.toggle('is-complete', elementIndex < currentIndex);
  });
};

const updateValidationState = () => {
  if (validationStateValue) {
    validationStateValue.textContent =
      state.autonomyValidation === 'manual' ? 'Manuelle' : 'Automatique';
  }
};

const renderBackups = () => {
  if (!backupList) return;
  backupList.innerHTML = '';
  autonomyBackups.forEach((backup) => {
    const card = document.createElement('article');
    card.className = 'backup-card';
    const statusClass = backup.status === 'Stable' ? 'healthy' : 'warning';
    card.innerHTML = `
      <div class="backup-card__title">
        <h4>${backup.id}</h4>
        <p>${backup.path}</p>
      </div>
      <div class="backup-card__meta">
        <span>${backup.timestamp}</span>
        <span>${backup.size}</span>
        <span class="status-pill status-pill--${statusClass}">${backup.status}</span>
        <button class="chip chip--mini" data-restore-backup="${backup.id}">Restaurer</button>
      </div>
    `;
    backupList.appendChild(card);
  });
  if (backupCountChip) {
    backupCountChip.textContent = `${autonomyBackups.length} backups actifs`;
  }
  if (autonomyBackups[0]) {
    if (lastBackupValue) {
      lastBackupValue.textContent = autonomyBackups[0].timestamp;
    }
    if (lastBackupPath) {
      lastBackupPath.textContent = `Stocké dans ${autonomyBackups[0].path}`;
    }
  }
};

const renderWatchers = () => {
  if (!watchersList) return;
  watchersList.innerHTML = '';
  autonomyWatchers.forEach((watcher) => {
    const li = document.createElement('li');
    li.className = 'watcher';
    const statusLabel = watcher.status === 'healthy' ? 'Actif' : 'Surveillance';
    li.innerHTML = `
      <div class="watcher__title">
        <h4>${watcher.scope}</h4>
        <p>${watcher.focus}</p>
      </div>
      <div class="watcher__meta">
        <span>${watcher.events}</span>
        <span class="status-pill status-pill--${watcher.status}">${statusLabel}</span>
      </div>
    `;
    watchersList.appendChild(li);
  });
};

const renderAutonomyLogs = () => {
  if (!autonomyLogList) return;
  autonomyLogList.innerHTML = '';
  autonomyLogs.forEach((log) => {
    const li = document.createElement('li');
    li.className = `log-entry log-entry--${log.type}`;
    li.innerHTML = `
      <span class="log-entry__id">${log.id}</span>
      <span class="log-entry__message">${log.message}</span>
    `;
    autonomyLogList.appendChild(li);
  });
};

const appendAutonomyLog = (message, type = 'info', options = {}) => {
  const id = options.id ?? buildTimestampId('AUTO_PATCH');
  autonomyLogs.unshift({ id, message, type });
  if (autonomyLogs.length > 16) {
    autonomyLogs.length = 16;
  }
  renderAutonomyLogs();
};

const updateSandboxDisplay = () => {
  const { status, lastRun, passed, total } = state.sandboxState;
  if (sandboxStatusValue) {
    sandboxStatusValue.textContent = status;
  }
  if (sandboxUpdatedValue) {
    sandboxUpdatedValue.textContent = formatRelativeTime(lastRun);
  }
  if (sandboxScoreValue) {
    sandboxScoreValue.textContent = `${passed}/${total} checks`;
  }
  if (sandboxMetaValue) {
    sandboxMetaValue.textContent = `venv isolé · Tests ${passed}/${total}`;
  }
};

const createBackup = () => {
  const now = new Date();
  const id = buildTimestampId('AUTO_BACKUP');
  const path = `Eterna\\Backups\\${now.getFullYear()}-${padNumber(
    now.getMonth() + 1
  )}-${padNumber(now.getDate())}_${padNumber(now.getHours())}${padNumber(
    now.getMinutes()
  )}`;
  const newBackup = {
    id,
    path,
    size: `${(1.8 + Math.random() * 0.6).toFixed(1)} GB`,
    status: 'Stable',
    timestamp: `${padNumber(now.getHours())}:${padNumber(now.getMinutes())}`,
  };
  autonomyBackups.unshift(newBackup);
  if (autonomyBackups.length > 8) {
    autonomyBackups.pop();
  }
  renderBackups();
  appendAutonomyLog(`Backup ${id} créé et chiffré (AES-256).`, 'success', { id });
  setAutonomyStep('verification');
  showToast('Backup complet chiffré créé.');
};

const toggleValidation = () => {
  state.autonomyValidation =
    state.autonomyValidation === 'manual' ? 'auto' : 'manual';
  validationToggleButtons.forEach((button) => {
    const label =
      state.autonomyValidation === 'manual'
        ? 'Validation manuelle activée'
        : 'Validation automatique activée';
    button.textContent = label;
  });
  updateValidationState();
  renderQueue();
  appendAutonomyLog(
    `Mode de validation ${
      state.autonomyValidation === 'manual' ? 'manuel' : 'automatique'
    } activé.`,
    'info'
  );
  setAutonomyStep(state.autonomyValidation === 'manual' ? 'validation' : 'application');
};

const renderQueue = () => {
  if (!queueList) return;
  queueList.innerHTML = '';
  let pendingCritical = false;
  autonomyQueue.forEach((task) => {
    if (task.requiresValidation && state.autonomyValidation === 'auto') {
      task.approved = true;
    }
    if (task.requiresValidation && !task.approved) {
      pendingCritical = true;
    }
    const li = document.createElement('li');
    li.className = 'queue-item';
    const statusClass = task.requiresValidation ? 'warning' : 'healthy';
    const canExecute = !task.requiresValidation || task.approved || state.autonomyValidation === 'auto';
    const applyLabel = canExecute ? 'Appliquer' : 'En attente validation';
    li.innerHTML = `
      <header class="queue-item__header">
        <span class="queue-item__title">${task.title}</span>
        <span class="status-pill status-pill--${statusClass}">${task.category}</span>
      </header>
      <p>${task.description}</p>
      <div class="queue-item__meta">
        <span>${task.id}</span>
        <span>${task.scope}</span>
      </div>
      <div class="queue-item__actions">
        ${
          task.requiresValidation
            ? `<button class="chip chip--mini${
                task.approved ? ' is-affirmed' : ''
              }" data-approve-task="${task.id}" ${
                state.autonomyValidation === 'auto' ? 'disabled' : ''
              }>${task.approved ? 'Validé' : 'Valider'}</button>`
            : ''
        }
        <button class="btn btn--secondary" data-execute-task="${task.id}" ${
          canExecute ? '' : 'disabled'
        }>${applyLabel}</button>
      </div>
    `;
    queueList.appendChild(li);
  });
  if (autonomyQueue.length === 0) {
    const empty = document.createElement('li');
    empty.className = 'queue-item queue-item--empty';
    empty.textContent = 'Aucune tâche en attente — module autonome en observation.';
    queueList.appendChild(empty);
  }
  setAutonomyStep(
    pendingCritical ? 'validation' : autonomyQueue.length ? 'proposition' : 'observation'
  );
};

const approveTask = (taskId) => {
  const task = autonomyQueue.find((item) => item.id === taskId);
  if (!task) return;
  task.approved = true;
  renderQueue();
  appendAutonomyLog(`Validation accordée pour ${task.id}.`, 'info', {
    id: task.id,
  });
};

const executeTask = (taskId) => {
  const index = autonomyQueue.findIndex((item) => item.id === taskId);
  if (index === -1) return;
  const [task] = autonomyQueue.splice(index, 1);
  renderQueue();
  appendAutonomyLog(
    `Exécution du patch ${task.id} (${task.scope}) dans la sandbox locale.`,
    'success',
    { id: task.id }
  );
  setAutonomyStep('application');
  showToast(`Patch ${task.id} lancé en sandbox.`);
};

const processNextTask = () => {
  const nextTask = autonomyQueue.find(
    (task) => !task.requiresValidation || task.approved || state.autonomyValidation === 'auto'
  );
  if (!nextTask) {
    showToast('Aucune tâche prêtes à être appliquée.');
    return;
  }
  executeTask(nextTask.id);
};

const restoreBackup = (backupId) => {
  const backup = autonomyBackups.find((item) => item.id === backupId);
  if (!backup) return;
  appendAutonomyLog(
    `Restauration automatique depuis ${backup.id} en cours.`,
    'rollback',
    { id: backup.id }
  );
  setAutonomyStep('application');
  showToast(`Restauration ${backup.id} programmée.`);
};

const updateEmotionState = (value) => {
  state.emotionLevel = value;
  if (emotionLabel) {
    if (value < 35) {
      emotionLabel.textContent = 'Calme';
    } else if (value < 70) {
      emotionLabel.textContent = 'Focus neutre';
    } else {
      emotionLabel.textContent = 'Énergie haute';
    }
  }
  if (emotionGuidance) {
    if (value < 35) {
      emotionGuidance.textContent =
        'Eterna privilégie la stabilité et retarde les patchs expérimentaux.';
    } else if (value < 70) {
      emotionGuidance.textContent =
        'Priorisation équilibrée entre innovation et stabilité.';
    } else {
      emotionGuidance.textContent =
        'Les améliorations audacieuses sont favorisées, avec surveillance renforcée.';
    }
  }
};

const runSandboxTest = () => {
  const now = new Date();
  const passed = 16 + Math.floor(Math.random() * 3);
  const total = state.sandboxState.total;
  const success = passed >= 17;
  state.sandboxState = {
    status: success ? 'OK' : 'Alerte',
    lastRun: now,
    passed,
    total,
  };
  updateSandboxDisplay();
  appendAutonomyLog(
    success
      ? `Sandbox FastAPI validée (${passed}/${total} checks).`
      : `Sandbox FastAPI a détecté ${total - passed} anomalies.`,
    success ? 'success' : 'alert'
  );
  setAutonomyStep(success ? 'verification' : 'validation');
  showToast(success ? 'Sandbox validée.' : 'Sandbox en attente de correction.');
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

  runBackupButtons.forEach((button) => {
    button.addEventListener('click', createBackup);
  });

  validationToggleButtons.forEach((button) => {
    button.addEventListener('click', toggleValidation);
  });

  runSandboxButtons.forEach((button) => {
    button.addEventListener('click', runSandboxTest);
  });

  processNextButton?.addEventListener('click', processNextTask);

  queueList?.addEventListener('click', (event) => {
    const target = event.target;
    if (target.matches('[data-approve-task]')) {
      approveTask(target.dataset.approveTask);
    }
    if (target.matches('[data-execute-task]')) {
      executeTask(target.dataset.executeTask);
    }
  });

  backupList?.addEventListener('click', (event) => {
    const target = event.target;
    if (target.matches('[data-restore-backup]')) {
      restoreBackup(target.dataset.restoreBackup);
    }
  });

  if (emotionSlider) {
    emotionSlider.addEventListener('input', (event) => {
      updateEmotionState(Number(event.target.value));
    });
  }

  exportLogsButton?.addEventListener('click', () => {
    appendAutonomyLog('Export des logs AUTO_PATCH vers coffre sécurisé.', 'info');
    showToast('Export des journaux autonomie en cours.');
    setAutonomyStep('memorisation');
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
  renderBackups();
  renderWatchers();
  renderAutonomyLogs();
  renderQueue();
  updateValidationState();
  updateSandboxDisplay();
  updateEmotionState(state.emotionLevel);
  setAutonomyStep(state.autonomyStep);
  appendSupportLog('Bienvenue dans le portail EternaDream Partner.');
  securityChip.textContent = 'TPM 2.0 scellé';
  networkChip.textContent = 'Dual 10 GbE + Wi-Fi 7';
  bindEvents();
};

window.addEventListener('DOMContentLoaded', init);
