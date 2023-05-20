<template>
  <div id="wrapper">
    <nav class="navbar" style="background-color: #398378;">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><img class="image" style="width: 100%; height: 100%;"
            src="@/assets/leihladen_logo.png"></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu"
          @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true" class="burger-icon"></span>
          <span aria-hidden="true" class="burger-icon"></span>
          <span aria-hidden="true" class="burger-icon"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': showMobileMenu }">
        <div class="navbar-start is-hidden-touch">
          <div class="navbar-item">
            <form method="get" action="/search">
              <div class="field has-addons">
                <div class="control">
                  <input type="text" class="input" placeholder="Nach Artikel suchen" maxlength="30" name="query">
                </div>
                <div class="control">
                  <button class="button">
                    <span class="icon">
                      <i class="fas fa-search" style="color:#398378;"></i>
                    </span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
        <!-- Start Mobile Menu Start -->
        <div class="has-text-centered is-hidden-desktop" v-show="showMobileMenu"
          style="margin-top: 10px; margin-bottom: 10px;">
          <form method="get" action="/search">
            <div class="field has-addons" style="justify-content: center;">
              <div class="control">
                <input type="text" class="input" placeholder="Nach Artikel suchen" maxlength="30" name="query">
              </div>
              <div class="control">
                <button class="button">
                  <span class="icon">
                    <i class="fas fa-search" style="color:#398378;"></i>
                  </span>
                </button>
              </div>
            </div>
          </form>
          <hr>
          <div class="is-flex is-justify-content-center" style="display: flex; flex-wrap: wrap;">
            <a v-for="category in categories" :key="category.id" :href="`/${category.name.toLowerCase()}`"
              class="navbar-item">
              <span class="icon" v-if="category.name == 'Alle'"><i class="fas fa-list"></i></span>
              <span class="icon" v-if="category.name == 'Haushalt'" style="color: #FFA500"><i
                  class="fas fa-home"></i></span>
              <span class="icon" v-if="category.name == 'Sonstiges'" style="color: #808080"><i
                  class="fas fa-th"></i></span>
              <span class="icon" v-if="category.name == 'Kinder'" style="color: #FF69B4"><i
                  class="fas fa-child"></i></span>
              <span class="icon" v-if="category.name == 'Spiele'" style="color: #9400D3"><i
                  class="fas fa-gamepad"></i></span>
              <span class="icon" v-if="category.name == 'Büro'" style="color: #4169E1"><i
                  class="fas fa-briefcase"></i></span>
              <span class="icon" v-if="category.name == 'Garten'" style="color: #008000"><i
                  class="fas fa-leaf"></i></span>
              <span class="icon" v-if="category.name == 'Werkzeug'" style="color: #000000"><i
                  class="fas fa-tools"></i></span>
              <span class="icon" v-if="category.name == 'Instrumente'" style="color: #FFD700"><i
                  class="fas fa-guitar"></i></span>
              <span class="icon" v-if="category.name == 'Diverses'" style="color: #808000"><i
                  class="fas fa-question"></i></span>
              <span>{{ category.name }}</span>
            </a>
          </div>
          <hr>
        </div>
        <!-- Ende Mobile Menu -->
        <div class="navbar-end">
          <div class="navbar-item has-text-centered">
            <div class="buttons is-flex is-justify-content-center is-align-items-center">
              <div class="navbar-item has-dropdown is-hoverable is-hidden-touch">
                <div class="dropdown is-hoverable">
                  <div class="dropdown-trigger">
                    <button class="button navbutton" aria-haspopup="true" aria-controls="dropdown-menu4">
                      <span class="icon"><i class="fa fa-folder-open"></i></span>
                      <span>Kategorien</span>
                      <span class="icon is-small">
                        <i class="fas fa-angle-down" aria-hidden="true"></i>
                      </span>
                    </button>
                  </div>
                  <div class="dropdown-menu" id="dropdown-menu4" role="menu">
                    <div class="dropdown-content">
                      <div class="dropdown-item">
                        <a v-for="category in categories" :key="category.id" :href="`/${category.name.toLowerCase()}`"
                          class="navbar-item">
                          <span class="icon" v-if="category.name == 'Alle'"><i class="fas fa-list"></i></span>
                          <span class="icon" v-if="category.name == 'Haushalt'" style="color: #FFA500"><i
                              class="fas fa-home"></i></span>
                          <span class="icon" v-if="category.name == 'Sonstiges'" style="color: #808080"><i
                              class="fas fa-th"></i></span>
                          <span class="icon" v-if="category.name == 'Kinder'" style="color: #FF69B4"><i
                              class="fas fa-child"></i></span>
                          <span class="icon" v-if="category.name == 'Spiele'" style="color: #9400D3"><i
                              class="fas fa-gamepad"></i></span>
                          <span class="icon" v-if="category.name == 'Büro'" style="color: #4169E1"><i
                              class="fas fa-briefcase"></i></span>
                          <span class="icon" v-if="category.name == 'Garten'" style="color: #008000"><i
                              class="fas fa-leaf"></i></span>
                          <span class="icon" v-if="category.name == 'Werkzeug'" style="color: #000000"><i
                              class="fas fa-tools"></i></span>
                          <span class="icon" v-if="category.name == 'Instrumente'" style="color: #FFD700"><i
                              class="fas fa-guitar"></i></span>
                          <span class="icon" v-if="category.name == 'Diverses'" style="color: #808000"><i
                              class="fas fa-question"></i></span>
                          <span>{{ category.name }}</span>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <template v-if="$store.state.isAuthenticated">
                <router-link to="/adminpanel" class="button"> <span class="icon"><i
                      class="fas fa-cog"></i></span><span>Adminpanel</span></router-link>
              </template>
              <template v-else>
                <router-link to="/login" class="button"><span class="icon"><i
                      class="fas fa-user"></i></span><span>Login</span></router-link>
              </template>
              <router-link to="/wishlist" class="button">
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
  <footer class="footer mobile-is-6">
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
              <div class="mb-2"><router-link to="/impressum">Impressum</router-link></div>
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
      categories: [],
    };
  },
  beforeCreate() {
    //LocalStorage initialisieren -> ClientID setzen/holen, Wunschliste holen usw.
    this.$store.commit("initializeStore");
    this.$store.commit("initializeClient");

    //Prüfen ob der Client ein admin token hat
    const token = this.$store.state.token

    //Wenn ja Token in headers setzen -> Wichtig um ihn als Admin zu kennzeichnen!
    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  created() {
    //Bei jedem Seitenaufruf Kategorien holen
    this.getCategories()
  },
  mounted() {
    //Client Wunschliste aus localStorage holen
    this.wishlist = this.$store.state.wishlist
  },
  methods: {
    getCategories() {
      //API Route zum holen aller Kategorien
      axios
        .get(`/api/v1/categorieslight`)
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  computed: {
    //Berechnet Anzahl der Artikel auf der Wunschliste um sie in der navbar anzuzeigen
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
  background-color: rgb(245, 245, 245);
  ;
}

@media screen and (max-width: 768px) {
  .footer {
    font-size: 14px;
  }
}

.navbutton {
  margin-right: 10px;
}

.burger-icon {
  color: white;
}

.input:focus {
  border-color: #398378;
  box-shadow: 0 0 10px 2px rgba(57, 131, 120, 0.5);
}

.category-link {
  margin-right: 10px;
  margin-bottom: 10px;
  margin-top: 8px;
}
</style>
