<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="flex flex-center bg-grey-2">
        <q-card style="width: 420px; max-width: 95vw" class="shadow-4">
          <q-card-section class="bg-primary text-white text-center q-py-lg">
            <div class="text-h5 text-weight-bold">FlowCapital</div>
            <div class="text-caption q-mt-xs">Crie sua conta</div>
          </q-card-section>

          <q-card-section class="q-pa-lg">
            <q-form @submit.prevent="registrar">
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
                class="q-mb-xs"
                :rules="[validarSenha]"
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

              <div class="text-caption text-grey-6 q-mb-md q-px-sm" style="font-size: 0.75rem; line-height: 1.2">
                Mínimo 8 caracteres com maiúscula, minúscula, número e símbolo (ex: @#$!).
              </div>

              <q-input
                v-model="confirmarSenha"
                label="Confirmar Senha"
                :type="mostrarSenha ? 'text' : 'password'"
                outlined
                class="q-mb-md"
                :rules="[val => val === senha || 'As senhas não conferem']"
              >
                <template #prepend>
                  <q-icon name="lock_outline" />
                </template>
              </q-input>

              <div v-if="erro" class="text-negative text-caption q-mb-md">
                {{ erro }}
              </div>

              <q-btn
                type="submit"
                label="Cadastrar"
                color="primary"
                class="full-width q-py-sm"
                :loading="carregando"
              />
            </q-form>
          </q-card-section>

          <q-card-section class="text-center q-pt-none">
            <span class="text-grey-7 text-caption">Já tem conta? </span>
            <q-btn flat no-caps color="primary" label="Entrar" to="/login" class="text-caption text-weight-bold" />
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
const confirmarSenha = ref('')
const mostrarSenha = ref(false)
const carregando = ref(false)
const erro = ref('')

function validarSenha(val) {
  if (!val || val.length < 8) return 'Mínimo 8 caracteres'
  if (!/[A-Z]/.test(val)) return 'Precisa de uma letra maiúscula'
  if (!/[a-z]/.test(val)) return 'Precisa de uma letra minúscula'
  if (!/\d/.test(val)) return 'Precisa de um número'
  if (!/[!@#$%^&*()\-_=+[\]{};:'",.<>?/\\|`~]/.test(val)) return 'Precisa de um símbolo especial'
  return true
}

async function registrar() {
  erro.value = ''
  carregando.value = true
  try {
    const resposta = await axios.post('http://localhost:8000/api/autenticacao/registrar/', {
      cpf: cpf.value,
      senha: senha.value,
      confirmar_senha: confirmarSenha.value,
    })
    
    if (resposta.data.token) {
        localStorage.setItem('token', resposta.data.token)
        router.push('/dashboard')
    } else {
        router.push('/login')
    }
  } catch (e) {
    console.error(e)
    const dados = e.response?.data
    if (dados?.cpf) {
      erro.value = dados.cpf[0]
    } else if (dados?.senha) {
      erro.value = dados.senha[0]
    } else if (dados?.non_field_errors) {
      erro.value = dados.non_field_errors[0]
    } else {
      erro.value = 'Erro ao cadastrar. Verifique se o servidor está rodando.'
    }
  } finally {
    carregando.value = false
  }
}
</script>