<template>
  <q-page class="capital-home-page">
    <div class="grid-overlay"></div>

    <div class="home-wrapper">
      <!-- ── Hero ───────────────────────────────────────── -->
      <section class="hero-section">
        <div class="brand-badge">
          <span class="pulse-dot"></span>
          Fintech · Open Finance · Score Alternativo
        </div>

        <h1>
          Seu fluxo de renda vira
          <span class="gradient-text">limite de crédito.</span>
        </h1>

        <p>
          O Capital Flow analisa movimentações financeiras reais para oferecer uma
          análise de crédito mais justa, rápida e sem burocracia.
        </p>

        <div class="hero-actions">
          <q-btn to="/registrar" label="Começar agora" no-caps unelevated class="primary-gradient-btn" />
          <q-btn to="/login" label="Acessar painel" no-caps outline class="outline-btn" />
        </div>

        <div class="stats-bar">
          <div class="stat-item">
            <strong>2.1k+</strong>
            <span>Análises realizadas</span>
          </div>
          <div class="stat-sep"></div>
          <div class="stat-item">
            <strong>94%</strong>
            <span>Taxa de aprovação</span>
          </div>
          <div class="stat-sep"></div>
          <div class="stat-item">
            <strong>60s</strong>
            <span>Tempo de resposta</span>
          </div>
          <div class="stat-sep"></div>
          <div class="stat-item">
            <strong>Zero</strong>
            <span>Burocracia</span>
          </div>
        </div>

        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon"><q-icon name="receipt_long" size="1.1rem" /></div>
            <strong>Sem holerite</strong>
            <span>Análise baseada no fluxo real da conta</span>
          </div>
          <div class="feature-card">
            <div class="feature-icon"><q-icon name="auto_awesome" size="1.1rem" /></div>
            <strong>IA explicável</strong>
            <span>Resultado transparente ao usuário</span>
          </div>
          <div class="feature-card">
            <div class="feature-icon"><q-icon name="diversity_3" size="1.1rem" /></div>
            <strong>Mais inclusão</strong>
            <span>Pensado para renda variável</span>
          </div>
        </div>
      </section>

      <!-- ── Demo ───────────────────────────────────────── -->
      <section class="demo-section">
        <q-card v-if="!resultado && !conectando" class="demo-card">
          <div class="demo-icon">
            <q-icon name="account_balance" size="3rem" />
          </div>
          <div class="tech-badge">
            <q-icon name="bolt" size="xs" class="q-mr-xs" />
            Open Finance · AWS Bedrock · Textract
          </div>
          <h2>Teste o motor de análise</h2>
          <p>
            Simule uma conexão bancária via Open Finance e veja o score
            calculado pela IA em tempo real.
          </p>
          <q-btn
            label="Simular conexão bancária"
            icon="wifi_tethering"
            no-caps
            unelevated
            class="primary-gradient-btn full-width"
            @click="simularConexaoBanco"
          />
        </q-card>

        <div v-if="conectando" class="loading-card">
          <q-spinner-orbit color="primary" size="4em" />
          <h2>Mapeando transações...</h2>
          <p>Analisando o fluxo de caixa com o motor de risco.</p>
        </div>

        <q-slide-transition>
          <q-card v-if="resultado && !conectando" class="result-card">
            <div class="result-label">Resultado da simulação</div>

            <svg viewBox="0 0 200 110" class="demo-gauge">
              <defs>
                <linearGradient id="demoGaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%"   stop-color="#ef4444" />
                  <stop offset="45%"  stop-color="#f59e0b" />
                  <stop offset="100%" stop-color="#22c55e" />
                </linearGradient>
              </defs>
              <path d="M 15 95 A 80 80 0 0 1 185 95"
                fill="none" stroke="#e2e8f0" stroke-width="12" stroke-linecap="round" />
              <path d="M 15 95 A 80 80 0 0 1 185 95"
                fill="none" stroke="url(#demoGaugeGrad)" stroke-width="12" stroke-linecap="round"
                :stroke-dasharray="251"
                :stroke-dashoffset="251 * (1 - resultado.score / 1000)"
                style="transition: stroke-dashoffset 0.9s ease;" />
              <text x="100" y="73" text-anchor="middle" fill="#0f172a"
                font-size="32" font-weight="900" font-family="system-ui">
                {{ resultado.score }}
              </text>
              <text x="100" y="90" text-anchor="middle" fill="#64748b"
                font-size="9" font-family="system-ui">de 1000</text>
            </svg>

            <div class="status-chip">{{ resultado.status }}</div>

            <div class="result-details">
              <h3>Motor de risco</h3>
              <div class="detail-row">
                <q-icon name="trending_up" color="green" size="sm" />
                <span>Receitas</span>
                <strong>{{ resultado.detalhes.renda_calculada }}</strong>
              </div>
              <div class="detail-row">
                <q-icon name="trending_down" color="red" size="sm" />
                <span>Despesas</span>
                <strong>{{ resultado.detalhes.despesa_calculada }}</strong>
              </div>
              <div class="detail-row">
                <q-icon name="analytics" color="blue" size="sm" />
                <span>Transações</span>
                <strong>{{ resultado.detalhes.qtd_transacoes_analisadas }}</strong>
              </div>
            </div>

            <q-btn
              label="Simular novamente"
              no-caps
              outline
              class="result-btn full-width"
              @click="resetar"
            />
          </q-card>
        </q-slide-transition>
      </section>
    </div>

    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const resultado = ref(null)
