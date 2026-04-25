<template>
  <q-layout view="lHh Lpr lFf">
  <q-page-container>
  <q-page class="dash-page">
    <div class="grid-overlay"></div>

    <!-- Nav Bar -->
    <nav class="dash-nav">
      <div class="nav-brand">
        <div class="brand-logo-sm">CF</div>
        <div>
          <div class="brand-name">Capital Flow</div>
          <div class="brand-sub">Open Finance</div>
        </div>
      </div>

      <div v-if="cpfMascarado" class="nav-user">
        <q-icon name="person" size="xs" class="q-mr-xs" />
        {{ cpfMascarado }}
      </div>

      <div class="nav-actions">
        <q-btn
          v-if="isStaff"
          icon="admin_panel_settings"
          label="Admin"
          no-caps
          unelevated
          class="admin-btn"
          to="/superadmin"
        />
        <q-btn
          icon="sync"
          label="Atualizar"
          no-caps
          unelevated
          class="sync-btn"
          :loading="carregando"
          @click="analisar"
        />
        <q-btn flat round icon="logout" class="logout-btn" @click="sair">
          <q-tooltip>Sair</q-tooltip>
        </q-btn>
      </div>
    </nav>

    <!-- Loading -->
    <div v-if="carregando && !resultado" class="hero-loading">
      <div class="loading-ring"></div>
      <div class="loading-text">
        <h2>Analisando seu perfil</h2>
        <p>Processando transações com IA...</p>
      </div>
    </div>

    <!-- Dashboard content -->
    <div v-if="resultado && !carregando" class="dash-content">

      <!-- Score hero -->
      <div class="score-hero">
        <div class="score-left">

          <div class="score-gauge-wrap">
            <svg viewBox="0 0 220 130" class="score-svg">
              <defs>
                <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#ef4444"/>
                  <stop offset="40%" stop-color="#f59e0b"/>
                  <stop offset="100%" stop-color="#22c55e"/>
                </linearGradient>
                <filter id="glow">
                  <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                  <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>
              <!-- Track -->
              <path d="M 20 105 A 90 90 0 0 1 200 105"
                fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="14" stroke-linecap="round"/>
              <!-- Value arc -->
              <path d="M 20 105 A 90 90 0 0 1 200 105"
                fill="none" stroke="url(#gaugeGrad)" stroke-width="14" stroke-linecap="round"
                filter="url(#glow)"
                :stroke-dasharray="283"
                :stroke-dashoffset="gaugeOffset"
                style="transition: stroke-dashoffset 1.2s cubic-bezier(0.34,1.56,0.64,1);"/>
              <!-- Score -->
              <text x="110" y="84" text-anchor="middle" font-size="38" font-weight="900"
                fill="white" font-family="sans-serif">{{ resultado.score }}</text>
              <text x="110" y="102" text-anchor="middle" font-size="11" fill="#64748b"
                font-family="sans-serif" font-weight="600">PONTOS DE 1000</text>
            </svg>

            <!-- Status badge -->
            <div :class="['score-status', 'status-' + resultado.cor]">
              <span class="status-dot"></span>
              {{ resultado.status }}
            </div>
          </div>

        </div>

        <!-- Metric cards -->
        <div class="metrics-grid">
          <div class="metric-card metric-income">
            <div class="mc-icon">
              <q-icon name="trending_up" size="sm"/>
            </div>
            <div class="mc-body">
              <div class="mc-label">Receitas</div>
              <div class="mc-value">{{ resultado.detalhes.renda_calculada }}</div>
            </div>
          </div>

          <div class="metric-card metric-expense">
            <div class="mc-icon">
              <q-icon name="trending_down" size="sm"/>
            </div>
            <div class="mc-body">
              <div class="mc-label">Despesas</div>
              <div class="mc-value">{{ resultado.detalhes.despesa_calculada }}</div>
            </div>
          </div>

          <div class="metric-card metric-txn">
            <div class="mc-icon">
              <q-icon name="receipt_long" size="sm"/>
            </div>
            <div class="mc-body">
              <div class="mc-label">Transações</div>
              <div class="mc-value">{{ resultado.detalhes.qtd_transacoes_analisadas }}</div>
            </div>
          </div>

          <!-- AI Analysis card -->
          <div v-if="resultado.analise_ia" class="metric-card metric-ai">
            <div class="ai-icon-wrap">
              <q-icon name="auto_awesome" size="sm"/>
            </div>
            <div class="ai-badge-label">Análise IA · AWS Bedrock</div>
            <p class="ai-text">{{ resultado.analise_ia }}</p>
          </div>
        </div>
      </div>

      <!-- Transaction Table -->
      <div class="txn-panel">
        <div class="txn-header">
          <div class="section-label">
            <q-icon name="account_balance_wallet" size="xs" class="q-mr-xs"/>
            Extrato Analisado
          </div>
          <div class="txn-count">{{ resultado.transacoes.length }} transações</div>
        </div>

        <q-table
          :rows="resultado.transacoes"
          :columns="colunas"
          row-key="data"
          :pagination="{ rowsPerPage: 12 }"
          flat
          class="dark-table"
        >
          <template v-slot:body-cell-valor="props">
            <q-td :props="props"
              :class="['PIX_RECEBIDO','TED_RECEBIDO'].includes(props.row.tipo) ? 'val-pos' : 'val-neg'">
              {{ ['PIX_RECEBIDO','TED_RECEBIDO'].includes(props.row.tipo) ? '+' : '−' }}
              R$ {{ Number(props.row.valor).toFixed(2) }}
            </q-td>
          </template>
          <template v-slot:body-cell-tipo="props">
            <q-td :props="props">
              <span :class="'tipo-chip tipo-' + (['PIX_RECEBIDO','TED_RECEBIDO'].includes(props.row.tipo) ? 'in' : 'out')">
                {{ props.row.tipo.replace(/_/g, ' ') }}
              </span>
            </q-td>
          </template>
        </q-table>
      </div>

    </div>

    <!-- Blobs -->
    <div class="blob b1"></div>
    <div class="blob b2"></div>
    <div class="blob b3"></div>
  </q-page>
  </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const carregando = ref(true)
