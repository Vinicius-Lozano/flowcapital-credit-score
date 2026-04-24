<template>
  <q-page class="flex flex-center column q-pa-md bg-grey-1">
    
    <div class="text-center q-mb-xl">
      <div class="text-h3 text-primary text-weight-bold">FlowCapital</div>
      <div class="text-subtitle1 text-grey-8">Conecte seu banco para análise justa.</div>
    </div>
    
    <!-- STEP 1: Connect bank via Belvo Widget -->
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
        :loading="carregandoWidget"
        @click="abrirBelvoWidget" 
      />

      <div v-if="erroWidget" class="text-negative text-caption q-mt-md">
        {{ erroWidget }}
      </div>
    </q-card>

    <!-- STEP 2: Loading spinner while backend processes -->
    <div v-if="conectando" class="text-center">
      <q-spinner-pie color="primary" size="4em" />
      <div class="text-h6 q-mt-md text-grey-8">Analisando seu extrato bancário...</div>
      <div class="text-caption text-grey-6">Puxando transações dos últimos 90 dias via Open Finance.</div>
    </div>

    <!-- STEP 3: Show results -->
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
const carregandoWidget = ref(false)
const erroWidget = ref('')

const API_URL = 'http://localhost:8000'

async function abrirBelvoWidget() {
  erroWidget.value = ''
  carregandoWidget.value = true

  try {
    // 1. Get a widget access token from our Django backend
    const tokenResp = await axios.get(`${API_URL}/api/belvo/token/`)
    const accessToken = tokenResp.data.access

    if (!accessToken) {
      erroWidget.value = 'Não foi possível obter token do Belvo. Verifique as chaves na .env.'
      carregandoWidget.value = false
      return
    }

    carregandoWidget.value = false

    // 2. Open the Belvo Connect Widget
    // eslint-disable-next-line no-undef
    window.belvoSDK.createWidget(accessToken, {
      // For Sandbox, use sandbox institutions
      institution: 'erebor_mx_retail',
      institution_type: 'retail',
      locale: 'pt',
      country_codes: ['BR'],

      callback: async (link, institution) => {
        // 3. User successfully connected their bank!
        console.log('Link criado:', link, institution)
        conectando.value = true

        try {
          const token = localStorage.getItem('token')
          const resp = await axios.post(
            `${API_URL}/api/analisar/`,
            { link_id: link },
            { headers: { Authorization: `Token ${token}` } }
          )
          resultado.value = resp.data
        } catch (e) {
          console.error('Erro na análise:', e)
          erroWidget.value = 'Erro ao processar análise de crédito.'
        } finally {
          conectando.value = false
        }
      },

      onExit: (data) => {
        console.log('Widget fechado:', data)
      },

      onEvent: (data) => {
        console.log('Belvo event:', data)
      }
    }).build()
  } catch (e) {
    console.error('Erro ao abrir widget:', e)
    erroWidget.value = 'Erro ao conectar com Belvo. O servidor está rodando?'
    carregandoWidget.value = false
  }
}

const resetar = () => {
  resultado.value = null
}
</script>