<template>
  <q-page class="flex flex-center column">
    <div class="text-h4 text-primary q-mb-xl text-weight-bold">
      FlowCapital
    </div>

    <q-badge 
      :color="conectado ? 'positive' : 'negative'" 
      class="text-h6 q-pa-md shadow-2"
    >
      {{ conectado ? '🟢 Back-end Conectado!' : '🔴 Back-end Desconectado' }}
    </q-badge>

    <div v-if="!conectado" class="text-caption q-mt-md text-grey">
      Verifique se o Django está rodando na porta 8000.
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Variável que guarda o estado da conexão (começa falsa)
const conectado = ref(false)

// Assim que a tela carrega (mounted), ele tenta bater no Django
onMounted(async () => {
  try {
    // Usando o axios direto aqui:
    const resposta = await axios.get('http://localhost:8000/api/test/')
    if (resposta.data.status === 'conectado') {
      conectado.value = true // Ficou verde!
    }
  } catch (erro) {
    conectado.value = false // Ficou vermelho!
    console.error("Erro ao tentar conectar:", erro)
  }
})
</script>