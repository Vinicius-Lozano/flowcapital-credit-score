<template>
  <q-page class="q-pa-md bg-dark">
    <div class="row items-center q-mb-lg full-width" style="max-width: 1200px; margin: 0 auto">
      <q-btn flat icon="arrow_back" color="primary" label="Voltar" to="/" no-caps class="q-mr-md" />
      <div class="text-h4 text-weight-bolder text-white">Análise de Crédito (Pluggy)</div>
      <q-space />
      <q-btn 
        color="primary" 
        icon="account_balance" 
        label="Conectar Banco" 
        rounded 
        push
        @click="abrirPluggy" 
        :loading="carregandoWidget" 
        class="q-mr-sm"
      />
      <q-btn 
        color="white" 
        flat
        icon="terminal" 
        label="Simular" 
        rounded 
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
          Conecte sua conta via <b>Pluggy</b> ou use o modo <b>Simular</b> para ver como funciona.
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="conectando" class="flex flex-center text-center q-pa-xl">
      <q-spinner-dots color="primary" size="5em" />
      <div class="text-h6 q-mt-md text-white">Processando dados financeiros...</div>
      <div class="text-caption text-grey-5">Sincronizando e calculando score...</div>
    </div>

    <div v-if="resultado && !conectando" class="row q-col-gutter-lg full-width" style="max-width: 1200px; margin: 0 auto">
      
      <!-- Score Panel -->
      <div class="col-12 col-md-4">
        <q-card :class="'bg-' + resultado.cor + ' text-white text-center q-pa-lg shadow-4'" style="border-radius: 20px">
          <div class="text-overline text-uppercase text-weight-bold opacity-80">Score de Crédito</div>
          <div class="text-h1 text-weight-bolder q-my-sm">{{ resultado.score }}</div>
          <div class="text-h5 text-weight-bold q-mb-md">{{ resultado.status }}</div>
          
          <q-separator dark class="q-my-md opacity-20" />
          
          <div class="text-body2 text-left opacity-90">
            <div class="row items-center q-mb-sm">
              <q-icon name="info" class="q-mr-xs" />
              <span>Origem: <b>{{ resultado.origem }}</b></span>
            </div>
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
            title="Extrato Consolidado"
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
const carregandoWidget = ref(false)
const resultado = ref(null)

const API_URL = process.env.API_URL

const colunas = [
  { name: 'data', align: 'left', label: 'Data', field: 'data', sortable: true },
  { name: 'descricao', align: 'left', label: 'Descrição', field: 'descricao', sortable: true },
  { name: 'tipo', align: 'center', label: 'Tipo', field: 'tipo' },
  { name: 'valor', align: 'right', label: 'Valor', field: 'valor', sortable: true }
]

const abrirPluggy = async () => {
  carregandoWidget.value = true
  try {
    const authToken = localStorage.getItem('token')
    const { data } = await axios.get(`${API_URL}/api/pluggy/token/`, {
      headers: { Authorization: `Token ${authToken}` }
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
    alert('Erro ao iniciar conexão com a Pluggy.');
  } finally {
    carregandoWidget.value = false
  }
}

const analisarComPluggy = async (itemId) => {
  conectando.value = true
  try {
    const authToken = localStorage.getItem('token')
    const resp = await axios.post(
      `${API_URL}/api/analisar/`,
      { item_id: itemId },
      { headers: { Authorization: `Token ${authToken}` } }
    )
    resultado.value = resp.data
  } catch (error) {
    console.error(error)
    alert('Erro ao analisar os dados da conta.')
  } finally {
    conectando.value = false
  }
}

const simularAnalise = async () => {
  conectando.value = true
  resultado.value = null
  try {
    const authToken = localStorage.getItem('token')
    const resp = await axios.post(
      `${API_URL}/api/analisar/`,
      { mock: true },
      { headers: { Authorization: `Token ${authToken}` } }
    )
    setTimeout(() => {
      resultado.value = resp.data
      conectando.value = false
    }, 1000)
  } catch (error) {
    console.error('Erro na simulação:', error)
    alert('Erro ao simular análise.')
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
