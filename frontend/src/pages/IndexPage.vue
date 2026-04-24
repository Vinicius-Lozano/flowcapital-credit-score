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

    </div>

    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
  </q-page>
</template>

<script setup>
// Página inicial apenas para visualização e redirecionamento de usuários deslogados.
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
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-section {
  color: white;
  text-align: center;
  max-width: 800px;
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
  margin: 0 auto 30px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  justify-content: center;
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
  max-width: 800px;
  margin: 0 auto;
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
}
</style>
