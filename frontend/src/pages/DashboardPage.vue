<template>
  <q-page class="q-pa-md bg-dark">
    <div class="row items-center q-mb-lg full-width" style="max-width: 1200px; margin: 0 auto">
      <q-btn flat icon="arrow_back" color="primary" label="Voltar" to="/" no-caps class="q-mr-md" />
      <div class="text-h4 text-weight-bolder text-white">Análise de Crédito</div>
      <q-space />
      <q-btn 
        color="primary" 
        icon="rocket_launch" 
        label="Simular Avaliação" 
        rounded 
        push
        @click="simularAnalise" 
        :loading="conectando" 
      />
    </div>

    <!-- Empty State -->
    <div v-if="!resultado && !conectando" class="flex flex-center text-center q-pa-xl">
      <div class="q-pa-lg bg-dark-light shadow-2" style="border-radius: 20px; max-width: 500px">
        <q-icon name="analytics" size="6rem" color="primary" class="q-mb-md" />
        <div class="text-h5 text-white q-mb-sm">Pronto para sua análise?</div>
        <div class="text-body1 text-grey-4">
          Clique no botão <b>Simular Avaliação</b> para processar seu histórico de transações e gerar seu score de crédito instantaneamente.
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="conectando" class="flex flex-center text-center q-pa-xl">
      <q-spinner-dots color="primary" size="5em" />
      <div class="text-h6 q-mt-md text-white">Processando dados financeiros...</div>
      <div class="text-caption text-grey-5">Calculando score baseado no fluxo de caixa...</div>
    </div>

    <div v-if="resultado && !conectando" class="row q-col-gutter-lg full-width" style="max-width: 1200px; margin: 0 auto">
      
      <!-- Score Panel -->
      <div class="col-12 col-md-4">
        <q-card :class="'bg-' + resultado.cor + ' text-white text-center q-pa-lg shadow-4'" style="border-radius: 20px">
          <div class="text-overline text-uppercase text-weight-bold opacity-80">Flow Score</div>
          <div class="text-h1 text-weight-bolder q-my-sm">{{ resultado.score }}</div>
          <div class="text-h5 text-weight-bold q-mb-md">{{ resultado.status }}</div>
          
          <q-separator dark class="q-my-md opacity-20" />
          
          <div class="text-body2 text-left opacity-90">
            <div class="row justify-between q-mb-xs">
              <span><q-icon name="trending_up" class="q-mr-xs"/> Entradas:</span>
              <span class="text-weight-bold">{{ resultado.detalhes.renda_calculada }}</span>
            </div>
            <div class="row justify-between">
              <span><q-icon name="trending_down" class="q-mr-xs"/> Saídas:</span>
              <span class="text-weight-bold">{{ resultado.detalhes.despesa_calculada }}</span>
            </div>
          </div>
        </q-card>
      </div>

      <!-- Transactions Table -->
      <div class="col-12 col-md-8">
        <q-card square class="bg-dark-light text-white shadow-2" style="border-radius: 20px; border: 1px solid rgba(255,255,255,0.1)">
          <q-table
            title="Histórico Processado"
            :rows="resultado.transacoes"
            :columns="colunas"
            row-key="data"
            dark
            flat
            :pagination="{ rowsPerPage: 8 }"
          >
            <template v-slot:body-cell-valor="props">
              <q-td :props="props" :class="props.row.tipo === 'PIX_RECEBIDO' ? 'text-green-13 text-weight-bold' : 'text-red-13'">
                {{ props.row.tipo === 'PIX_RECEBIDO' ? '+' : '-' }} R$ {{ props.row.valor.toFixed(2) }}
              </q-td>
            </template>
            
            <template v-slot:body-cell-tipo="props">
              <q-td :props="props">
                <q-badge :color="props.row.tipo === 'PIX_RECEBIDO' ? 'green-9' : 'red-9'" class="q-pa-xs">
                  {{ props.row.tipo.replace('_', ' ') }}
                </q-badge>
              </q-td>
            </template>
          </q-table>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const conectando = ref(false)
const resultado = ref(null)

const API_URL = process.env.API_URL

const colunas = [
  { name: 'data', align: 'left', label: 'Data', field: 'data', sortable: true },
  { name: 'descricao', align: 'left', label: 'Descrição', field: 'descricao', sortable: true },
  { name: 'tipo', align: 'center', label: 'Tipo', field: 'tipo' },
  { name: 'valor', align: 'right', label: 'Valor', field: 'valor', sortable: true }
]

const simularAnalise = async () => {
  conectando.value = true
  resultado.value = null
  
  try {
    const authToken = localStorage.getItem('token')
    // Calling the endpoint without link_id triggers the Mock simulation in backend
    const resp = await axios.post(
      `${API_URL}/api/analisar/`,
      {},
      { headers: { Authorization: `Token ${authToken}` } }
    )
    
    // Artificial delay to make it feel like "processing"
    setTimeout(() => {
      resultado.value = resp.data
      conectando.value = false
    }, 1500)
  } catch (e) {
    console.error('Erro na simulação:', e)
    alert('Erro ao processar simulação. Verifique se o backend está rodando.')
    conectando.value = false
  }
}

onMounted(() => {
  if (!localStorage.getItem('token')) {
    router.push('/login')
  }
})
</script>

<style scoped>
.bg-dark-light {
  background: #1e1e1e !important;
}
.opacity-80 { opacity: 0.8; }
.opacity-90 { opacity: 0.9; }
.opacity-20 { opacity: 0.2; }
</style>
