<template>
  <q-layout view="hHh Lpr lff" class="bg-dark text-white font-sans">
    <q-header elevated class="bg-dark bg-opacity-90 backdrop-filter blur-5 text-white">
      <q-toolbar class="q-py-md q-px-lg">
        <q-btn flat no-caps dense class="text-h6 text-weight-bolder" to="/">
          <q-icon name="account_balance_wallet" class="q-mr-sm" color="primary" />
          FlowCapital
        </q-btn>
        
        <q-space />

        <div class="row q-gutter-sm">
          <q-btn flat no-caps label="Entrar" to="/login" class="text-weight-bold" />
          <q-btn outline no-caps label="Criar Conta" color="primary" to="/registrar" class="text-weight-bold q-px-md" />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
// Simplifed modern layout with no drawer
</script>

<style>
.bg-opacity-90 {
  background-color: rgba(30, 30, 30, 0.9) !important;
}
.blur-5 {
  backdrop-filter: blur(8px);
}
.font-sans {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
body {
  background: #121212;
}
</style>
