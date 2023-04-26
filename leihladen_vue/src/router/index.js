import {
  createRouter,
  createWebHistory
} from 'vue-router'

import store from '../store'

import HomeView from '../views/HomeView.vue'
import ImpressumView from '../views/ImpressumView.vue'
import ProductView from '../views/ProductView.vue'
import CategoryView from '../views/CategoryView.vue'
import SearchView from '../views/SearchView.vue'
import AdminLoginView from '../views/AdminLoginView.vue'
import AdminpanelView from '../views/AdminpanelView.vue'
import WishlistView from '../views/WishlistView.vue'
import WishlistCheckoutView from '../views/WishlistCheckoutView.vue'
import WishlistScanView from '../views/WishlistScanView.vue'
import WishlistAdminView from '../views/WishlistAdminView.vue'
import ProductCreateView from '../views/ProductCreateView.vue'
import ProductEditView from '../views/ProductEditView.vue'



const routes = [{
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/impressum',
    name: 'impressum',
    component: ImpressumView
  },
  {
    path: '/search',
    name: 'Search',
    component: SearchView
  },
  {
    path: '/wishlist',
    name: 'Wisthlist',
    component: WishlistView
  },
  {
    path: '/wishlist/checkout',
    name: 'WishlistCheckout',
    component: WishlistCheckoutView
  },
  {
    path: '/wishlist/scan',
    name: 'WishlistScan',
    component: WishlistScanView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/wishlist/:client_id',
    name: 'WishlistAdmin',
    component: WishlistAdminView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/login',
    name: 'AdminLogin',
    component: AdminLoginView
  },
  {
    path: '/adminpanel',
    name: 'Adminpanel',
    component: AdminpanelView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/:category_slug/:product_slug',
    name: 'Product',
    component: ProductView
  },
  {
    path: '/:category_slug',
    name: 'Category',
    component: CategoryView
  },
  {
    path: '/product/create',
    name: 'ProductCreate',
    component: ProductCreateView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/:category_slug/:product_slug/edit',
    name: 'ProductEdit',
    component: ProductEditView,
    meta: {
      requireLogin: true
    },
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({
      name: 'AdminLogin',
      query: {
        to: to.path
      }
    })
  } else {
    next()
  }
})

export default router