const resultado = ref(null)
const isStaff = ref(false)
const cpfMascarado = ref('')

const API_URL = process.env.API_URL

const colunas = [
  { name: 'data',      align: 'left',  label: 'Data',      field: 'data',      sortable: true },
  { name: 'descricao', align: 'left',  label: 'Descrição', field: 'descricao', sortable: true },
  { name: 'tipo',      align: 'center',label: 'Tipo',       field: 'tipo'                     },
  { name: 'valor',     align: 'right', label: 'Valor',      field: 'valor',     sortable: true },
]

const gaugeOffset = computed(() => {
  if (!resultado.value) return 283
  return 283 * (1 - resultado.value.score / 1000)
})

const token = () => localStorage.getItem('token')

const carregarPerfil = async () => {
  try {
    const resp = await axios.get(`${API_URL}/api/autenticacao/me/`, {
      headers: { Authorization: `Token ${token()}` },
    })
    isStaff.value = resp.data.is_staff
    cpfMascarado.value = resp.data.cpf
  } catch {
    // silently fail
  }
}

const analisar = async () => {
  if (!token()) { router.push('/login'); return }
  carregando.value = true
  try {
    const resp = await axios.post(
      `${API_URL}/api/analisar/`,
      {},
      { headers: { Authorization: `Token ${token()}` } },
    )
    resultado.value = resp.data
  } catch (e) {
    if (e.response?.status === 401) router.push('/login')
    console.error('Erro na análise', e)
  } finally {
    carregando.value = false
  }
}

const sair = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(async () => {
  if (!token()) { router.push('/login'); return }
  await carregarPerfil()
  analisar()
})
</script>