const conectando = ref(false)
const API_URL = process.env.API_URL

const simularConexaoBanco = async () => {
  conectando.value = true
  try {
    await new Promise((r) => setTimeout(r, 1500))
    const resposta = await axios.post(`${API_URL}/api/demo/`)
    resultado.value = resposta.data
  } catch (erro) {
    console.error('Erro na demo', erro)
  } finally {
    conectando.value = false
  }
}

const resetar = () => { resultado.value = null }
</script>

<style scoped>
/* ── Page ──────────────────────────────────────────────────────── */
.capital-home-page {
  min-height: calc(100vh - 70px);
  position: relative;
  overflow: hidden;
  padding: 56px 24px;
  background:
    radial-gradient(circle at top left,    rgba(37, 99, 235, 0.38), transparent 35%),
    radial-gradient(circle at bottom right, rgba(22, 163, 74, 0.22), transparent 35%),
    linear-gradient(135deg, #020617, #0f172a);
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(37, 99, 235, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37, 99, 235, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
  z-index: 1;
  pointer-events: none;
}

.home-wrapper {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.08fr 0.92fr;
  gap: 52px;
  align-items: center;
}

/* ── Hero ──────────────────────────────────────────────────────── */
.hero-section { color: white; }

.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.16);
  border: 1px solid rgba(96, 165, 250, 0.35);
  color: #bfdbfe;
  font-weight: 700;
  font-size: 0.8rem;
  letter-spacing: 0.02em;
  margin-bottom: 22px;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  background: #34d399;
  border-radius: 50%;
  flex-shrink: 0;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.75); }
}

.hero-section h1 {
  font-size: 3.8rem;
  line-height: 1.02;
  font-weight: 900;
  margin: 0 0 20px;
}

.gradient-text {
  display: block;
  background: linear-gradient(135deg, #60a5fa 0%, #34d399 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-section p {
  max-width: 560px;
  font-size: 1.08rem;
  line-height: 1.7;
  color: #94a3b8;
  margin: 0 0 28px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 28px;
}

.primary-gradient-btn {
  min-height: 48px;
  padding: 0 28px;
  border-radius: 14px;
  font-weight: 900;
  color: white !important;
  background: linear-gradient(135deg, #2563eb, #16a34a);
  box-shadow: 0 14px 34px rgba(37, 99, 235, 0.3);
}

.primary-gradient-btn:hover { transform: translateY(-1px); }

.outline-btn {
  min-height: 48px;
  padding: 0 24px;
  border-radius: 14px;
  font-weight: 800;
  color: white;
  border-color: rgba(255, 255, 255, 0.5);
}

/* ── Stats bar ─────────────────────────────────────────────────── */
.stats-bar {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.65);
  border: 1px solid rgba(148, 163, 184, 0.14);
  backdrop-filter: blur(10px);
  margin-bottom: 28px;
}

.stat-item { flex: 1; text-align: center; }

.stat-item strong {
  display: block;
  font-size: 1.35rem;
  font-weight: 900;
  color: white;
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat-item span {
  display: block;
  font-size: 0.72rem;
  color: #64748b;
  margin-top: 4px;
}

.stat-sep {
  width: 1px;
  height: 32px;
  background: rgba(148, 163, 184, 0.18);
  flex-shrink: 0;
}

/* ── Feature grid ──────────────────────────────────────────────── */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.feature-card {
  padding: 16px;
  border-radius: 18px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.18);
  transition: border-color 0.2s, transform 0.2s;
}

.feature-card:hover {
  border-color: rgba(96, 165, 250, 0.4);
  transform: translateY(-2px);
}

.feature-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(37, 99, 235, 0.16);
  border: 1px solid rgba(96, 165, 250, 0.22);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #60a5fa;
  margin-bottom: 10px;
}

