<template>
  <div class="capital-dashboard-page">
    <div class="dashboard-wrapper">

      <!-- Nav Bar -->
      <nav class="dash-nav">
        <div class="nav-brand">
          <div class="brand-logo-sm">CF</div>
          <span>Capital Flow</span>
        </div>
        <div class="nav-title">Painel Open Finance (Pluggy)</div>
        <div class="nav-actions">
          <q-btn
            icon="refresh"
            label="Sincronizar Banco"
            no-caps
            unelevated
            class="primary-gradient-btn"
            :loading="conectando || carregandoWidget"
            @click="abrirPluggy"
          />
          <q-btn
            flat
            round
            icon="logout"
            class="logout-btn"
            @click="sair"
          >
            <q-tooltip>Sair</q-tooltip>
          </q-btn>
        </div>
      </nav>

      <!-- Empty State -->
      <div v-if="!resultado && !conectando" class="empty-state">
        <div class="empty-icon">
          <q-icon name="account_balance" size="3rem" />
        </div>
        <h2>Nenhum dado sincronizado</h2>
        <p>Clique em "Sincronizar Banco" para emitir sua avaliação de crédito baseada no fluxo de caixa atual via Pluggy.</p>
        <div class="row justify-center q-gutter-sm">
          <q-btn
            label="Sincronizar via Pluggy"
            icon="account_balance"
            no-caps
            unelevated
            class="primary-gradient-btn"
            @click="abrirPluggy"
            :loading="carregandoWidget"
          />
          <q-btn
            label="Simular"
            icon="terminal"
            no-caps
            outline
            color="white"
            @click="simularAnalise"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="conectando" class="loading-state">
        <q-spinner-orbit color="primary" size="4em" />
        <h2>Mapeando transações...</h2>
        <p>Analisando o fluxo de caixa com o motor de risco.</p>
      </div>

      <!-- Results -->
      <div v-if="resultado && !conectando" class="results-grid">

        <!-- Score Panel -->
        <div class="score-panel">
          <div class="panel-badge">Score de Crédito</div>

          <div class="score-circle">
            <span>Score</span>
            <strong>{{ resultado.score }}</strong>
          </div>

          <div class="status-chip">{{ resultado.status }}</div>

          <div class="score-metrics">
            <div class="metric-row">
               <q-icon name="info" color="white" size="xs" />
               <span>Origem</span>
               <strong>{{ resultado.origem }}</strong>
            </div>
            <div class="metric-row">
              <q-icon name="trending_up" color="green-4" size="xs" />
              <span>Receitas</span>
              <strong>{{ resultado.detalhes.renda_calculada }}</strong>
            </div>
            <div class="metric-row">
              <q-icon name="trending_down" color="red-4" size="xs" />
              <span>Despesas</span>
              <strong>{{ resultado.detalhes.despesa_calculada }}</strong>
            </div>
            <div class="metric-row">
              <q-icon name="analytics" color="blue-4" size="xs" />
              <span>Transações</span>
              <strong>{{ resultado.detalhes.qtd_transacoes_analisadas }}</strong>
            </div>
          </div>

          <q-btn
            label="Atualizar análise"
            icon="refresh"
            no-caps
            outline
            class="refresh-btn full-width q-mt-sm"
            :loading="conectando || carregandoWidget"
            @click="abrirPluggy"
          />
        </div>

        <!-- Right column -->
        <div class="right-col">

          <!-- AI Analysis -->
          <div v-if="resultado.analise_ia" class="ai-panel q-mb-md">
            <div class="ai-header">
              <div class="panel-badge">
                <q-icon name="auto_awesome" size="xs" class="q-mr-xs" />
                Análise AI
              </div>
            </div>
            <p class="ai-texto">{{ resultado.analise_ia }}</p>
          </div>

          <!-- Table Panel -->
          <div class="table-panel">
            <div class="panel-badge q-mb-md">Extrato Analisado</div>

            <q-table
              :rows="resultado.transacoes"
              :columns="colunas"
              row-key="data"
              :pagination="{ rowsPerPage: 10 }"
              flat
              class="dark-table"
            >
              <template v-slot:body-cell-valor="props">
                <q-td :props="props" :class="props.row.tipo === 'PIX_RECEBIDO' || props.row.tipo === 'TED_RECEBIDO' ? 'valor-positivo' : 'valor-negativo'">
                  {{ props.row.tipo === 'PIX_RECEBIDO' || props.row.tipo === 'TED_RECEBIDO' ? '+' : '-' }} R$ {{ Number(props.row.valor).toFixed(2) }}
                </q-td>
              </template>

              <template v-slot:body-cell-tipo="props">
                <q-td :props="props">
                  <span :class="'tipo-badge tipo-' + (['PIX_RECEBIDO','TED_RECEBIDO'].includes(props.row.tipo) ? 'entrada' : 'saida')">
                    {{ props.row.tipo.replace(/_/g, ' ') }}
                  </span>
                </q-td>
              </template>
            </q-table>
          </div>

        </div>

      </div>

    </div>

    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const conectando = ref(false)
