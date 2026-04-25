<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="capital-register-page">
        <div class="grid-overlay"></div>
        <div class="register-wrapper">
          <div class="register-brand">
            <div class="brand-logo">CF</div>

            <h1>Capital Flow</h1>
            <p>
              Crie sua conta e descubra como seu fluxo de renda pode se transformar em crédito.
            </p>

            <div class="brand-points">
              <div>
                <strong>Cadastro simples</strong>
                <span>Comece sua análise em poucos passos</span>
              </div>

              <div>
                <strong>Dados protegidos</strong>
                <span>Usamos apenas o necessário para análise</span>
              </div>

              <div>
                <strong>Crédito justo</strong>
                <span>Modelo pensado para renda variável</span>
              </div>
            </div>
          </div>

          <q-card class="register-card">
            <q-card-section class="text-center q-pb-md">
              <div class="card-badge">Nova conta</div>
              <div class="text-h5 text-weight-bold text-dark q-mt-md">
                Criar cadastro
              </div>
              <div class="text-grey-7 q-mt-xs">
                Preencha seus dados para acessar a plataforma.
              </div>
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
                  class="q-mb-md custom-input"
                  :rules="[(val) => (!!val && val.length === 11) || 'CPF incompleto']"
                >
                  <template #prepend>
                    <q-icon name="badge" color="primary" />
                  </template>
                </q-input>

                <q-input
                  v-model="senha"
                  label="Senha"
                  :type="mostrarSenha ? 'text' : 'password'"
                  outlined
                  class="q-mb-xs custom-input"
                  :rules="[validarSenha]"
                >
                  <template #prepend>
                    <q-icon name="lock" color="primary" />
                  </template>

                  <template #append>
                    <q-icon
                      :name="mostrarSenha ? 'visibility_off' : 'visibility'"
                      class="cursor-pointer"
                      @click="mostrarSenha = !mostrarSenha"
                    />
                  </template>
                </q-input>

                <div class="password-hint">
                  Mínimo 8 caracteres com maiúscula, minúscula, número e símbolo.
                </div>

                <q-input
                  v-model="confirmarSenha"
                  label="Confirmar senha"
                  :type="mostrarSenha ? 'text' : 'password'"
                  outlined
                  class="q-mb-md custom-input"
                  :rules="[(val) => val === senha || 'As senhas não conferem']"
                >
                  <template #prepend>
                    <q-icon name="lock_outline" color="primary" />
                  </template>
                </q-input>

                <div v-if="erro" class="error-box q-mb-md">
                  {{ erro }}
                </div>

                <q-btn
                  type="submit"
                  label="Cadastrar"
                  unelevated
                  no-caps
                  class="full-width primary-gradient-btn q-py-sm"
                  :loading="carregando"
                />
              </q-form>
            </q-card-section>

            <q-card-section class="text-center q-pt-none">
              <span class="text-grey-7 text-caption">Já tem conta? </span>
              <q-btn
                flat
                no-caps
                label="Entrar"
                to="/login"
                class="text-caption text-weight-bold login-link"
              />
            </q-card-section>
          </q-card>
        </div>
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const cpf = ref('')
const senha = ref('')
const confirmarSenha = ref('')
const mostrarSenha = ref(false)
const carregando = ref(false)
const erro = ref('')

const API_URL = process.env.API_URL

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
    const resposta = await axios.post(`${API_URL}/api/autenticacao/registrar/`, {
      cpf: cpf.value,
      senha: senha.value,
      confirmar_senha: confirmarSenha.value,
    })

    if (resposta.data.token) {
      localStorage.setItem('token', resposta.data.token)
    }

    window.location.href = '/#/login'
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

<style scoped>
.grid-overlay {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(37, 99, 235, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37, 99, 235, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}

.capital-register-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 18px;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.38), transparent 35%),
    radial-gradient(circle at bottom right, rgba(22, 163, 74, 0.22), transparent 35%),
    linear-gradient(135deg, #020617, #0f172a);
}

.register-wrapper {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1080px;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 42px;
  align-items: center;
}

.register-brand {
  color: white;
}

.brand-logo {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: linear-gradient(135deg, #2563eb, #22c55e);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 1.25rem;
  margin-bottom: 24px;
  box-shadow: 0 16px 38px rgba(37, 99, 235, 0.35);
}

.register-brand h1 {
  font-size: 3.1rem;
  line-height: 1;
  font-weight: 900;
  margin: 0 0 16px;
}

.register-brand p {
  max-width: 520px;
  font-size: 1.08rem;
  line-height: 1.7;
  color: #cbd5e1;
  margin: 0;
}

.brand-points {
  margin-top: 32px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.brand-points div {
  padding: 16px;
  border-radius: 18px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.22);
}

.brand-points strong {
  display: block;
  color: white;
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.brand-points span {
  color: #cbd5e1;
  font-size: 0.85rem;
  line-height: 1.4;
}

.register-card {
  width: 100%;
  max-width: 460px;
  justify-self: end;
  border-radius: 28px;
  padding-top: 8px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 28px 90px rgba(0, 0, 0, 0.38);
}

.card-badge {
  display: inline-block;
  padding: 7px 13px;
  border-radius: 999px;
  background: #eff6ff;
  color: #2563eb;
  font-weight: 800;
  font-size: 0.78rem;
}

.custom-input :deep(.q-field__control) {
  border-radius: 14px;
}

.password-hint {
  margin: 0 0 16px;
  padding: 10px 12px;
  border-radius: 12px;
  background: #f8fafc;
  color: #64748b;
  font-size: 0.78rem;
  line-height: 1.4;
}

.primary-gradient-btn {
  min-height: 46px;
  border-radius: 14px;
  font-weight: 800;
  color: white;
  background: linear-gradient(135deg, #2563eb, #16a34a);
  box-shadow: 0 14px 32px rgba(37, 99, 235, 0.25);
}

.primary-gradient-btn:hover {
  transform: translateY(-1px);
}

.login-link {
  color: #2563eb;
}

.error-box {
  padding: 12px 14px;
  border-radius: 14px;
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
  font-size: 0.86rem;
  font-weight: 600;
}

@media (max-width: 900px) {
  .register-wrapper {
    grid-template-columns: 1fr;
    gap: 28px;
  }

  .register-card {
    justify-self: center;
  }

  .register-brand {
    text-align: center;
  }

  .brand-logo {
    margin-left: auto;
    margin-right: auto;
  }

  .register-brand p {
    margin-left: auto;
    margin-right: auto;
  }

  .brand-points {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .capital-register-page {
    padding: 24px 14px;
  }

  .register-brand h1 {
    font-size: 2.25rem;
  }

  .register-card {
    border-radius: 22px;
  }
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(110px);
  z-index: 0;
  animation: float 10s ease-in-out infinite;
  pointer-events: none;
}

.blob-1 {
  top: -12%;
  left: -10%;
  width: 500px;
  height: 500px;
  background: rgba(37, 99, 235, 0.18);
}

.blob-2 {
  bottom: -20%;
  right: -12%;
  width: 600px;
  height: 600px;
  background: rgba(22, 163, 74, 0.16);
  animation-delay: -5s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }

  50% {
    transform: translateY(-30px) scale(1.05);
  }
}
</style>
