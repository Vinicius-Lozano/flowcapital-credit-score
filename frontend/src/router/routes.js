const routes = [
  {
    path: '/login',
    component: () => import('pages/LoginPage.vue'),
  },
  {
    path: '/registrar',
    component: () => import('pages/RegisterPage.vue'),
  },
  {
    path: '/dashboard',
    component: () => import('pages/DashboardPage.vue'),
  },
  {
    path: '/superadmin',
    component: () => import('pages/AdminPage.vue'),
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