<style scoped>
/* ── Base ─────────────────────────────────────────────── */
.dash-page {
  min-height: 100vh;
  background:
    radial-gradient(ellipse 80% 50% at 0% 0%, rgba(14, 165, 233, 0.22), transparent),
    radial-gradient(ellipse 60% 60% at 100% 100%, rgba(20, 184, 166, 0.18), transparent),
    linear-gradient(160deg, #020817 0%, #070f1e 50%, #020c18 100%);
  position: relative;
  overflow-x: hidden;
}

.grid-overlay {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(14, 165, 233, 0.055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(14, 165, 233, 0.055) 1px, transparent 1px);
  background-size: 52px 52px;
  pointer-events: none;
  z-index: 0;
}

/* ── Nav ──────────────────────────────────────────────── */
.dash-nav {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 28px;
  border-bottom: 1px solid rgba(14, 165, 233, 0.12);
  background: rgba(2, 8, 23, 0.82);
  backdrop-filter: blur(20px);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-logo-sm {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0ea5e9, #14b8a6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 0.95rem;
  color: white;
  box-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
  flex-shrink: 0;
}

.brand-name {
  color: white;
  font-weight: 800;
  font-size: 0.95rem;
  line-height: 1.2;
}

.brand-sub {
  color: #38bdf8;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.nav-user {
  display: flex;
  align-items: center;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(14, 165, 233, 0.1);
  border: 1px solid rgba(14, 165, 233, 0.22);
  color: #7dd3fc;
  font-size: 0.82rem;
  font-weight: 600;
  font-family: monospace;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logout-btn {
  color: #475569 !important;
}

.admin-btn {
  min-height: 38px;
  padding: 0 16px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.84rem;
  color: #c4b5fd !important;
  background: rgba(139, 92, 246, 0.14) !important;
  border: 1px solid rgba(139, 92, 246, 0.3) !important;
}

.sync-btn {
  min-height: 38px;
  padding: 0 18px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.84rem;
  color: white !important;
  background: linear-gradient(135deg, #0ea5e9, #14b8a6) !important;
  box-shadow: 0 0 22px rgba(14, 165, 233, 0.35);
}

/* ── Loading ──────────────────────────────────────────── */
.hero-loading {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 73px);
  gap: 36px;
  color: white;
  text-align: center;
}

.loading-ring {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid rgba(14, 165, 233, 0.15);
  border-top-color: #0ea5e9;
  animation: spin 1s linear infinite;
  box-shadow: 0 0 30px rgba(14, 165, 233, 0.35);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text h2 {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0 0 8px;
}

.loading-text p {
  color: #475569;
  margin: 0;
  font-size: 0.95rem;
}

/* ── Content ──────────────────────────────────────────── */
.dash-content {
  position: relative;
  z-index: 2;
  max-width: 1320px;
  margin: 0 auto;
  padding: 28px 28px 40px;
}

/* ── Score Hero ───────────────────────────────────────── */
.score-hero {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  margin-bottom: 24px;
  align-items: start;
}

.score-left {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.score-gauge-wrap {
  width: 100%;
  padding: 28px 22px 22px;
  border-radius: 24px;
  background: rgba(2, 12, 30, 0.75);
  border: 1px solid rgba(14, 165, 233, 0.16);
  backdrop-filter: blur(18px);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.score-svg {
  width: 100%;
  overflow: visible;
}

.score-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 20px;
  border-radius: 14px;
  font-weight: 800;
  font-size: 0.92rem;
  margin-top: 4px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.6; transform: scale(0.85); }
}

.status-green {
  background: rgba(34, 197, 94, 0.12);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #4ade80;
}
.status-green .status-dot { background: #4ade80; }

.status-orange {
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: #fbbf24;
}
.status-orange .status-dot { background: #fbbf24; }

.status-red {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}
.status-red .status-dot { background: #f87171; }

/* ── Metric cards ─────────────────────────────────────── */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto 1fr;
  gap: 16px;
}

.metric-card {
  padding: 20px 22px;
  border-radius: 20px;
  background: rgba(2, 12, 30, 0.75);
  border: 1px solid rgba(14, 165, 233, 0.1);
  backdrop-filter: blur(18px);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: border-color 0.2s, transform 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-income {
  border-color: rgba(34, 197, 94, 0.18);
}
.metric-income .mc-icon { color: #4ade80; background: rgba(34, 197, 94, 0.12); border-color: rgba(34, 197, 94, 0.25); }
.metric-income .mc-value { color: #4ade80; }

.metric-expense {
  border-color: rgba(239, 68, 68, 0.18);
}
.metric-expense .mc-icon { color: #f87171; background: rgba(239, 68, 68, 0.12); border-color: rgba(239, 68, 68, 0.25); }
.metric-expense .mc-value { color: #f87171; }

.metric-txn {
  border-color: rgba(14, 165, 233, 0.18);
}
.metric-txn .mc-icon { color: #38bdf8; background: rgba(14, 165, 233, 0.12); border-color: rgba(14, 165, 233, 0.25); }
.metric-txn .mc-value { color: #38bdf8; }

.mc-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid;
  flex-shrink: 0;
}

.mc-label {
  color: #475569;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.mc-value {
  font-size: 1.22rem;
  font-weight: 900;
  color: white;
  line-height: 1.1;
}

/* AI card spanning all 3 columns */
.metric-ai {
  grid-column: 1 / -1;
  flex-direction: column;
  align-items: flex-start;
  padding: 22px 24px;
  border-color: rgba(139, 92, 246, 0.22);
  background: rgba(139, 92, 246, 0.06);
}

.ai-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(139, 92, 246, 0.16);
  border: 1px solid rgba(139, 92, 246, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a78bfa;
  margin-bottom: 10px;
}

.ai-badge-label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #a78bfa;
  margin-bottom: 10px;
}

.ai-text {
  color: #94a3b8;
  font-size: 0.94rem;
  line-height: 1.75;
  margin: 0;
}

/* ── Transaction Table ────────────────────────────────── */
.txn-panel {
  border-radius: 24px;
  background: rgba(2, 12, 30, 0.75);
  border: 1px solid rgba(14, 165, 233, 0.12);
  backdrop-filter: blur(18px);
  overflow: hidden;
}

.txn-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  border-bottom: 1px solid rgba(14, 165, 233, 0.08);
}

.section-label {
  display: inline-flex;
  align-items: center;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #38bdf8;
}

.txn-count {
  font-size: 0.8rem;
  color: #334155;
  font-weight: 600;
}

.dark-table {
  background: transparent !important;
}

.dark-table :deep(thead tr th) {
  background: rgba(255, 255, 255, 0.025);
  color: #334155;
  font-weight: 700;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid rgba(14, 165, 233, 0.08);
}

.dark-table :deep(tbody tr td) {
  color: #94a3b8;
  font-size: 0.88rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.dark-table :deep(tbody tr:hover td) {
  background: rgba(14, 165, 233, 0.04);
  color: #cbd5e1;
}

.dark-table :deep(.q-table__bottom) {
  background: transparent;
  color: #334155;
  border-top: 1px solid rgba(14, 165, 233, 0.08);
}

.dark-table :deep(.q-table__bottom .q-btn) {
  color: #475569;
}

.val-pos { color: #4ade80 !important; font-weight: 700; }
.val-neg { color: #f87171 !important; font-weight: 700; }

.tipo-chip {
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
}

.tipo-in {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.22);
}

.tipo-out {
  background: rgba(239, 68, 68, 0.08);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.18);
}

/* ── Blobs ────────────────────────────────────────────── */
.blob {
  position: fixed;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
  z-index: 0;
  animation: float 12s ease-in-out infinite;
}

.b1 {
  top: -15%;
  left: -10%;
  width: 550px;
  height: 550px;
  background: rgba(14, 165, 233, 0.13);
}

.b2 {
  bottom: -15%;
  right: -10%;
  width: 600px;
  height: 600px;
  background: rgba(20, 184, 166, 0.1);
  animation-delay: -6s;
}

.b3 {
  top: 30%;
  right: 20%;
  width: 350px;
  height: 350px;
  background: rgba(99, 102, 241, 0.07);
  animation-delay: -3s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50%       { transform: translateY(-28px) scale(1.04); }
}

/* ── Responsive ───────────────────────────────────────── */
@media (max-width: 1024px) {
  .score-hero {
    grid-template-columns: 240px 1fr;
  }
}

@media (max-width: 860px) {
  .score-hero {
    grid-template-columns: 1fr;
  }

  .metrics-grid {
    grid-template-columns: 1fr 1fr;
  }

  .metric-ai {
    grid-column: 1 / -1;
  }
}

@media (max-width: 600px) {
  .dash-nav {
    padding: 12px 16px;
    flex-wrap: wrap;
    gap: 10px;
  }

  .nav-user {
    display: none;
  }

  .dash-content {
    padding: 16px;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }
}
</style>
