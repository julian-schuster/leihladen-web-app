import {
  createStore
} from 'vuex'

export default createStore({
  state: {
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
    },
    addToWishlist(state, item) {
      const exists = state.wishlist.items.filter(i => i.product.id === item.product.id)

      if (exists.length) {
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      } else {
        state.wishlist.items.push(item)
      }

      localStorage.setItem('wishlist', JSON.stringify(state.wishlist))
    }
  },
  actions: {},
  modules: {}
})