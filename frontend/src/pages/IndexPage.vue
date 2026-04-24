<template>
  <q-page class="capital-home-page">
    <div class="home-wrapper">
      <section class="hero-section">
        <div class="brand-badge">Fintech • Open Finance • Score alternativo</div>

        <h1>
          Seu fluxo de renda vira
          <span>limite de crédito.</span>
        </h1>

        <p>
          O Capital Flow analisa movimentações financeiras reais para oferecer uma
          análise de crédito mais justa, rápida e sem burocracia.
        </p>

        <div class="hero-actions">
          <q-btn
            to="/registrar"
            label="Começar agora"
            no-caps
            unelevated
            class="primary-gradient-btn"
          />

          <q-btn
            to="/login"
            label="Acessar painel"
            no-caps
            outline
            class="outline-btn"
          />
        </div>

        <div class="feature-grid">
          <div>
            <strong>Sem holerite</strong>
            <span>Análise baseada no fluxo real</span>
          </div>

          <div>
            <strong>Mais clareza</strong>
            <span>Resultado explicado ao usuário</span>
          </div>

          <div>
            <strong>Mais inclusão</strong>
            <span>Pensado para renda variável</span>
          </div>
        </div>
      </section>

      <section class="demo-section">
        <q-card v-if="!resultado && !conectando" class="demo-card">
          <div class="demo-icon">
            <q-icon name="account_balance" size="3.4rem" />
          </div>

          <h2>Teste o motor de análise</h2>

          <p>
            Simule uma conexão bancária via Open Finance usando um extrato de exemplo.
            O sistema enviará os dados para a API e retornará o score calculado.
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
          <q-spinner-orbit color="primary" size="5em" />
          <h2>Mapeando transações...</h2>
          <p>Analisando o fluxo de caixa com o motor de risco.</p>
        </div>

        <q-slide-transition>
          <q-card v-if="resultado && !conectando" class="result-card">
            <div class="result-label">Resultado da simulação</div>

            <div class="score-circle">
              <span>Score</span>
              <strong>{{ resultado.score }}</strong>
            </div>

            <div class="status-chip">
              {{ resultado.status }}
            </div>

            <div class="result-details">
              <h3>Motor de risco</h3>

              <div class="detail-row">
                <q-icon name="trending_up" color="green" />
                <span>Receitas:</span>
                <strong>R$ {{ resultado.detalhes.renda_calculada }}</strong>
              </div>

              <div class="detail-row">
                <q-icon name="trending_down" color="red" />
                <span>Despesas:</span>
                <strong>R$ {{ resultado.detalhes.despesa_calculada }}</strong>
              </div>

              <div class="detail-row">
                <q-icon name="analytics" color="blue" />
                <span>Transações processadas:</span>
                <strong>{{ resultado.detalhes.qtd_transacoes_analisadas }}</strong>
              </div>
            </div>

            <q-btn
              label="Tentar novamente"
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

const extratoDummy = {
  cliente: 'Vinicius Lozano',
  cpf: '123.456.789-00',
  transacoes: [
    {
      data: '2026-04-20',
      tipo: 'PIX_RECEBIDO',
      valor: 1500.0,
      descricao: 'Serviço Prestado - Cliente A',
    },
    {
      data: '2026-04-21',
      tipo: 'BOLETO_PAGO',
      valor: 850.0,
      descricao: 'Aluguel Equipamento',
    },
    {
      data: '2026-04-22',
      tipo: 'PIX_RECEBIDO',
      valor: 3200.0,
      descricao: 'Serviço Prestado - Cliente B',
    },
    {
      data: '2026-04-23',
      tipo: 'COMPRA_CARTAO',
      valor: 450.0,
      descricao: 'Mercado',
    },
    {
      data: '2026-04-23',
      tipo: 'TARIFA_BANCARIA',
      valor: 35.0,
      descricao: 'Manutenção Conta',
    },
  ],
}

const simularConexaoBanco = async () => {
  conectando.value = true

  try {
    await new Promise((resolve) => setTimeout(resolve, 1500))

    const resposta = await axios.post('http://localhost:8000/api/analisar/', extratoDummy)

    resultado.value = resposta.data
  } catch (erro) {
    console.error('Erro', erro)
    alert('Erro no backend. Verifique se a API está rodando!')
  } finally {
    conectando.value = false
  }
}

const resetar = () => {
  resultado.value = null
}
</script>

<style scoped>
.capital-home-page {
  min-height: calc(100vh - 70px);
  position: relative;
  overflow: hidden;
  padding: 56px 24px;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.38), transparent 35%),
    radial-gradient(circle at bottom right, rgba(22, 163, 74, 0.22), transparent 35%),
    linear-gradient(135deg, #020617, #0f172a);
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

.hero-section {
  color: white;
}

.brand-badge {
  display: inline-block;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.16);
  border: 1px solid rgba(96, 165, 250, 0.35);
  color: #bfdbfe;
  font-weight: 700;
  margin-bottom: 22px;
}