const carregandoWidget = ref(false)
const resultado = ref(null)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const colunas = [
  { name: 'data', align: 'left', label: 'Data', field: 'data', sortable: true },
  { name: 'descricao', align: 'left', label: 'Descrição', field: 'descricao', sortable: true },
  { name: 'tipo', align: 'center', label: 'Tipo', field: 'tipo' },
  { name: 'valor', align: 'right', label: 'Valor', field: 'valor', sortable: true },
]

const token = () => localStorage.getItem('token')

const abrirPluggy = async () => {
  if (!token()) { router.push('/login'); return; }
  carregandoWidget.value = true
  try {
    const { data } = await axios.get(`${API_URL}/api/pluggy/token/`, {
      headers: { Authorization: `Token ${token()}` }
    })

    const pluggyConnect = new PluggyConnect({
      connectToken: data.accessToken,
      includeSandbox: true,
      onSuccess: (itemData) => {
        analisarComPluggy(itemData.item.id);
      },
      onError: (error) => {
        console.error('Erro no widget Pluggy:', error);
        alert('Erro ao conectar com o banco.');
      }
    });

    pluggyConnect.init();
  } catch (error) {
    console.error('Erro ao abrir Pluggy:', error);
    if (error.response?.status === 401) router.push('/login');
    else alert('Erro ao iniciar conexão com a Pluggy.');
  } finally {
    carregandoWidget.value = false
  }
}

const analisarComPluggy = async (itemId) => {
  conectando.value = true
  try {
    const resp = await axios.post(
      `${API_URL}/api/analisar/`,
      { item_id: itemId },
      { headers: { Authorization: `Token ${token()}` } }
    )
    resultado.value = resp.data
  } catch (error) {
    console.error(error)
    if (error.response?.status === 401) router.push('/login');
    else alert('Erro ao analisar os dados da conta.')
  } finally {
    conectando.value = false
  }
}

const simularAnalise = async () => {
  if (!token()) { router.push('/login'); return; }
  conectando.value = true
  resultado.value = null
  try {
    const resp = await axios.post(
      `${API_URL}/api/analisar/`,
      { mock: true },
      { headers: { Authorization: `Token ${token()}` } }
    )
    setTimeout(() => {
      resultado.value = resp.data
      conectando.value = false
    }, 1000)
  } catch (error) {
    console.error('Erro na simulação:', error)
    if (error.response?.status === 401) router.push('/login');
    else alert('Erro ao simular análise.')
    conectando.value = false
  }
}

const sair = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  if (!token()) router.push('/login')
})
</script>

<style scoped>
.capital-dashboard-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.38), transparent 35%),
    radial-gradient(circle at bottom right, rgba(22, 163, 74, 0.22), transparent 35%),
    linear-gradient(135deg, #020617, #0f172a);
}

.dashboard-wrapper {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px;
}

/* Nav */
.dash-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding: 14px 22px;
  border-radius: 20px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.18);
  backdrop-filter: blur(14px);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
  font-weight: 800;
  font-size: 1rem;
}

.brand-logo-sm {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, #2563eb, #22c55e);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 0.9rem;
  color: white;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
  flex-shrink: 0;
}

.nav-title {
  color: #94a3b8;
  font-size: 0.88rem;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logout-btn {
  color: #94a3b8 !important;
}

/* Empty / Loading states */
.empty-state,
.loading-state {
  text-align: center;
  padding: 80px 24px;
  color: white;
}

.empty-icon {
  width: 100px;
  height: 100px;
  border-radius: 28px;
  background: rgba(37, 99, 235, 0.14);
  border: 1px solid rgba(96, 165, 250, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  color: #60a5fa;
}

.empty-state h2,
.loading-state h2 {
  font-size: 1.55rem;
  font-weight: 800;
  margin: 0 0 10px;
}

.empty-state p,
.loading-state p {
  color: #94a3b8;
  font-size: 0.98rem;
  margin: 0 0 28px;
}

/* Results grid */
.results-grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 22px;
  align-items: start;
}

.right-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* AI Analysis */
.ai-panel {
  padding: 22px;
  border-radius: 20px;
  background: rgba(37, 99, 235, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.28);
  backdrop-filter: blur(14px);
}

.ai-header {
  margin-bottom: 14px;
}

.ai-texto {
  color: #cbd5e1;
  line-height: 1.7;
  font-size: 0.95rem;
  margin: 0;
}

/* Score panel */
.score-panel {
  padding: 26px;
  border-radius: 24px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.18);
  backdrop-filter: blur(14px);
  text-align: center;
  color: white;
}

