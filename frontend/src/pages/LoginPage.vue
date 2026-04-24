<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
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
                :rules="[val => !!val && val.length === 11 || 'CPF incompleto']"
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
                :rules="[val => !!val && val.length >= 8 || 'Mínimo 8 caracteres']"
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
            <q-btn flat no-caps color="primary" label="Cadastre-se" to="/registrar" class="text-caption text-weight-bold" />
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
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

const API_URL = process.env.API_URL

async function fazerLogin() {
  erro.value = ''
  carregando.value = true
  
  try {
    const resposta = await axios.post(`${API_URL}/api/autenticacao/login/`, {
      cpf: cpf.value,
      senha: senha.value,
    })
    
    // Sucesso
    localStorage.setItem('token', resposta.data.token)
    router.push('/dashboard')
  } catch (e) {
    console.error('Erro de login:', e)
    // Se o backend ainda não estiver pronto, use isto para "pular" o login no Hackathon:
    // router.push('/') 
    
    const dados = e.response?.data
    if (dados?.non_field_errors) {
      erro.value = dados.non_field_errors[0]
    } else if (dados?.detail) {
      erro.value = dados.detail
    } else {
      erro.value = 'Erro ao conectar com o servidor.'
    }
  } finally {
    carregando.value = false
  }
}
</script>