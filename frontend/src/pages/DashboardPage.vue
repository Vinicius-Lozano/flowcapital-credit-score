<template>
  <q-page class="q-pa-md">
    <div class="row items-center q-mb-lg full-width" style="max-width: 1200px; margin: 0 auto">
      <q-btn flat icon="arrow_back" color="primary" label="Voltar" to="/" no-caps class="q-mr-md" />
      <div class="text-h4 text-weight-bolder">Painel Open Finance</div>
      <q-space />
      <q-btn color="primary" icon="refresh" label="Sincronizar Banco" rounded @click="simularConexaoBanco" :loading="conectando" />
    </div>

    <!-- Empty State -->
    <div v-if="!resultado && !conectando" class="flex flex-center text-center q-pa-xl">
      <div>
        <q-icon name="account_balance" size="6rem" color="grey-4" class="q-mb-md" />
        <div class="text-h5 text-grey-8">Nenhum dado sincronizado.</div>
        <div class="text-body1 text-grey-6">Clique em "Sincronizar Banco" para emitir sua avaliação de crédito baseada no fluxo de caixa atual.</div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="conectando" class="flex flex-center text-center q-pa-xl">
      <q-spinner-orbit color="primary" size="5em" />
      <div class="text-h6 q-mt-md text-grey-8">Sincronizando transações...</div>
      <div class="text-caption text-grey-6">Analisando entradas e saídas recentes...</div>
    </div>

    <div v-if="resultado && !conectando" class="row q-col-gutter-lg full-width" style="max-width: 1200px; margin: 0 auto">
      
      <!-- Score Panel -->
      <div class="col-12 col-md-4">
        <q-card :class="'bg-' + resultado.cor + ' text-white text-center q-pa-lg shadow-4'" style="border-radius: 12px">
          <div class="text-overline text-uppercase text-weight-bold opacity-80">Score de Crédito</div>
          <div class="text-h1 text-weight-bolder q-my-sm">{{ resultado.score }}</div>
          <div class="text-h5 text-weight-bold q-mb-md">{{ resultado.status }}</div>
          
          <q-separator dark class="q-my-md opacity-20" />
          
          <div class="text-body2 text-left opacity-90">
            <q-icon name="trending_up" color="green-2" size="sm" class="q-mr-xs"/> Receitas Estimadas: R$ {{ resultado.detalhes.renda_calculada.replace('R$ ', '') }}<br>
            <q-icon name="trending_down" color="red-2" size="sm" class="q-mr-xs"/> Despesas: R$ {{ resultado.detalhes.despesa_calculada.replace('R$ ', '') }}
          </div>
        </q-card>
      </div>

      <!-- Transactions Table -->
      <div class="col-12 col-md-8">
        <q-card bordered class="shadow-1 no-shadow" style="border-radius: 12px">
          <q-table
            title="Extrato Analisado"
            :rows="resultado.transacoes"
            :columns="colunas"
            row-key="data"
            :pagination="{ rowsPerPage: 10 }"
            flat
          >
            <!-- Custom Formatting for Values -->
            <template v-slot:body-cell-valor="props">
              <q-td :props="props" :class="props.row.tipo === 'PIX_RECEBIDO' ? 'text-green text-weight-bold' : 'text-red'">
                {{ props.row.tipo === 'PIX_RECEBIDO' ? '+' : '-' }} R$ {{ props.row.valor.toFixed(2) }}
              </q-td>
            </template>
            
            <!-- Custom Formatting for Types to look nice -->
            <template v-slot:body-cell-tipo="props">
              <q-td :props="props">
                <q-badge :color="props.row.tipo === 'PIX_RECEBIDO' ? 'green-1' : 'red-1'" :text-color="props.row.tipo === 'PIX_RECEBIDO' ? 'green-9' : 'red-9'" class="q-pa-xs">
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

const simularConexaoBanco = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('Sessão expirada. Por favor, faça login novamente.')
    router.push('/login')
    return
  }

  conectando.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    const resposta = await axios.post(`${API_URL}/api/analisar/`, {}, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    resultado.value = resposta.data
  } catch (erro) {
    console.error("Erro", erro)
    if (erro.response && erro.response.status === 401) {
       alert("Sessão inválida. Faça login novamente.")
       router.push('/login')
    } else {
       alert("Erro no backend (Verifique se a API está rodando!)")
    }
  } finally {
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
.opacity-80 { opacity: 0.8; }
.opacity-90 { opacity: 0.9; }
.opacity-20 { opacity: 0.2; }
</style>
