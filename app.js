/**
 * VIKAS-DRISHTI: AI-Powered MPLADS Risk Intelligence & Monitoring System
 * Client Application Logic (MoSPI SIH26102)
 */

// Global State
const state = {
  currentRole: 'DISTRICT_OFFICER',
  allProjects: [],
  activeProjectId: 'MP_SEH_CH_2024_10234',
  activeProjectData: null,
  summaryData: null,
  map: null,
  mapMarkers: [],
  charts: {}
};

// ==============================================================
// 0. DRY API CLIENT & NFR (TOASTS, LOADING)
// ==============================================================

function setGlobalLoading(isLoading) {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    if (isLoading) overlay.classList.remove('hidden');
    else overlay.classList.add('hidden');
  }
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<i class="fa-solid ${type === 'success' ? 'fa-circle-check text-emerald-500' : 'fa-circle-exclamation text-red-500'}"></i> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('fade-out');
    toast.addEventListener('animationend', () => toast.remove());
  }, 4000);
}

async function apiClient(endpoint, options = {}) {
  setGlobalLoading(true);
  try {
    const res = await fetch(endpoint, options);
    const data = await res.json();
    if (data.error) {
      showToast(data.error, 'error');
      throw new Error(data.error);
    }
    return data;
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    // Don't show toast for known expected silent errors if any, but default to show
    throw err;
  } finally {
    setGlobalLoading(false);
  }
}

// ==============================================================
// 1. INITIALIZATION & LIFECYCLE
// ==============================================================

document.addEventListener('DOMContentLoaded', () => {
  initClock();
  initRoleSelector();
  initNavigation();
  initLeafletMap();
  loadSummary();
  loadProjects();
  loadDuplicates();
  loadAuditTrail();

  // Load flagship project into Copilot by default
  openProjectCopilot('MP_SEH_CH_2024_10234', false);
});

function initClock() {
  function updateTime() {
    const now = new Date();
    const clockEl = document.getElementById('liveTime');
    if (clockEl) {
      clockEl.textContent = now.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
    }
  }
  updateTime();
  setInterval(updateTime, 1000);
}

// ==============================================================
// 2. NAVIGATION & TABS
// ==============================================================

function initNavigation() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-tab');
      switchTab(target);
    });
  });
}

function switchTab(tabId) {
  // Update nav tabs
  document.querySelectorAll('.nav-tab').forEach(t => {
    t.classList.toggle('active', t.getAttribute('data-tab') === tabId);
  });

  // Update content sections
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
  });
  const targetSection = document.getElementById(`tab-${tabId}`);
  if (targetSection) {
    targetSection.classList.add('active');
  }

  // Trigger leaflet map redraw if map was hidden
  if (tabId === 'dashboard' && state.map) {
    setTimeout(() => {
      state.map.invalidateSize();
    }, 150);
  }

  // Initialize charts for cost-payment if opened
  if (tabId === 'cost-payment') {
    initCostAndSpendCharts();
  }
}

// ==============================================================
// 3. ROLE-BASED ACCESS CONTROL (RBAC)
// ==============================================================

const ROLE_DEFINITIONS = {
  DISTRICT_OFFICER: {
    badge: 'DISTRICT OFFICER',
    info: 'Viewing District: <strong>Sehore (Madhya Pradesh)</strong>. Authorized to review risk alerts, initiate ground investigations, update field verification status, and generate dossiers.',
    canVerify: true,
    canEscalate: true
  },
  STATE_NODAL: {
    badge: 'STATE NODAL AUTHORITY',
    info: 'Viewing State: <strong>Madhya Pradesh (52 Districts)</strong>. Authorized to compare district-level risk, monitor regional trends, and review escalated alerts.',
    canVerify: true,
    canEscalate: true
  },
  MINISTRY_ADMIN: {
    badge: 'MINISTRY/ADMIN OFFICER',
    info: 'Viewing National Portfolio: <strong>MoSPI National Directorate (12,458 Works)</strong>. Full portfolio overview, trend intelligence, and multi-state compliance tracking.',
    canVerify: false,
    canEscalate: false
  },
  MP_VIEWER: {
    badge: 'MP / AUTHORIZED VIEWER',
    info: 'Viewing Constituency: <strong>Vidisha Parliamentary Constituency (Shri Ramakant Bhargava)</strong>. Permitted view of sanctioned works and citizen asset progress.',
    canVerify: false,
    canEscalate: false
  },
  ADMIN: {
    badge: 'SYSTEM ADMINISTRATOR',
    info: 'System Administrator Mode: Full governance permissions, model weight calibrations, and immutable audit trail oversight.',
    canVerify: true,
    canEscalate: true
  }
};

function initRoleSelector() {
  const selector = document.getElementById('roleSelector');
  if (!selector) return;

  selector.addEventListener('change', (e) => {
    state.currentRole = e.target.value;
    updateRoleUI();
  });
  updateRoleUI();
}

