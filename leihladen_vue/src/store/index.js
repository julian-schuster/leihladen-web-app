import {
  createStore
} from 'vuex'

import {
  v4 as uuidv4
} from 'uuid';

export default createStore({
  state: {
    clientId: '',
    wishlist: {
      items: [],
    },
    isAuthenticated: false,
    token: '',
    isLoading: false
  },
  getters: {},
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('wishlist')) {
        state.wishlist = JSON.parse(localStorage.getItem('wishlist'))
      } else {
        localStorage.setItem('wishlist', JSON.stringify(state.wishlist))
      }

      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    addToWishlist(state, item) {
      const exists = state.wishlist.items.filter(i => i.product.id === item.product.id)

      if (exists.length) {
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      } else {
        state.wishlist.items.push(item)
      }

      localStorage.setItem('wishlist', JSON.stringify(state.wishlist))
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
    },
    initializeClient(state) {
      if (localStorage.getItem('clientId') == '') {
        const uuid = uuidv4()
        localStorage.setItem('clientId', uuid)
      } else {
        state.clientId = localStorage.getItem('clientId')
      }
    },
  },
  actions: {},
  modules: {}
})