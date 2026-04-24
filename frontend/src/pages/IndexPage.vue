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

      <!-- Demo Feature Area -->
      <div class="col-12 col-md-5 flex flex-center z-top q-mt-xl q-mt-md-none">
        
        <!-- INITIAL DEMO CARD -->
        <q-card v-if="!resultado && !conectando" class="glass-card text-white text-center q-pa-lg" style="width: 100%; max-width: 450px;">
          <q-icon name="account_balance" size="4rem" color="primary" class="q-mb-md icon-glow" />
          <div class="text-h6 q-mb-sm text-weight-bold">Teste Nosso Motor Open Finance</div>
          <div class="text-body2 text-grey-4 q-mb-lg">
            Veja como funciona nossa análise na prática lendo um extrato de exemplo.
          </div>
          
          <q-btn 
            color="primary" 
            icon="wifi_tethering"
            label="Simular Conexão Bancária" 
            class="full-width q-py-sm text-weight-bold" 
            size="md" 
            rounded
            @click="simularConexaoBanco" 
          />
        </q-card>

        <!-- LOADING STATE -->
        <div v-if="conectando" class="text-center text-white">
          <q-spinner-orbit color="primary" size="5em" />
          <div class="text-h6 q-mt-md">Mapeando transações...</div>
          <div class="text-caption text-grey-5">Analisando o fluxo de caixa com IA.</div>
        </div>

        <!-- RESULT DEMO CARD -->
        <q-slide-transition>
          <q-card 
            v-if="resultado && !conectando" 
            :class="'bg-' + resultado.cor + '-9 glass-card-solid text-white q-pa-lg text-center'" 
            style="width: 100%; max-width: 450px;"
          >
            <div class="text-overline text-uppercase text-weight-bold opacity-80">Resultado da Simulação</div>
            <div class="text-h2 text-weight-bolder q-my-sm">{{ resultado.score }}</div>
            <div class="text-h5 text-weight-bold q-mb-md">{{ resultado.status }}</div>
            
            <q-separator dark class="q-my-md opacity-20" />
            
            <div class="text-body2 opacity-90 text-left">
              <strong>Motor de Risco:</strong><br><br>
              <q-icon name="trending_up" color="green-4" size="sm" class="q-mr-xs"/> Receitas: R$ {{ resultado.detalhes.renda_calculada }}<br>
              <q-icon name="trending_down" color="red-4" size="sm" class="q-mr-xs"/> Despesas: R$ {{ resultado.detalhes.despesa_calculada }}<br>
              <q-icon name="analytics" color="blue-4" size="sm" class="q-mr-xs"/> Transações processadas: {{ resultado.detalhes.qtd_transacoes_analisadas }}
            </div>
            
            <q-btn outline color="white" label="Tentar Novamente" class="full-width q-mt-xl text-weight-bold" rounded @click="resetar" />
          </q-card>
        </q-slide-transition>

      </div>
    </div>
    
    <!-- Abstract Background Elements -->
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
  cliente: "Vinicius Lozano",
  cpf: "123.456.789-00",
  transacoes: [
    { data: "2026-04-20", tipo: "PIX_RECEBIDO", valor: 1500.00, descricao: "Serviço Prestado - Cliente A" },
    { data: "2026-04-21", tipo: "BOLETO_PAGO", valor: 850.00, descricao: "Aluguel Equipamento" },
    { data: "2026-04-22", tipo: "PIX_RECEBIDO", valor: 3200.00, descricao: "Serviço Prestado - Cliente B" },
    { data: "2026-04-23", tipo: "COMPRA_CARTAO", valor: 450.00, descricao: "Mercado" },
    { data: "2026-04-23", tipo: "TARIFA_BANCARIA", valor: 35.00, descricao: "Manutenção Conta" }
  ]
}

const simularConexaoBanco = async () => {
  conectando.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    const resposta = await axios.post('http://localhost:8000/api/analisar/', extratoDummy)
    resultado.value = resposta.data
  } catch (erro) {
    console.error("Erro", erro)
    alert("Erro no backend (Verifique se a API está rodando!)")
  } finally {
    conectando.value = false
  }
}

const resetar = () => {
  resultado.value = null
}
</script>

<style scoped>
.leading-tight { line-height: 1.1; }
.z-top { z-index: 10; }

.text-glow {
  text-shadow: 0 0 20px rgba(25, 118, 210, 0.6);
}
.icon-glow {
  filter: drop-shadow(0 0 10px rgba(25, 118, 210, 0.4));
}
.btn-glow {
  box-shadow: 0 0 25px rgba(25, 118, 210, 0.5);
  transition: all 0.3s ease;
}
.btn-glow:hover {
  box-shadow: 0 0 40px rgba(25, 118, 210, 0.8);
  transform: translateY(-2px);
}

.glass-card {
  background: rgba(40, 40, 40, 0.4);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
}
.glass-card-solid {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
}

.opacity-80 { opacity: 0.8; }
.opacity-90 { opacity: 0.9; }
.opacity-20 { opacity: 0.2; }

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