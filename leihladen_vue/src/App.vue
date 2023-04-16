<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Leihladen</strong></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu"
          @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': showMobileMenu }">
        <div class="navbar-start">
          <div class="navbar-item">
            <form method="get" action="/search">
              <div class="field has-addons">
                <div class="control">
                  <input type="text" class="input" placeholder="Nach Artikel suchen" name="query">
                </div>
                <div class="control">
                  <button class="button is-success">
                    <span class="icon">
                      <i class="fas fa-search"></i>
                    </span>
                  </button>
                </div>
              </div>
            </form>
          </div>
          <div class="navbar-item">
            {{ $store.state.clientId }}
          </div>
        </div>
        <div class="navbar-end">
          <router-link to="/garten" class="navbar-item">Garten</router-link>
          <router-link to="/brettspiele" class="navbar-item">Brettspiele</router-link>
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <router-link to="/adminpanel" class="button is-light">Adminpanel</router-link>
              </template>

              <template v-else>
                <router-link to="/login" class="button is-light">Login</router-link>
              </template>

              <router-link to="/wishlist" class="button is-success">
                <span class="icon"><i class="fas fa-list"></i></span>
                <span>Wunschliste ({{ wishlistTotalLength }})</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <section class="section content">
      <router-view />
    </section>
  </div>
  <footer class="footer has-background-white-ter mobile-is-6">
    <div class="container">
      <div class="columns is-multiline">
        <div class="column is-12">
          <div class="columns is-mobile is-multiline">
            <div class="column is-4  has-text-left">
              <p class="has-text-weight-bold mb-2">Kontakt</p>
              <p><i class="fas fa-map-marker-alt mr-2"></i> Musterstraße 123, 12345 Musterstadt</p>
              <p><i class="fas fa-envelope mr-2"></i> info@leihladen.de</p>
              <p><i class="fas fa-phone mr-2"></i> 0123 / 456 789</p>
            </div>
            <div class="column is-4 has-text-centered">
              <p class="has-text-weight-bold mb-2">Öffnungszeiten</p>
              <p>Fr: 16:00-17:30 Uhr</p>
            </div>
            <div class="column is-4 has-text-right">
              <p class="has-text-weight-bold">For Demonstration Only</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showMobileMenu: false,
      wishlist: {
        items: [],
      },
    };
  },
  beforeCreate() {
    this.$store.commit("initializeStore");
    this.$store.commit("initializeClient");

    const token = this.$store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.wishlist = this.$store.state.wishlist
  },
  computed: {
    wishlistTotalLength() {
      let totalLength = 0;

      for (let i = 0; i < this.wishlist.items.length; i++) {
        totalLength += this.wishlist.items[i].quantity;
      }

      return totalLength;
    },
  },
};
</script>

<style lang="scss">
@import "../node_modules/bulma";

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}

.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}

@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}

body {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

#app {
  flex: 1;
  display: flex;
  flex-direction: column;
}

footer {
  margin-top: auto;
}
</style>
