<template>
  <q-page class="flex flex-center column q-pa-md bg-grey-1">
    
    <div class="text-center q-mb-xl">
      <div class="text-h3 text-primary text-weight-bold">FlowCapital</div>
      <div class="text-subtitle1 text-grey-8">Conecte seu banco para análise justa.</div>
    </div>
    
    <q-card v-if="!resultado && !conectando" style="width: 100%; max-width: 450px" bordered class="q-pa-lg shadow-4 text-center">
      <q-icon name="account_balance" size="4rem" color="primary" class="q-mb-md" />
      <div class="text-h6 q-mb-sm text-grey-9">Autorizar Open Finance</div>
      <div class="text-body2 text-grey-7 q-mb-lg">
        Não precisamos do seu holerite. Conecte sua conta bancária principal de forma segura para avaliarmos seu fluxo de caixa.
      </div>
      
      <q-btn 
        color="green-8" 
        icon="lock"
        label="Conectar meu Banco Principal" 
        class="full-width q-mt-sm" 
        size="lg" 
        rounded
        @click="simularConexaoBanco" 
      />
    </q-card>

    <div v-if="conectando" class="text-center">
      <q-spinner-pie color="primary" size="4em" />
      <div class="text-h6 q-mt-md text-grey-8">Redirecionando para o seu banco...</div>
      <div class="text-caption text-grey-6">Puxando extrato dos últimos 90 dias de forma segura.</div>
    </div>

    <q-slide-transition>
      <q-card 
        v-if="resultado && !conectando" 
        :class="'bg-' + resultado.cor + ' text-white q-pa-lg text-center shadow-6'" 
        style="width: 100%; max-width: 450px; border-radius: 16px"
      >
        <div class="text-subtitle1 text-uppercase text-weight-medium">Score FlowCapital</div>
        <div class="text-h1 text-weight-bolder q-my-md">{{ resultado.score }}</div>
        <div class="text-h5 text-weight-bold">{{ resultado.status }}</div>
        
        <q-separator dark class="q-my-md" />
        
        <div class="text-body2 opacity-80 text-left q-mt-md">
          <strong>Extrato Analisado (Motor Python):</strong><br>
          <q-icon name="check_circle" color="green-3"/> Entradas: {{ resultado.detalhes.renda_calculada }}<br>
          <q-icon name="warning" color="red-3"/> Saídas: {{ resultado.detalhes.despesa_calculada }}<br>
          <q-icon name="receipt_long" color="blue-3"/> Transações lidas: {{ resultado.detalhes.qtd_transacoes_analisadas }}
        </div>
        
        <q-btn outline color="white" label="Fazer nova simulação" class="full-width q-mt-lg" rounded @click="resetar" />
      </q-card>
    </q-slide-transition>

  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const resultado = ref(null)
const conectando = ref(false)

// O "Extrato Open Finance" (Exatamente como um banco devolve)
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
    // Fingindo tempo de processamento do banco
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Mandando a LISTA DE TRANSAÇÕES crua para o Python se virar
    const resposta = await axios.post('http://localhost:8000/api/analisar/', extratoDummy)
    
    resultado.value = resposta.data
  } catch (erro) {
    console.error("Erro", erro)
    alert("Erro no servidor Django!")
  } finally {
    conectando.value = false
  }
}

const resetar = () => {
  resultado.value = null
}
</script>