.feature-card strong {
  display: block;
  color: white;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.feature-card span {
  color: #64748b;
  font-size: 0.8rem;
  line-height: 1.4;
}

/* ── Demo section ──────────────────────────────────────────────── */
.demo-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.demo-card,
.result-card {
  width: 100%;
  max-width: 470px;
  border-radius: 28px;
  padding: 32px 28px;
  text-align: center;
  color: #0f172a;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 28px 90px rgba(0, 0, 0, 0.4);
}

.demo-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 14px;
  border-radius: 22px;
  background: linear-gradient(135deg, #2563eb, #22c55e);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 12px 32px rgba(37, 99, 235, 0.38);
}

.tech-badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 11px;
  border-radius: 999px;
  background: #f0fdf4;
  color: #166534;
  font-size: 0.7rem;
  font-weight: 700;
  margin-bottom: 14px;
  letter-spacing: 0.02em;
}

.demo-card h2 {
  font-size: 1.6rem;
  font-weight: 900;
  margin: 0 0 10px;
}

.demo-card p {
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 22px;
  font-size: 0.92rem;
}

.loading-card {
  width: 100%;
  max-width: 470px;
  border-radius: 28px;
  padding: 48px 28px;
  text-align: center;
  color: white;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(14px);
}

.loading-card h2 {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 22px 0 8px;
}

.loading-card p { color: #94a3b8; margin: 0; }

/* ── Result card ───────────────────────────────────────────────── */
.result-label {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  background: #eff6ff;
  color: #2563eb;
  font-weight: 800;
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 14px;
}

.demo-gauge {
  width: 100%;
  max-width: 220px;
  margin: 0 auto 12px;
  display: block;
}

.status-chip {
  display: inline-block;
  padding: 9px 18px;
  border-radius: 12px;
  font-weight: 900;
  font-size: 0.88rem;
  margin-bottom: 16px;
  color: #166534;
  background: #dcfce7;
}

.result-details {
  text-align: left;
  padding: 14px;
  border-radius: 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  margin-bottom: 14px;
}

.result-details h3 {
  margin: 0 0 10px;
  font-size: 0.88rem;
  color: #0f172a;
  font-weight: 700;
}

.detail-row {
  display: grid;
  grid-template-columns: 24px 1fr auto;
  align-items: center;
  gap: 8px;
  color: #475569;
  margin-bottom: 9px;
  font-size: 0.86rem;
}

.detail-row:last-child { margin-bottom: 0; }
.detail-row strong { color: #0f172a; font-weight: 700; }

.result-btn {
  min-height: 44px;
  border-radius: 14px;
  font-weight: 800;
  color: #2563eb;
}

/* ── Blobs ─────────────────────────────────────────────────────── */
.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(110px);
  z-index: 0;
  animation: float 10s ease-in-out infinite;
  pointer-events: none;
}

.blob-1 { top: -12%; left: -10%; width: 500px; height: 500px; background: rgba(37, 99, 235, 0.18); }
.blob-2 { bottom: -20%; right: -12%; width: 600px; height: 600px; background: rgba(22, 163, 74, 0.16); animation-delay: -5s; }

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50%       { transform: translateY(-30px) scale(1.05); }
}

/* ── Responsive ────────────────────────────────────────────────── */
@media (max-width: 960px) {
  .home-wrapper { grid-template-columns: 1fr; gap: 36px; }
  .hero-section { text-align: center; }
  .hero-section p { margin-left: auto; margin-right: auto; }
  .hero-actions { justify-content: center; }
  .stats-bar { flex-wrap: wrap; gap: 12px; }
  .stat-sep { display: none; }
  .feature-grid { grid-template-columns: 1fr; }
  .hero-section h1 { font-size: 2.8rem; }
  .brand-badge { justify-content: center; }
}

@media (max-width: 520px) {
  .capital-home-page { padding: 36px 16px; }
  .hero-section h1 { font-size: 2.2rem; }
  .demo-card, .result-card { border-radius: 22px; padding: 24px 20px; }
}
</style>