function updateRoleUI() {
  const roleConfig = ROLE_DEFINITIONS[state.currentRole] || ROLE_DEFINITIONS.DISTRICT_OFFICER;
  const badgeEl = document.getElementById('roleBadge');
  const infoEl = document.getElementById('roleInfo');

  if (badgeEl) badgeEl.textContent = roleConfig.badge;
  if (infoEl) infoEl.innerHTML = roleConfig.info;

  // Filter district if District Officer
  const distFilter = document.getElementById('districtFilter');
  if (distFilter) {
    if (state.currentRole === 'DISTRICT_OFFICER') {
      distFilter.value = 'Sehore';
    } else {
      distFilter.value = 'ALL';
    }
    filterProjects();
  }
}

// ==============================================================
// 4. DATA FETCHING & RENDERING
// ==============================================================

async function loadSummary() {
  try {
    const data = await apiClient('/api/summary');
    state.summaryData = data;

    // Update KPIs
    if (document.getElementById('kpiTotal')) {
      document.getElementById('kpiTotal').textContent = data.total_projects.toLocaleString();
      document.getElementById('kpiCritical').textContent = data.critical_risk;
      document.getElementById('kpiHigh').textContent = data.high_risk;
      document.getElementById('kpiMedium').textContent = data.medium_risk;
      document.getElementById('kpiLow').textContent = data.low_risk;
    }

    // Render Trend Chart
    if (data.trend_data) {
      initTrendChart(data.trend_data);
    }
  } catch (err) {
    // Error handled by apiClient
  }
}

async function loadProjects() {
  try {
    const data = await apiClient('/api/projects');
    state.allProjects = data.projects || [];
    renderProjectsTable(state.allProjects);
    renderMapMarkers(state.allProjects);
  } catch (err) {
    // Error handled by apiClient
  }
}