.panel-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.16);
  border: 1px solid rgba(96, 165, 250, 0.35);
  color: #bfdbfe;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 22px;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background:
    radial-gradient(circle, rgba(15, 23, 42, 0.95) 54%, transparent 55%),
    conic-gradient(#22c55e 0deg, #2563eb 260deg, rgba(148, 163, 184, 0.18) 260deg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto 18px;
}

.score-circle span {
  color: #94a3b8;
  font-size: 0.8rem;
  font-weight: 700;
}

.score-circle strong {
  font-size: 2.6rem;
  font-weight: 900;
  line-height: 1;
}

.status-chip {
  display: inline-block;
  padding: 8px 18px;
  border-radius: 12px;
  font-weight: 800;
  font-size: 0.9rem;
  margin-bottom: 22px;
  background: rgba(34, 197, 94, 0.14);
  border: 1px solid rgba(34, 197, 94, 0.32);
  color: #86efac;
}

.score-metrics {
  text-align: left;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(148, 163, 184, 0.1);
  margin-bottom: 18px;
}

.metric-row {
  display: grid;
  grid-template-columns: 18px 1fr auto;
  align-items: center;
  gap: 8px;
  color: #94a3b8;
  padding: 8px 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.08);
  font-size: 0.84rem;
}

.metric-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.metric-row strong {
  color: white;
  font-weight: 700;
}

.refresh-btn {
  min-height: 40px;
  border-radius: 12px;
  font-weight: 700;
  color: #60a5fa !important;
  border-color: rgba(96, 165, 250, 0.35) !important;
}

/* Table panel */
.table-panel {
  padding: 24px;
  border-radius: 24px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.18);
  backdrop-filter: blur(14px);
  overflow: hidden;
}

.dark-table {
  background: transparent !important;
  color: #e2e8f0;
}

.dark-table :deep(thead tr th) {
  background: rgba(255, 255, 255, 0.04);
  color: #94a3b8;
  font-weight: 700;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}

.dark-table :deep(tbody tr td) {
  color: #cbd5e1;
  border-bottom: 1px solid rgba(148, 163, 184, 0.06);
}

.dark-table :deep(tbody tr:hover td) {
  background: rgba(255, 255, 255, 0.03);
}

.dark-table :deep(.q-table__bottom) {
  background: transparent;
  color: #94a3b8;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.dark-table :deep(.q-table__bottom .q-btn) {
  color: #94a3b8;
}

.valor-positivo {
  color: #86efac !important;
  font-weight: 700;
}

.valor-negativo {
  color: #fca5a5 !important;
  font-weight: 700;
}

.tipo-badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 700;
}

.tipo-entrada {
  background: rgba(34, 197, 94, 0.14);
  color: #86efac;
  border: 1px solid rgba(34, 197, 94, 0.28);
}

.tipo-saida {
  background: rgba(239, 68, 68, 0.1);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.22);
}

/* Primary btn */
.primary-gradient-btn {
  min-height: 40px;
  padding: 0 20px;
  border-radius: 12px;
  font-weight: 800;
  color: white !important;
  background: linear-gradient(135deg, #2563eb, #16a34a);
  box-shadow: 0 10px 26px rgba(37, 99, 235, 0.28);
}

/* Blobs */
.blob {
  position: fixed;
  border-radius: 50%;
  filter: blur(110px);
  z-index: 0;
  animation: float 10s ease-in-out infinite;
  pointer-events: none;
}

.blob-1 {
  top: -10%;
  left: -8%;
  width: 500px;
  height: 500px;
  background: rgba(37, 99, 235, 0.18);
}

.blob-2 {
  bottom: -18%;
  right: -10%;
  width: 600px;
  height: 600px;
  background: rgba(22, 163, 74, 0.16);
  animation-delay: -5s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }

  50% {
    transform: translateY(-30px) scale(1.05);
  }
}

@media (max-width: 960px) {
  .results-grid {
    grid-template-columns: 1fr;
  }

  .dash-nav {
    flex-wrap: wrap;
    gap: 10px;
  }

  .nav-title {
    display: none;
  }
}

@media (max-width: 520px) {
  .dashboard-wrapper {
    padding: 14px;
    
  }

  .dash-nav {
    padding: 12px 16px;
  }
}
</style>