.hero-section h1 {
  font-size: 3.8rem;
  line-height: 1.02;
  font-weight: 900;
  margin: 0 0 22px;
}

.hero-section h1 span {
  display: block;
  color: #60a5fa;
  text-shadow: 0 0 24px rgba(37, 99, 235, 0.5);
}

.hero-section p {
  max-width: 590px;
  font-size: 1.1rem;
  line-height: 1.7;
  color: #cbd5e1;
  margin: 0 0 30px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 34px;
}

.primary-gradient-btn {
  min-height: 48px;
  padding: 0 28px;
  border-radius: 14px;
  font-weight: 900;
  color: white;
  background: linear-gradient(135deg, #2563eb, #16a34a);
  box-shadow: 0 14px 34px rgba(37, 99, 235, 0.28);
}

.primary-gradient-btn:hover {
  transform: translateY(-1px);
}

.outline-btn {
  min-height: 48px;
  padding: 0 24px;
  border-radius: 14px;
  font-weight: 800;
  color: white;
  border-color: rgba(255, 255, 255, 0.7);
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.feature-grid div {
  padding: 16px;
  border-radius: 18px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.22);
}

.feature-grid strong {
  display: block;
  color: white;
  margin-bottom: 8px;
}

.feature-grid span {
  color: #cbd5e1;
  font-size: 0.88rem;
  line-height: 1.4;
}

.demo-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.demo-card,
.result-card,
.loading-card {
  width: 100%;
  max-width: 470px;
  border-radius: 28px;
  padding: 30px;
  text-align: center;
  color: #0f172a;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 28px 90px rgba(0, 0, 0, 0.38);
}

.demo-icon {
  width: 82px;
  height: 82px;
  margin: 0 auto 20px;
  border-radius: 24px;
  background: linear-gradient(135deg, #2563eb, #22c55e);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 16px 38px rgba(37, 99, 235, 0.35);
}

.demo-card h2,
.loading-card h2 {
  font-size: 1.65rem;
  font-weight: 900;
  margin: 0 0 10px;
}

.demo-card p,
.loading-card p {
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 24px;
}

.loading-card {
  color: white;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(148, 163, 184, 0.22);
  backdrop-filter: blur(14px);
}

.loading-card p {
  color: #cbd5e1;
}

.result-label {
  display: inline-block;
  padding: 7px 13px;
  border-radius: 999px;
  background: #eff6ff;
  color: #2563eb;
  font-weight: 900;
  font-size: 0.78rem;
  text-transform: uppercase;
  margin-bottom: 18px;
}

.score-circle {
  width: 150px;
  height: 150px;
  margin: 0 auto 18px;
  border-radius: 50%;
  background:
    radial-gradient(circle, white 54%, transparent 55%),
    conic-gradient(#22c55e 0deg, #2563eb 260deg, #e2e8f0 260deg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-circle span {
  color: #64748b;
  font-size: 0.85rem;
  font-weight: 700;
}

.score-circle strong {
  font-size: 2.5rem;
  color: #0f172a;
  font-weight: 900;
}

.status-chip {
  padding: 12px;
  border-radius: 14px;
  font-weight: 900;
  margin-bottom: 18px;
  color: #166534;
  background: #dcfce7;
}

.result-details {
  text-align: left;
  padding: 18px;
  border-radius: 18px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.result-details h3 {
  margin: 0 0 14px;
  font-size: 1rem;
  color: #0f172a;
}

.detail-row {
  display: grid;
  grid-template-columns: 28px 1fr auto;
  align-items: center;
  gap: 8px;
  color: #475569;
  margin-bottom: 12px;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-row strong {
  color: #0f172a;
}

.result-btn {
  margin-top: 18px;
  min-height: 46px;
  border-radius: 14px;
  font-weight: 900;
  color: #2563eb;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(110px);
  z-index: 0;
  animation: float 10s ease-in-out infinite;
}

.blob-1 {
  top: -12%;
  left: -10%;
  width: 500px;
  height: 500px;
  background: rgba(37, 99, 235, 0.18);
}

.blob-2 {
  bottom: -20%;
  right: -12%;
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

@media (max-width: 950px) {
  .home-wrapper {
    grid-template-columns: 1fr;
    gap: 34px;
  }

  .hero-section {
    text-align: center;
  }

  .hero-section p {
    margin-left: auto;
    margin-right: auto;
  }

  .hero-actions {
    justify-content: center;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .hero-section h1 {
    font-size: 2.8rem;
  }
}

@media (max-width: 520px) {
  .capital-home-page {
    padding: 36px 16px;
  }

  .hero-section h1 {
    font-size: 2.25rem;
  }

  .demo-card,
  .result-card,
  .loading-card {
    border-radius: 22px;
    padding: 24px;
  }
}
</style>
