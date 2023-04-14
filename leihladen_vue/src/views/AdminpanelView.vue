<template>
    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
        <div class="lds-dual-ring"></div>
    </div>
    <div class="container" v-if="!$store.state.isLoading">
        <div class="columns">
            <div class="column is-12">
                <section class="hero is-dark welcome is-small">
                    <div class="hero-body">
                        <div class="container">
                            <h1 class="title">
                                Adminpanel
                            </h1>
                        </div>
                    </div>
                </section>
                <section class="info-tiles">
                    <div class="tile is-ancestor has-text-centered">
                        <div class="tile is-parent">
                            <article class="tile is-child box">
                                <p class="title">{{ wishlistCount }}</p>
                                <p class="subtitle">Wunschlisten</p>
                            </article>
                        </div>
                        <div class="tile is-parent">
                            <article class="tile is-child box">
                                <p class="title">{{ productsTotal }}</p>
                                <p class="subtitle">Artikel</p>
                            </article>
                        </div>
                        <div class="tile is-parent">
                            <article class="tile is-child box">
                                <p class="title">{{ productsAvailable }}</p>
                                <p class="subtitle">Artikel verfügbar</p>
                            </article>
                        </div>
                        <div class="tile is-parent">
                            <article class="tile is-child box">
                                <p class="title">{{ calculateUtilization }}%</p>
                                <p class="subtitle">Auslastung</p>
                            </article>
                        </div>
                    </div>
                </section>
                <div class="columns">
                    <div class="column is-6">
                        <div class="card">
                            <header class="card-header">
                                <p class="card-header-title">
                                    Artikel suchen
                                </p>
                                <a href="#" class="card-header-icon" aria-label="more options">
                                    <span class="icon">
                                        <i class="fa fa-angle-down" aria-hidden="true"></i>
                                    </span>
                                </a>
                            </header>
                            <div class="card-content">
                                <div class="content">
                                    <div class="control has-icons-left has-icons-right">
                                        <input class="input is-large" type="text" placeholder="">
                                        <span class="icon is-medium is-left">
                                            <i class="fa fa-search"></i>
                                        </span>
                                        <span class="icon is-medium is-right">
                                            <i class="fa fa-check"></i>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="column is-6">
                        <div class="card">
                            <header class="card-header">
                                <p class="card-header-title">
                                    Funktionen
                                </p>
                                <a href="#" class="card-header-icon" aria-label="more options">
                                    <span class="icon">
                                        <i class="fa fa-angle-down" aria-hidden="true"></i>
                                    </span>
                                </a>
                            </header>
                            <div class="card-content">
                                <div class="content">
                                    <div class="buttons">
                                        <div class="column is-12">
                                            <router-link to="/wishlist/scan" class="button is-dark">Wunschliste
                                                scannen</router-link>
                                            <button @click="logout()" class="button is-danger">Log out</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Adminpanel',
    data() {
        return {
            wishlistCount: 0,
            productsAvailable: 0,
            productsTotal: 0
        }
    },
    methods: {
        logout() {
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")
            localStorage.removeItem("username")
            localStorage.removeItem("userid")

            this.$store.commit('removeToken')
            this.$router.push('/')
        },
        async getProducts() {
            await axios
                .get(`/api/v1/products`)
                .then((response) => {
                    this.productsTotal = response.data.count;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        async getWishlists() {
            await axios
                .get(`/api/v1/wishlists`)
                .then((response) => {
                    this.wishlistCount = response.data.count;
                    this.$store.commit("setIsLoading", false);
                })
                .catch((error) => {
                    console.log(error);
                });
        }
    },
    mounted() {
        document.title = 'Adminpanel | Leihladen'
        this.$store.commit("setIsLoading", true);
        this.getProducts();
        this.getWishlists();

    },
    computed: {
        calculateUtilization() {
            const utilization = (this.productsTotal - this.productsAvailable) / this.productsTotal * 100;
            return utilization;
        }
    }
}
</script>