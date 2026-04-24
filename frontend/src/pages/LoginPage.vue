<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="capital-login-page">
        <div class="login-wrapper">
          <div class="login-brand">
            <div class="brand-logo">CF</div>

            <h1>Capital Flow</h1>
            <p>
              Crédito inteligente para quem tem renda em movimento.
            </p>

            <div class="brand-points">
              <div>
                <strong>Score alternativo</strong>
                <span>Análise baseada no fluxo da renda</span>
              </div>

              <div>
                <strong>Mais clareza</strong>
                <span>Resultado explicado para o usuário</span>
              </div>

              <div>
                <strong>Mais inclusão</strong>
                <span>Pensado para renda variável</span>
              </div>
            </div>
          </div>

          <q-card class="login-card">
            <q-card-section class="text-center q-pb-md">
              <div class="card-badge">Acesso seguro</div>
              <div class="text-h5 text-weight-bold text-dark q-mt-md">
                Entrar na conta
              </div>
              <div class="text-grey-7 q-mt-xs">
                Acesse para continuar sua análise de crédito.
              </div>
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
                  class="q-mb-md custom-input"
                  :rules="[(val) => (!!val && val.length >= 8) || 'Mínimo 8 caracteres']"
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

                <div v-if="erro" class="error-box q-mb-md">
                  {{ erro }}
                </div>

                <q-btn
                  type="submit"
                  label="Entrar"
                  unelevated
                  no-caps
                  class="full-width primary-gradient-btn q-py-sm"
                  :loading="carregando"
                />
              </q-form>
            </q-card-section>

            <q-card-section class="text-center q-pt-none">
              <span class="text-grey-7 text-caption">Não tem conta? </span>
              <q-btn
                flat
                no-caps
                label="Cadastre-se"
                to="/registrar"
                class="text-caption text-weight-bold register-link"
              />
            </q-card-section>
          </q-card>
        </div>
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
    console.error('Erro de login:', e)

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

<style scoped>
.capital-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 18px;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.38), transparent 35%),
    radial-gradient(circle at bottom right, rgba(22, 163, 74, 0.22), transparent 35%),
    linear-gradient(135deg, #020617, #0f172a);
}

.login-wrapper {
  width: 100%;
  max-width: 1080px;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 42px;
  align-items: center;
}

.login-brand {
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

.login-brand h1 {
  font-size: 3.1rem;
  line-height: 1;
  font-weight: 900;
  margin: 0 0 16px;
}

.login-brand p {
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

.login-card {
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

.register-link {
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
  .login-wrapper {
    grid-template-columns: 1fr;
    gap: 28px;
  }

  .login-card {
    justify-self: center;
  }

  .login-brand {
    text-align: center;
  }

  .brand-logo {
    margin-left: auto;
    margin-right: auto;
  }

  .login-brand p {
    margin-left: auto;
    margin-right: auto;
  }

  .brand-points {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .capital-login-page {
    padding: 24px 14px;
  }

  .login-brand h1 {
    font-size: 2.25rem;
  }

  .login-card {
    border-radius: 22px;
  }
}
</style>