function renderProjectsTable(projects) {
  const tbody = document.getElementById('projectsTableBody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (projects.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-6 text-slate-500">No projects match the selected criteria.</td></tr>`;
    return;
  }

  projects.forEach(p => {
    const tr = document.createElement('tr');
    
    // Risk tier badge class
    let tierBadge = 'badge-low';
    if (p.risk_tier === 'CRITICAL') tierBadge = 'badge-critical';
    else if (p.risk_tier === 'HIGH') tierBadge = 'badge-high';
    else if (p.risk_tier === 'MEDIUM') tierBadge = 'badge-medium';

    // Primary signal text
    const costSig = p.signals_breakdown?.cost_anomaly?.signal || 'Cost normal';
    
    // Spend vs Progress
    const spendVsProg = `${p.funds_utilized_percent}% spend / ${p.physical_progress_percent}% work`;
    const isMismatch = (p.funds_utilized_percent - p.physical_progress_percent) > 25;

    tr.innerHTML = `
      <td>
        <div class="flex items-center gap-2">
          <span class="badge-tier ${tierBadge}">${p.risk_score}/100</span>
          <strong class="font-mono text-xs block">${p.display_id}</strong>
        </div>
      </td>
      <td>
        <div class="font-bold text-slate-900">${p.title}</div>
        <div class="text-xs text-amber-700">${p.title_hi || ''}</div>
        <div class="text-xs text-slate-500 mt-0.5"><i class="fa-solid fa-user-tie"></i> ${p.mp_name}</div>
      </td>
      <td>
        <div class="text-xs font-semibold text-slate-800">${p.village}, ${p.district}</div>
        <div class="text-xs text-slate-500">${p.state}</div>
      </td>
      <td>
        <div class="text-xs">Sanction: <strong>₹${p.sanctioned_amount_lakhs.toFixed(2)}L</strong></div>
        <div class="text-xs text-slate-700">Actual: <strong class="${p.actual_expenditure_lakhs > p.sanctioned_amount_lakhs ? 'text-red-600 font-bold' : ''}">₹${p.actual_expenditure_lakhs.toFixed(2)}L</strong></div>
      </td>
      <td>
        <div class="text-xs font-mono ${isMismatch ? 'text-red-600 font-bold' : 'text-slate-700'}">${spendVsProg}</div>
        <div class="progress-bar-bg mt-1" style="width: 100px;">
          <div class="progress-bar-fill ${isMismatch ? 'bg-red-500' : 'bg-emerald-500'}" style="width: ${p.physical_progress_percent}%;"></div>
        </div>
      </td>
      <td>
        <span class="text-xs text-slate-700">${costSig}</span>
      </td>
      <td>
        <span class="badge-pill ${p.status.includes('Required') || p.status.includes('Escalated') ? 'bg-red-100 text-red-700 font-bold' : 'bg-slate-100 text-slate-700'} text-xs">
          ${p.status}
        </span>
      </td>
      <td>
        <button class="btn btn-sm btn-outline" onclick="openProjectCopilot('${p.id}')">
          <i class="fa-solid fa-wand-magic-sparkles text-indigo-500"></i> Copilot
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function filterProjects() {
  const search = (document.getElementById('projectSearch')?.value || '').toLowerCase().trim();
  const tier = document.getElementById('tierFilter')?.value || 'ALL';
  const district = document.getElementById('districtFilter')?.value || 'ALL';

  const filtered = state.allProjects.filter(p => {
    if (tier !== 'ALL' && p.risk_tier !== tier) return false;
    if (district !== 'ALL' && p.district !== district) return false;
    if (search) {
      const matchStr = `${p.id} ${p.display_id} ${p.title} ${p.title_hi || ''} ${p.district} ${p.village} ${p.mp_name}`.toLowerCase();
      if (!matchStr.includes(search)) return false;
    }
    return true;
  });

  renderProjectsTable(filtered);
}

// ==============================================================
// 5. INTERACTIVE LEAFLET RISK MAP
// ==============================================================

function initLeafletMap() {
  const mapEl = document.getElementById('riskMap');
  if (!mapEl) return;

  // Center on Central India
  state.map = L.map('riskMap').setView([22.8, 78.5], 5);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors | MoSPI VIKAS-DRISHTI'
  }).addTo(state.map);
}

function renderMapMarkers(projects) {
  if (!state.map) return;

  // Clear existing markers
  state.mapMarkers.forEach(m => state.map.removeLayer(m));
  state.mapMarkers = [];

  projects.forEach(p => {
    if (!p.coordinates) return;

    let markerColor = '#10B981'; // Low
    if (p.risk_tier === 'CRITICAL') markerColor = '#EF4444';
    else if (p.risk_tier === 'HIGH') markerColor = '#F97316';
    else if (p.risk_tier === 'MEDIUM') markerColor = '#F59E0B';

    const circleMarker = L.circleMarker([p.coordinates.lat, p.coordinates.lng], {
      radius: p.risk_tier === 'CRITICAL' ? 12 : 9,
      fillColor: markerColor,
      color: '#FFFFFF',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.85
    }).addTo(state.map);

    const popupContent = `
      <div style="font-family: 'Inter', sans-serif; min-width: 220px;">
        <div style="font-size: 0.72rem; font-family: monospace; color: #64748B;">${p.display_id}</div>
        <strong style="font-size: 0.9rem; color: #0F172A; display: block; margin: 2px 0;">${p.title}</strong>
        <div style="font-size: 0.75rem; color: #D97706; margin-bottom: 6px;">${p.title_hi || ''}</div>
        <div style="margin: 6px 0; font-size: 0.8rem;">
          <span style="background: ${markerColor}; color: #FFFFFF; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">
            Risk: ${p.risk_score}/100 (${p.risk_tier})
          </span>
        </div>
        <div style="font-size: 0.75rem; color: #334155; margin-bottom: 4px;">
          📍 ${p.village}, ${p.district} (${p.state})
        </div>
        <div style="font-size: 0.75rem; color: #475569; margin-bottom: 8px;">
          Cost: ₹${p.actual_expenditure_lakhs.toFixed(2)}L (Sanction: ₹${p.sanctioned_amount_lakhs.toFixed(2)}L)
        </div>
        <button 
          style="background: #1E293B; color: #FFFFFF; border: none; padding: 6px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; cursor: pointer; width: 100%;"
          onclick="openProjectCopilot('${p.id}')">
          <i class="fa-solid fa-wand-magic-sparkles"></i> Open in Copilot
        </button>
      </div>
    `;

    circleMarker.bindPopup(popupContent);
    state.mapMarkers.push(circleMarker);
  });
}

// ==============================================================
// 6. AI INVESTIGATION COPILOT CONTROLLER
// ==============================================================

async function openProjectCopilot(projectId, autoSwitch = true) {
  state.activeProjectId = projectId;

  try {
    const project = await apiClient(`/api/projects/${projectId}`);
    
    state.activeProjectData = project;
    renderCopilotDossier(project);

    if (autoSwitch) {
      switchTab('copilot');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  } catch (err) {
    // Error handled by apiClient
  }
}

function renderCopilotDossier(p) {
  // Hero section
  document.getElementById('copilotTitle').textContent = p.title;
  document.getElementById('copilotTitleHi').textContent = p.title_hi || '';
  document.getElementById('copilotDisplayId').textContent = p.display_id;
  document.getElementById('copilotLocation').textContent = `Village ${p.village}, Block ${p.block || ''}, ${p.district}, ${p.state}`;
  document.getElementById('copilotMp').textContent = p.mp_name;
  document.getElementById('copilotAgency').textContent = `${p.implementing_agency} (Contractor: ${p.contractor || 'N/A'})`;

  // Score Box
  const scoreValEl = document.getElementById('copilotScoreVal');
  scoreValEl.textContent = p.risk_score;
  scoreValEl.className = `score-val text-${getTierColor(p.risk_tier)}-600`;

  const tierBadgeEl = document.getElementById('copilotTierBadge');
  tierBadgeEl.textContent = `${p.risk_tier} — ${p.risk_tier === 'CRITICAL' ? 'VERIFY' : 'REVIEW'}`;
  tierBadgeEl.className = `score-tier-badge badge-${p.risk_tier.toLowerCase()}`;

  // Multi-Signal Breakdown
  const b = p.signals_breakdown || {};
  document.getElementById('scoreCost').textContent = `${b.cost_anomaly?.score || 0} / 25`;
  document.getElementById('signalCostText').textContent = b.cost_anomaly?.signal || '';

  document.getElementById('scoreDelay').textContent = `${b.delay?.score || 0} / 20`;
  document.getElementById('signalDelayText').textContent = b.delay?.signal || '';

  document.getElementById('scoreMismatch').textContent = `${b.spend_progress_mismatch?.score || 0} / 20`;
  document.getElementById('signalMismatchText').textContent = b.spend_progress_mismatch?.signal || '';

  document.getElementById('scoreDuplicate').textContent = `${b.duplicate_possibility?.score || 0} / 15`;
  document.getElementById('signalDuplicateText').textContent = b.duplicate_possibility?.signal || '';

  document.getElementById('scoreOther').textContent = `${b.other_patterns?.score || 0} / 20`;
  document.getElementById('signalOtherText').textContent = b.other_patterns?.signal || '';

  document.getElementById('scoreTotalSummary').textContent = `${p.risk_score} / 100 (${p.risk_tier})`;

  // XAI Explanation
  document.getElementById('xaiExplanationText').textContent = `"${p.ai_explanation || 'Project parameters evaluated by AI multi-signal model.'}"`;

  // Render Verification Checklist
  renderChecklist(p.verification_checklist || []);

  // Render Payment Tranches
  renderPaymentTranches(p.payments || []);
}

function getTierColor(tier) {
  if (tier === 'CRITICAL') return 'red';
  if (tier === 'HIGH') return 'orange';
  if (tier === 'MEDIUM') return 'amber';
  return 'emerald';
}

function renderChecklist(checklist) {
  const container = document.getElementById('checklistContainer');
  if (!container) return;
  container.innerHTML = '';

  checklist.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = `checklist-item ${item.completed ? 'completed' : ''}`;
    
    div.innerHTML = `
      <div class="chk-index">${idx + 1}</div>
      <div class="chk-body">
        <div class="chk-title">${item.title}</div>
        <div class="chk-desc">${item.desc}</div>
        ${item.completed ? `<div class="chk-meta"><i class="fa-solid fa-circle-check"></i> Verified by: ${item.verified_by || 'Officer'} on ${item.timestamp || 'Today'}</div>` : ''}
      </div>
      <div>
        <button class="${item.completed ? 'btn-completed' : 'btn-verify'}" onclick="toggleChecklistStep('${item.id}')">
          ${item.completed ? '<i class="fa-solid fa-check"></i> COMPLETED' : '<i class="fa-solid fa-clipboard-check"></i> VERIFY'}
        </button>
      </div>
    `;
    container.appendChild(div);
  });
}

async function toggleChecklistStep(chkId) {
  if (!state.activeProjectData) return;

  const officerName = state.currentRole === 'DISTRICT_OFFICER' ? 'Dr. Anand Verma, IAS' : 'Authorized Officer';
  const officerRole = ROLE_DEFINITIONS[state.currentRole]?.badge || 'District Officer';

  try {
    const data = await apiClient('/api/verify-step', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: state.activeProjectData.id,
        checklist_id: chkId,
        officer_name: officerName,
        officer_role: officerRole
      })
    });

    if (data.success) {
      showToast('Checklist verification updated successfully', 'success');
      // Reload project in copilot
      await openProjectCopilot(state.activeProjectData.id, false);
      // Reload audit log
      loadAuditTrail();
      // Reload summary to reflect updated KPIs/Metrics dynamically
      loadSummary();
    }
  } catch (err) {
    // Error handled by apiClient
  }
}

async function submitOfficerAction() {
  if (!state.activeProjectData) return;

  const actionType = document.getElementById('officerActionSelect').value;
  const remarks = document.getElementById('officerRemarksInput').value || 'Administrative protocol executed.';
  const officerName = state.currentRole === 'DISTRICT_OFFICER' ? 'Dr. Anand Verma, IAS' : 'Authorized Officer';
  const officerRole = ROLE_DEFINITIONS[state.currentRole]?.badge || 'District Officer';

  try {
    const data = await apiClient('/api/action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: state.activeProjectData.id,
        action_type: actionType,
        remarks: remarks,
        officer_name: officerName,
        officer_role: officerRole
      })
    });

    if (data.success) {
      showToast(`Action Recorded. Project Status: ${data.project_status}`, 'success');
      document.getElementById('officerRemarksInput').value = '';
      await openProjectCopilot(state.activeProjectData.id, false);
      await loadProjects();
      await loadAuditTrail();
      // Reload summary to reflect updated KPIs/Metrics dynamically
      loadSummary();
    }
  } catch (err) {
    // Error handled by apiClient
  }
}

function renderPaymentTranches(payments) {
  const tbody = document.getElementById('paymentTranchesBody');
  if (!tbody) return;
  tbody.innerHTML = '';

  payments.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="font-bold">Tranche ${p.tranche}</td>
      <td class="font-mono">${p.date}</td>
      <td class="font-bold text-slate-900">₹${p.amount_lakhs.toFixed(2)} Lakhs</td>
      <td>${p.stage}</td>
      <td><span class="badge-pill bg-emerald-100 text-emerald-800 font-semibold">${p.status}</span></td>
      <td><span class="${p.anomaly !== 'None' ? 'text-red-600 font-bold' : 'text-slate-500'} text-xs">${p.anomaly}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

// ==============================================================
// 7. MULTILINGUAL DUPLICATE DETECTION MATRIX
// ==============================================================

async function loadDuplicates() {
  try {
    const data = await apiClient('/api/duplicates');
    renderDuplicatePairs(data.pairs || []);
  } catch (err) {
    // Error handled by apiClient
  }
}

function renderDuplicatePairs(pairs) {
  const container = document.getElementById('duplicatePairsContainer');
  if (!container) return;
  container.innerHTML = '';

  pairs.forEach(pair => {
    const card = document.createElement('div');
    card.className = 'dup-card';
    
    card.innerHTML = `
      <div class="dup-card-header">
        <div class="flex items-center gap-2">
          <span class="badge-pill bg-red-100 text-red-800 font-bold text-xs"><i class="fa-solid fa-triangle-exclamation"></i> POTENTIAL DUPLICATE SIGNAL</span>
          <span class="text-xs text-slate-500 font-mono">Spatial Distance: <strong>${pair.distance_km} km</strong></span>
        </div>
        <div class="dup-sim-badge">
          <i class="fa-solid fa-brain"></i> Multilingual Semantic Similarity: ${(pair.semantic_similarity * 100).toFixed(0)}%
        </div>
      </div>

      <div class="dup-comparison-grid">
        <div class="dup-box">
          <div class="dup-box-title">MPLADS PROJECT UNDER MONITORING</div>
          <div class="dup-proj-title">${pair.source_title}</div>
          <div class="dup-proj-hi">${pair.source_title_hi}</div>
          <div class="dup-meta-row">
            <span><strong>ID:</strong> ${pair.source_id}</span>
            <span><strong>Cost:</strong> ₹${pair.source_cost.toFixed(2)}L</span>
            <span><strong>Location:</strong> ${pair.source_village}, ${pair.source_district}</span>
          </div>
        </div>

        <div class="text-center font-bold text-slate-400 text-sm">
          <i class="fa-solid fa-arrow-right-arrow-left text-indigo-500 text-xl block mb-1"></i>
          VS
        </div>

        <div class="dup-box">
          <div class="dup-box-title">EXISTING ASSET IN VILLAGE / SCHEME REGISTRY</div>
          <div class="dup-proj-title">${pair.target_title}</div>
          <div class="dup-proj-hi">${pair.target_title_hi}</div>
          <div class="dup-meta-row">
            <span><strong>Scheme:</strong> ${pair.scheme}</span>
            <span><strong>Cost:</strong> ₹${pair.target_cost.toFixed(2)}L</span>
            <span><strong>Sanction:</strong> ${pair.sanction_year}</span>
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-200">
        <div class="text-xs text-slate-600">
          <strong>AI Analysis:</strong> Identical asset utility ("Community Hall" <-> "सामुदायिक भवन") located within 1.5km buffer. Officer physical de-duplication check required to ensure non-overlapping funding.
        </div>
        <button class="btn btn-sm btn-primary" onclick="openProjectCopilot('MP_SEH_CH_2024_10234')">
          Review in Copilot
        </button>
      </div>
    `;

    container.appendChild(card);
  });
}

// ==============================================================
// 8. CHARTS INITIALIZATION (Chart.js)
// ==============================================================

function initTrendChart(trendData) {
  const canvas = document.getElementById('trendChart');
  if (!canvas) return;

  if (state.charts.trend) {
    state.charts.trend.destroy();
  }

  const ctx = canvas.getContext('2d');
  state.charts.trend = new Chart(ctx, {
    type: 'line',
    data: {
      labels: trendData.months,
      datasets: [
        {
          label: 'Cost Anomalies',
          data: trendData.cost_anomalies,
          borderColor: '#EF4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          tension: 0.3,
          fill: true
        },
        {
          label: 'Project Delays',
          data: trendData.project_delays,
          borderColor: '#F97316',
          backgroundColor: 'transparent',
          tension: 0.3,
          borderDash: [5, 5]
        },
        {
          label: 'Spend-Progress Mismatches',
          data: trendData.spend_progress_mismatches,
          borderColor: '#F59E0B',
          backgroundColor: 'transparent',
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } }
      },
      scales: {
        y: { beginAtZero: true, grid: { color: '#E2E8F0' } },
        x: { grid: { display: false } }
      }
    }
  });
}

function initCostAndSpendCharts() {
  // 1. Cost Anomaly Scatter
  const scatterCanvas = document.getElementById('costScatterChart');
  if (scatterCanvas && !state.charts.costScatter) {
    const ctx = scatterCanvas.getContext('2d');
    
    // Synthetic peer points
    const normalPoints = Array.from({ length: 30 }, () => ({
      x: 18 + Math.random() * 6,
      y: 19 + Math.random() * 5
    }));

    state.charts.costScatter = new Chart(ctx, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Normal Peer Projects (n=42)',
            data: normalPoints,
            backgroundColor: '#10B981'
          },
          {
            label: 'Outlier Work (MP/SEH/CH/2024/10234)',
            data: [{ x: 22.0, y: 48.45 }],
            backgroundColor: '#EF4444',
            pointRadius: 8
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } }
        },
        scales: {
          x: { title: { display: true, text: 'Estimated Sanction (₹ Lakhs)' } },
          y: { title: { display: true, text: 'Actual Cost (₹ Lakhs)' } }
        }
      }
    });
  }

  // 2. Spend vs Progress Chart
  const spendCanvas = document.getElementById('spendProgressChart');
  if (spendCanvas && !state.charts.spendProgress) {
    const ctx = spendCanvas.getContext('2d');
    state.charts.spendProgress = new Chart(ctx, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Parity Line (Spend = Progress)',
            data: [{ x: 0, y: 0 }, { x: 50, y: 50 }, { x: 100, y: 100 }],
            type: 'line',
            borderColor: '#94A3B8',
            borderDash: [5, 5],
            fill: false,
            pointRadius: 0
          },
          {
            label: 'Community Hall (High Mismatch)',
            data: [{ x: 30, y: 75 }],
            backgroundColor: '#EF4444',
            pointRadius: 8
          },
          {
            label: 'Other Monitored Works',
            data: [{ x: 95, y: 97.7 }, { x: 45, y: 82 }, { x: 65, y: 72 }, { x: 90, y: 92 }],
            backgroundColor: '#3B82F6',
            pointRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } }
        },
        scales: {
          x: { min: 0, max: 100, title: { display: true, text: 'Physical Ground Progress (%)' } },
          y: { min: 0, max: 100, title: { display: true, text: 'Funds Utilized (%)' } }
        }
      }
    });
  }
}

// ==============================================================
// 9. AI INGESTION SIMULATOR SANDBOX
// ==============================================================

const SIMULATOR_PRESETS = {
  flagship: {
    title: "Construction of Community Hall",
    sector: "Community Infrastructure",
    location: "Sehore, Madhya Pradesh",
    est: 22.00,
    act: 48.45,
    util: 75,
    prog: 30,
    actDur: 17,
    expDur: 9,
    expProg: 85,
    advance: 68,
    dupTitle: "सामुदायिक भवन निर्माण - पिपलिया",
    dupDist: 1.4
  },
  water_ro: {
    title: "Installation of Solar-Powered Drinking Water RO Plant",
    sector: "Drinking Water & Sanitation",
    location: "Pune, Maharashtra",
    est: 18.50,
    act: 27.80,
    util: 82,
    prog: 45,
    actDur: 11,
    expDur: 5,
    expProg: 90,
    advance: 54,
    dupTitle: "Gramin Shudh Jal Yojna RO Kendra",
    dupDist: 0.8
  },
  hindi_dup: {
    title: "सामुदायिक भवन निर्माण कार्य",
    sector: "Community Infrastructure",
    location: "Ichhawar, Sehore",
    est: 20.00,
    act: 21.50,
    util: 60,
    prog: 55,
    actDur: 8,
    expDur: 8,
    expProg: 65,
    advance: 25,
    dupTitle: "Community Hall Construction Ward 4",
    dupDist: 0.5
  },
  normal_road: {
    title: "Construction of Interlocking CC Road and Drain",
    sector: "Rural Roads & Drainage",
    location: "Varanasi, Uttar Pradesh",
    est: 35.00,
    act: 34.20,
    util: 97.7,
    prog: 95,
    actDur: 8,
    expDur: 5,
    expProg: 100,
    advance: 28,
    dupTitle: "",
    dupDist: 12.0
  }
};

function loadSimulatorPreset(key) {
  const p = SIMULATOR_PRESETS[key];
  if (!p) return;

  document.getElementById('simTitle').value = p.title;
  document.getElementById('simSector').value = p.sector;
  document.getElementById('simLocation').value = p.location;
  document.getElementById('simEstCost').value = p.est;
  document.getElementById('simActCost').value = p.act;
  document.getElementById('simFundsUtil').value = p.util;
  document.getElementById('simPhysProg').value = p.prog;
  document.getElementById('simActDur').value = p.actDur;
  document.getElementById('simExpDur').value = p.expDur;
  document.getElementById('simExpProg').value = p.expProg;
  document.getElementById('simAdvancePct').value = p.advance;
  document.getElementById('simDupTitle').value = p.dupTitle;
  document.getElementById('simDupDist').value = p.dupDist;
}

async function runSimulator(e) {
  e.preventDefault();

  const payload = {
    title: document.getElementById('simTitle').value,
    sector: document.getElementById('simSector').value,
    estimated_cost_lakhs: parseFloat(document.getElementById('simEstCost').value),
    actual_expenditure_lakhs: parseFloat(document.getElementById('simActCost').value),
    funds_utilized_percent: parseFloat(document.getElementById('simFundsUtil').value),
    physical_progress_percent: parseFloat(document.getElementById('simPhysProg').value),
    expected_progress_percent: parseFloat(document.getElementById('simExpProg').value),
    duration_months: parseInt(document.getElementById('simActDur').value),
    expected_duration_months: parseInt(document.getElementById('simExpDur').value),
    payments: [{ amount_lakhs: (parseFloat(document.getElementById('simEstCost').value) * parseFloat(document.getElementById('simAdvancePct').value) / 100.0) }],
    duplicate_candidate: document.getElementById('simDupTitle').value ? {
      target_title: document.getElementById('simDupTitle').value,
      distance_km: parseFloat(document.getElementById('simDupDist').value || 5.0),
      cost_lakhs: parseFloat(document.getElementById('simEstCost').value)
    } : null
  };

  try {
    const data = await apiClient('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (data.success && data.evaluation) {
      showToast('AI Simulation Completed', 'success');
      renderSimulatorResult(data.evaluation);
    }
  } catch (err) {
    // Error handled by apiClient
  }
}

function renderSimulatorResult(ev) {
  const container = document.getElementById('simResultContainer');
  if (!container) return;
  container.classList.remove('hidden');

  let tierColor = 'red';
  if (ev.risk_tier === 'HIGH') tierColor = 'orange';
  else if (ev.risk_tier === 'MEDIUM') tierColor = 'amber';
  else if (ev.risk_tier === 'LOW') tierColor = 'emerald';

  const b = ev.signals_breakdown;

  container.innerHTML = `
    <div class="panel-card border-2 border-${tierColor}-400">
      <div class="panel-header bg-slate-900 text-white">
        <div class="panel-title text-white">
          <i class="fa-solid fa-microchip text-indigo-400"></i> AI Pipeline Ingestion Output: 
          <span class="text-${tierColor}-400 ml-2 font-mono text-xl">${ev.risk_score} / 100 (${ev.risk_tier})</span>
        </div>
        <span class="badge-pill bg-${tierColor}-500 text-white font-bold text-xs">${ev.status}</span>
      </div>
      <div class="panel-body">
        
        <div class="grid-2col gap-6 mb-4">
          <div>
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Signal Contribution Breakdown:</h4>
            <div class="space-y-2 text-sm">
              <div>Cost Anomaly: <strong>${b.cost_anomaly.score}/25</strong> — <span class="text-xs text-slate-600">${b.cost_anomaly.signal}</span></div>
              <div>Timeline Delay: <strong>${b.delay.score}/20</strong> — <span class="text-xs text-slate-600">${b.delay.signal}</span></div>
              <div>Spend-Progress Mismatch: <strong>${b.spend_progress_mismatch.score}/20</strong> — <span class="text-xs text-slate-600">${b.spend_progress_mismatch.signal}</span></div>
              <div>Multilingual Duplicate: <strong>${b.duplicate_possibility.score}/15</strong> — <span class="text-xs text-slate-600">${b.duplicate_possibility.signal}</span></div>
              <div>Other Patterns & Advance: <strong>${b.other_patterns.score}/20</strong> — <span class="text-xs text-slate-600">${b.other_patterns.signal}</span></div>
            </div>
          </div>

          <div>
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Explainable AI (XAI) Synthesis:</h4>
            <blockquote class="xai-quote text-sm">
              "${ev.ai_explanation}"
            </blockquote>
            <div class="text-xs text-slate-500 mt-2 italic">
              * ${ev.clarification}
            </div>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-slate-200">
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">Generated 5-Point Field Verification Checklist:</h4>
          <ul class="list-disc pl-5 text-xs text-slate-700 space-y-1">
            ${ev.verification_checklist.map(item => `<li><strong>${item.title}:</strong> ${item.desc}</li>`).join('')}
          </ul>
        </div>

      </div>
    </div>
  `;

  container.scrollIntoView({ behavior: 'smooth' });
}

// ==============================================================
// 10. IMMUTABLE AUDIT TRAIL
// ==============================================================

async function loadAuditTrail() {
  try {
    const data = await apiClient('/api/audit');
    renderAuditTable(data.audit_records || []);
  } catch (err) {
    // Error handled by apiClient
  }
}

function renderAuditTable(records) {
  const tbody = document.getElementById('auditTableBody');
  if (!tbody) return;
  tbody.innerHTML = '';

  records.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <div class="font-mono text-xs font-bold text-slate-800">${r.id}</div>
        <div class="text-xs text-slate-400 font-mono">${r.timestamp}</div>
      </td>
      <td class="font-bold text-slate-900">${r.officer_name}</td>
      <td><span class="badge-pill bg-slate-100 text-slate-700 text-xs">${r.officer_role}</span></td>
      <td class="font-mono text-xs">${r.project_id}</td>
      <td><span class="badge-pill bg-indigo-50 text-indigo-700 font-semibold text-xs">${r.decision_category}</span></td>
      <td class="text-xs text-slate-700">
        <strong>${r.action}:</strong> ${r.details}
      </td>
      <td>
        <code class="text-xs text-slate-500 font-mono" title="${r.sha256_hash}">
          ${r.sha256_hash ? r.sha256_hash.substring(0, 14) + '...' : 'N/A'}
        </code>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// ==============================================================
// 11. PRINTABLE OFFICIAL DOSSIER EXPORT
// ==============================================================

function printOfficialDossier() {
  const p = state.activeProjectData;
  if (!p) return;

  const modal = document.getElementById('dossierPrintModal');
  const body = document.getElementById('printableDossierBody');
  if (!modal || !body) return;

  const b = p.signals_breakdown || {};
  const completedChecks = (p.verification_checklist || []).filter(c => c.completed).length;
  const totalChecks = (p.verification_checklist || []).length;

  body.innerHTML = `
    <div style="text-align: center; border-bottom: 2px solid #0B192C; padding-bottom: 12px; margin-bottom: 16px;">
      <div style="font-size: 0.8rem; font-weight: bold; color: #475569;">भारत सरकार | GOVERNMENT OF INDIA</div>
      <div style="font-size: 1rem; font-weight: bold; color: #0B192C;">सांख्यिकी और कार्यक्रम कार्यान्वयन मंत्रालय</div>
      <div style="font-size: 0.85rem; color: #0B192C;">MINISTRY OF STATISTICS & PROGRAMME IMPLEMENTATION (MoSPI)</div>
      <div style="margin-top: 6px; font-size: 1.1rem; font-weight: 800; color: #1E293B;">
        MPLADS FORMAL RISK VERIFICATION DOSSIER
      </div>
      <div style="font-size: 0.75rem; color: #64748B;">Generated via VIKAS-DRISHTI AI Analytical Intelligence Layer</div>
    </div>

    <table style="width: 100%; font-size: 0.82rem; margin-bottom: 16px; border-collapse: collapse;">
      <tr>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC; width: 25%;"><strong>Project Display ID:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; font-family: monospace; font-weight: bold;">${p.display_id}</td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC; width: 25%;"><strong>Priority Risk Score:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; font-weight: bold; color: #EF4444;">${p.risk_score} / 100 (${p.risk_tier})</td>
      </tr>
      <tr>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC;"><strong>Work Description:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1;">${p.title} (${p.title_hi || ''})</td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC;"><strong>Constituency & MP:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1;">${p.mp_name}</td>
      </tr>
      <tr>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC;"><strong>Location:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1;">Village ${p.village}, District ${p.district}, ${p.state}</td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC;"><strong>Current Administrative Status:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; font-weight: bold;">${p.status}</td>
      </tr>
      <tr>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC;"><strong>Sanctioned Amount:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1;">₹${p.sanctioned_amount_lakhs.toFixed(2)} Lakhs</td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC;"><strong>Actual Expenditure to Date:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; font-weight: bold; color: #B91C1C;">₹${p.actual_expenditure_lakhs.toFixed(2)} Lakhs (+120.2%)</td>
      </tr>
      <tr>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC;"><strong>Physical Progress:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1;">${p.physical_progress_percent}% (Expected: ${p.expected_progress_percent}%)</td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; background: #F8FAFC;"><strong>Financial Utilization:</strong></td>
        <td style="padding: 4px 8px; border: 1px solid #CBD5E1; font-weight: bold;">${p.funds_utilized_percent}% (Mismatch: +${(p.funds_utilized_percent - p.physical_progress_percent).toFixed(0)}%)</td>
      </tr>
    </table>

    <div style="background: #EEF2FF; border-left: 4px solid #6366F1; padding: 10px 14px; font-size: 0.82rem; margin-bottom: 16px;">
      <strong>Explainable AI Summary:</strong> ${p.ai_explanation}
    </div>

    <div style="font-size: 0.85rem; font-weight: bold; color: #0B192C; margin-bottom: 6px;">
      FIELD VERIFICATION CHECKPOINTS STATUS (${completedChecks} / ${totalChecks} Completed):
    </div>

    <table style="width: 100%; font-size: 0.78rem; border-collapse: collapse; margin-bottom: 20px;">
      <thead>
        <tr style="background: #F1F5F9;">
          <th style="padding: 6px; border: 1px solid #CBD5E1; text-align: left;">Checkpoint</th>
          <th style="padding: 6px; border: 1px solid #CBD5E1; text-align: left;">Verification Scope</th>
          <th style="padding: 6px; border: 1px solid #CBD5E1; text-align: center; width: 120px;">Status</th>
          <th style="padding: 6px; border: 1px solid #CBD5E1; text-align: left;">Verified By / Date</th>
        </tr>
      </thead>
      <tbody>
        ${(p.verification_checklist || []).map(c => `
          <tr>
            <td style="padding: 6px; border: 1px solid #CBD5E1; font-weight: bold;">${c.title}</td>
            <td style="padding: 6px; border: 1px solid #CBD5E1;">${c.desc}</td>
            <td style="padding: 6px; border: 1px solid #CBD5E1; text-align: center; font-weight: bold; color: ${c.completed ? '#047857' : '#DC2626'};">
              ${c.completed ? '✓ COMPLETED' : '⚠ PENDING'}
            </td>
            <td style="padding: 6px; border: 1px solid #CBD5E1; font-size: 0.72rem;">
              ${c.completed ? `${c.verified_by}<br>${c.timestamp}` : '—'}
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>

    <div style="margin-top: 40px; display: flex; justify-content: space-between; font-size: 0.8rem; border-top: 1px solid #CBD5E1; padding-top: 20px;">
      <div>
        <div>______________________________________</div>
        <div style="font-weight: bold; margin-top: 4px;">Junior / Sub-Divisional Engineer</div>
        <div style="font-size: 0.72rem; color: #64748B;">Field Inspection Technical Officer</div>
      </div>
      <div style="text-align: right;">
        <div>______________________________________</div>
        <div style="font-weight: bold; margin-top: 4px;">District Collector & District Magistrate</div>
        <div style="font-size: 0.72rem; color: #64748B;">Nodal Authority, MPLADS Sehore</div>
      </div>
    </div>
  `;

  modal.classList.remove('hidden');
}

function closeDossierModal() {
  const modal = document.getElementById('dossierPrintModal');
  if (modal) modal.classList.add('hidden');
}

// Global exposure for onclick handlers
window.openProjectCopilot = openProjectCopilot;
window.toggleChecklistStep = toggleChecklistStep;
window.submitOfficerAction = submitOfficerAction;
window.filterProjects = filterProjects;
window.loadSimulatorPreset = loadSimulatorPreset;
window.runSimulator = runSimulator;
window.printOfficialDossier = printOfficialDossier;
window.closeDossierModal = closeDossierModal;
