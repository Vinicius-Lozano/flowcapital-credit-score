<template>
  <q-page class="flex flex-center bg-grey-2">
    <q-card style="width: 400px; max-width: 95vw" class="shadow-4">
      <q-card-section class="bg-primary text-white text-center q-py-lg">
        <div class="text-h5 text-weight-bold">FlowCapital</div>
        <div class="text-caption q-mt-xs">Acesse sua conta</div>
      </q-card-section>

      <q-card-section class="q-pa-lg">
        <q-form @submit.prevent="fazerLogin">
          <q-input
            v-model="cpf"
            label="CPF"
            mask="###.###.###-##"
            fill-mask
            unmasked-value
            outlined
            class="q-mb-md"
            :rules="[val => val.length === 11 || 'CPF incompleto']"
          >
            <template #prepend>
              <q-icon name="badge" />
            </template>
          </q-input>

          <q-input
            v-model="senha"
            label="Senha"
            :type="mostrarSenha ? 'text' : 'password'"
            outlined
            class="q-mb-md"
            :rules="[val => val.length >= 8 || 'Mínimo 8 caracteres']"
          >
            <template #prepend>
              <q-icon name="lock" />
            </template>
            <template #append>
              <q-icon
                :name="mostrarSenha ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="mostrarSenha = !mostrarSenha"
              />
            </template>
          </q-input>

          <div v-if="erro" class="text-negative text-caption q-mb-md">
            {{ erro }}
          </div>

          <q-btn
            type="submit"
            label="Entrar"
            color="primary"
            class="full-width q-py-sm"
            :loading="carregando"
          />
        </q-form>
      </q-card-section>

      <q-card-section class="text-center q-pt-none">
        <span class="text-grey-7 text-caption">Não tem conta? </span>
        <router-link to="/registrar" class="text-primary text-caption text-weight-bold">
          Cadastre-se
        </router-link>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const cpf = ref('')
const senha = ref('')
const mostrarSenha = ref(false)
const carregando = ref(false)
const erro = ref('')

async function fazerLogin() {
  erro.value = ''
  carregando.value = true
  try {
    const resposta = await axios.post('http://localhost:8000/api/autenticacao/login/', {
      cpf: cpf.value,
      senha: senha.value,
    })
    localStorage.setItem('token', resposta.data.token)
    router.push('/')
  } catch (e) {
    const dados = e.response?.data
    if (dados?.non_field_errors) {
      erro.value = dados.non_field_errors[0]
    } else {
      erro.value = 'Erro ao fazer login. Verifique os dados.'
    }
  } finally {
    carregando.value = false
  }
}
</script>
