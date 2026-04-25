<template>
  <q-layout view="lHh Lpr lFf">
  <q-page-container>
  <q-page class="capital-admin-page">
    <div class="grid-overlay"></div>

    <div class="admin-wrapper">

      <!-- Nav -->
      <nav class="dash-nav">
        <div class="nav-brand">
          <div class="brand-logo-sm">CF</div>
          <span>Capital Flow</span>
        </div>
        <div class="nav-title">
          <span class="admin-badge-nav">
            <q-icon name="admin_panel_settings" size="xs" class="q-mr-xs" />
            Super Admin
          </span>
        </div>
        <div class="nav-actions">
          <q-btn flat no-caps icon="dashboard" label="Dashboard" class="back-btn" to="/dashboard" />
          <q-btn flat round icon="logout" class="logout-btn" @click="sair">
            <q-tooltip>Sair</q-tooltip>
          </q-btn>
        </div>
      </nav>

      <!-- Page Header -->
      <div class="page-header">
        <div>
          <h1 class="page-title">Painel de Controle</h1>
          <p class="page-sub">Visão geral de usuários e atividades da plataforma.</p>
        </div>
        <q-btn
          icon="refresh"
          no-caps
          unelevated
          label="Atualizar"
          class="primary-gradient-btn"
          :loading="carregando"
          @click="carregar"
        />
      </div>

      <!-- Error -->
      <div v-if="erro" class="error-panel q-mb-lg">
        <q-icon name="error_outline" size="sm" class="q-mr-sm" />
        {{ erro }}
      </div>

      <!-- Loading -->
      <div v-if="carregando && !dados" class="loading-state">
        <q-spinner-orbit color="primary" size="3.5em" />
        <p>Carregando dados do painel...</p>
      </div>

      <template v-if="dados">

        <!-- Stats Cards -->
        <div class="stats-row">
          <div class="stat-card">
            <div class="stat-icon stat-icon-blue">
              <q-icon name="group" size="md" />
            </div>
            <div class="stat-content">
              <div class="stat-label">Total de Usuários</div>
              <div class="stat-value">{{ dados.total_usuarios }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon stat-icon-green">
              <q-icon name="person_add" size="md" />
            </div>
            <div class="stat-content">
              <div class="stat-label">Novos este Mês</div>
              <div class="stat-value">{{ dados.novos_este_mes }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon stat-icon-purple">
              <q-icon name="shield" size="md" />
            </div>
            <div class="stat-content">
              <div class="stat-label">Administradores</div>
              <div class="stat-value">{{ totalAdmins }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon stat-icon-teal">
              <q-icon name="verified_user" size="md" />
            </div>
            <div class="stat-content">
              <div class="stat-label">Usuários Ativos</div>
              <div class="stat-value">{{ totalAtivos }}</div>
            </div>
          </div>
        </div>

        <!-- User Table -->
        <div class="table-panel">
          <div class="table-header">
            <div class="panel-badge">
              <q-icon name="manage_accounts" size="xs" class="q-mr-xs" />
              Usuários Cadastrados
            </div>
            <q-input
              v-model="filtro"
              placeholder="Buscar por CPF..."
              outlined
              dense
              class="search-input"
            >
              <template #prepend>
                <q-icon name="search" color="grey-5" />
              </template>
            </q-input>
          </div>

          <q-table
            :rows="usuariosFiltrados"
            :columns="colunas"
            row-key="id"
            :pagination="{ rowsPerPage: 15 }"
            flat
            class="dark-table"
          >
            <template v-slot:body-cell-is_staff="props">
              <q-td :props="props">
                <span :class="props.row.is_staff ? 'badge-admin' : 'badge-user'">
                  {{ props.row.is_staff ? 'Admin' : 'Usuário' }}
                </span>
              </q-td>
            </template>

            <template v-slot:body-cell-is_active="props">
              <q-td :props="props">
                <span :class="props.row.is_active ? 'badge-active' : 'badge-inactive'">
                  {{ props.row.is_active ? 'Ativo' : 'Inativo' }}
                </span>
              </q-td>
            </template>
          </q-table>
        </div>

      </template>
    </div>

    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>
  </q-page>
  </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const carregando = ref(false)
const dados = ref(null)
const erro = ref('')
const filtro = ref('')

const API_URL = process.env.API_URL
const token = () => localStorage.getItem('token')

const colunas = [
  { name: 'id', align: 'center', label: '#', field: 'id', sortable: true },
  { name: 'cpf', align: 'left', label: 'CPF', field: 'cpf', sortable: true },
  { name: 'criado_em', align: 'left', label: 'Cadastro', field: 'criado_em', sortable: true },
  { name: 'is_staff', align: 'center', label: 'Perfil', field: 'is_staff' },
  { name: 'is_active', align: 'center', label: 'Status', field: 'is_active' },
]

const totalAdmins = computed(() => dados.value?.usuarios.filter((u) => u.is_staff).length ?? 0)
const totalAtivos = computed(() => dados.value?.usuarios.filter((u) => u.is_active).length ?? 0)

const usuariosFiltrados = computed(() => {
  if (!dados.value) return []
  if (!filtro.value) return dados.value.usuarios
  const q = filtro.value.toLowerCase()
  return dados.value.usuarios.filter((u) => u.cpf.toLowerCase().includes(q))
})

const carregar = async () => {
  if (!token()) { router.push('/login'); return }
  carregando.value = true
  erro.value = ''
  try {
    const resp = await axios.get(`${API_URL}/api/admin/painel/`, {
      headers: { Authorization: `Token ${token()}` },
    })
    dados.value = resp.data
  } catch (e) {
    if (e.response?.status === 401) { router.push('/login'); return }
    if (e.response?.status === 403) {
      erro.value = 'Acesso negado. Esta área é exclusiva para administradores.'
    } else {
      erro.value = 'Erro ao carregar dados do painel.'
    }
  } finally {
    carregando.value = false
  }
}

const sair = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  if (!token()) { router.push('/login'); return }
  carregar()
})
</script>

<style scoped>
.capital-admin-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 20% 10%, rgba(139, 92, 246, 0.25), transparent 40%),
    radial-gradient(circle at 80% 90%, rgba(37, 99, 235, 0.2), transparent 40%),
    linear-gradient(135deg, #020617, #0f172a);
}

