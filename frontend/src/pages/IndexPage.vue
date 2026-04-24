<template>
  <q-page class="flex flex-center q-pa-md" style="min-height: calc(100vh - 70px);">
    <div class="row full-width items-center justify-center q-col-gutter-xl" style="max-width: 1200px;">
      
      <!-- Hero Text Area -->
      <div class="col-12 col-md-6 text-center text-white z-top">
        <div class="text-h2 text-weight-bolder leading-tight q-mb-md">
          A Análise de Crédito<br>
          <span class="text-primary text-glow">Sem Burocracia.</span>
        </div>
        <div class="text-h6 text-grey-4 q-mb-xl text-weight-light q-mx-auto" style="max-width: 500px;">
          Conecte sua conta bancária via Open Finance em segundos. Esqueça holerites, contadores e papeladas. Aprovação baseada no fluxo de caixa real do seu negócio.
        </div>
        
        <div class="row q-gutter-md justify-center">
          <q-btn 
            to="/registrar"
            color="primary" 
            size="lg" 
            class="q-px-xl text-weight-bold btn-glow" 
            label="Começar Agora" 
            no-caps 
            rounded 
          />
          <q-btn 
            to="/login"
            outline 
            color="white" 
            size="lg" 
            class="q-px-lg text-weight-bold" 
            label="Acessar Painel" 
            no-caps 
            rounded 
          />
        </div>
      </div>

    </div>
    
    <!-- Abstract Background Elements -->
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
  </q-page>
</template>

<script setup>
// Página inicial apenas para visualização e redirecionamento de usuários deslogados.
</script>

<style scoped>
.leading-tight { line-height: 1.1; }
.z-top { z-index: 10; }

.text-glow {
  text-shadow: 0 0 20px rgba(25, 118, 210, 0.6);
}
.btn-glow {
  box-shadow: 0 0 25px rgba(25, 118, 210, 0.5);
  transition: all 0.3s ease;
}
.btn-glow:hover {
  box-shadow: 0 0 40px rgba(25, 118, 210, 0.8);
  transform: translateY(-2px);
}

/* Abstract Background Blobs */
.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  z-index: 0;
  animation: float 10s ease-in-out infinite;
}
.blob-1 {
  top: -10%;
  left: -10%;
  width: 500px;
  height: 500px;
  background: rgba(25, 118, 210, 0.15);
}
.blob-2 {
  bottom: -20%;
  right: -10%;
  width: 600px;
  height: 600px;
  background: rgba(156, 39, 176, 0.15);
  animation-delay: -5s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-30px) scale(1.05); }
}
</style>