.grid-overlay {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(139, 92, 246, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 1;
}

.admin-wrapper {
  position: relative;
  z-index: 2;
  max-width: 1400px;
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
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 0.9rem;
  color: white;
  box-shadow: 0 8px 20px rgba(124, 58, 237, 0.35);
  flex-shrink: 0;
}

.nav-title {
  display: flex;
  align-items: center;
}

.admin-badge-nav {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(139, 92, 246, 0.16);
  border: 1px solid rgba(139, 92, 246, 0.35);
  color: #c4b5fd;
  font-size: 0.82rem;
  font-weight: 700;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.back-btn {
  color: #94a3b8 !important;
  font-weight: 600;
  font-size: 0.88rem;
}

.logout-btn {
  color: #94a3b8 !important;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 900;
  margin: 0 0 8px;
  background: linear-gradient(135deg, #c4b5fd, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-sub {
  color: #64748b;
  font-size: 0.96rem;
  margin: 0;
}

/* Error */
.error-panel {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-radius: 16px;
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.28);
  color: #fca5a5;
  font-weight: 600;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 80px;
  color: #94a3b8;
}

.loading-state p {
  margin-top: 18px;
  font-size: 1rem;
}

/* Stats row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 28px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 22px 24px;
  border-radius: 20px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.14);
  backdrop-filter: blur(14px);
  transition: border-color 0.2s, transform 0.2s;
}

.stat-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-2px);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon-blue {
  background: rgba(37, 99, 235, 0.18);
  color: #60a5fa;
  border: 1px solid rgba(37, 99, 235, 0.3);
}

.stat-icon-green {
  background: rgba(22, 163, 74, 0.16);
  color: #4ade80;
  border: 1px solid rgba(22, 163, 74, 0.28);
}

.stat-icon-purple {
  background: rgba(139, 92, 246, 0.16);
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.28);
}

.stat-icon-teal {
  background: rgba(20, 184, 166, 0.16);
  color: #2dd4bf;
  border: 1px solid rgba(20, 184, 166, 0.28);
}

.stat-content {
  min-width: 0;
}

.stat-label {
  color: #64748b;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 6px;
}

.stat-value {
  color: white;
  font-size: 2rem;
  font-weight: 900;
  line-height: 1;
}

/* Table panel */
.table-panel {
  padding: 26px;
  border-radius: 24px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.14);
  backdrop-filter: blur(14px);
  overflow: hidden;
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
  flex-wrap: wrap;
  gap: 12px;
}

.panel-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(139, 92, 246, 0.14);
  border: 1px solid rgba(139, 92, 246, 0.32);
  color: #c4b5fd;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.search-input {
  width: 240px;
}

.search-input :deep(.q-field__control) {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05) !important;
  color: white;
}

.search-input :deep(.q-field__native),
.search-input :deep(input::placeholder) {
  color: #94a3b8;
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
  background: rgba(139, 92, 246, 0.05);
}

.dark-table :deep(.q-table__bottom) {
  background: transparent;
  color: #94a3b8;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.dark-table :deep(.q-table__bottom .q-btn) {
  color: #94a3b8;
}

/* Badges */
.badge-admin {
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 700;
  background: rgba(139, 92, 246, 0.16);
  color: #c4b5fd;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.badge-user {
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 700;
  background: rgba(148, 163, 184, 0.1);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.badge-active {
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 700;
  background: rgba(34, 197, 94, 0.14);
  color: #86efac;
  border: 1px solid rgba(34, 197, 94, 0.28);
}

.badge-inactive {
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 700;
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
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  box-shadow: 0 10px 26px rgba(124, 58, 237, 0.28);
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
  background: rgba(124, 58, 237, 0.14);
}

.blob-2 {
  bottom: -18%;
  right: -10%;
  width: 600px;
  height: 600px;
  background: rgba(37, 99, 235, 0.12);
  animation-delay: -5s;
}

.blob-3 {
  top: 40%;
  left: 40%;
  width: 400px;
  height: 400px;
  background: rgba(20, 184, 166, 0.07);
  animation-delay: -3s;
}

@keyframes float {
  0%,
  100% { transform: translateY(0) scale(1); }
  50%  { transform: translateY(-30px) scale(1.05); }
}

@media (max-width: 1100px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 700px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .table-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-input {
    width: 100%;
  }

  .dash-nav {
    flex-wrap: wrap;
    gap: 10px;
  }
}

@media (max-width: 520px) {
  .admin-wrapper {
    padding: 14px;
  }
}
</style>
