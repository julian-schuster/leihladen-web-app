<template>
    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
        <div class="lds-dual-ring"></div>
    </div>
    <div class="container" v-if="!$store.state.isLoading">
        <div class="columns">
            <div class="column is-12">
                <section class="hero welcome is-small ">
                    <div class="hero-body">
                        <div class="container">
                            <h1 class="title ">
                                Adminpanel
                            </h1>
                        </div>
                    </div>
                </section>
                <section class="info-tiles">
                    <div class="tile is-ancestor has-text-centered">
                        <div class="tile is-parent " @click="showCard('wishlist')">
                            <article class="tile is-child box tile-box">
                                <p class="title">{{ wishlistCount }}</p>
                                <p class="subtitle">Wunschlisten</p>
                            </article>
                        </div>
                        <div class="tile is-parent" @click="showCard('productsTotal')">
                            <article class="tile is-child box tile-box">
                                <p class="title">{{ productsTotal }}</p>
                                <p class="subtitle">Artikel</p>
                            </article>
                        </div>
                        <div class="tile is-parent" @click="showCard('productsNotAvailable')">
                            <article class="tile is-child box tile-box">
                                <p class="title">{{ calculateBorrowedProducts }}</p>
                                <p class="subtitle">Artikel ausgeliehen</p>
                            </article>
                        </div>
                        <div class="tile is-parent">
                            <article class="tile is-child box ">
                                <p class="title">{{ calculateUtilization }}%</p>
                                <p class="subtitle">Auslastung</p>
                            </article>
                        </div>
                    </div>
                </section>
                <div class="columns">
                    <div class="column is-6">
                        <section class="info-tiles">
                            <div>
                                <div class="columns">
                                    <div class="column is-12">
                                        <div class="card" v-if="selectedCard === 'wishlist'">
                                            <div class="card-content">
                                                <p class="title">Wunschlisten</p>
                                                <table class="table is-fullwidth">
                                                    <thead>
                                                        <tr>
                                                            <th>id</th>
                                                            <th>client_id</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(wishlist, index) in paginatedWishlists(currentPage)"
                                                            :key="index">
                                                            <td>{{ wishlist.id }}</td>
                                                            <td>{{ wishlist.client_id }}</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <Pagination :totalItems="wishlists.length" :itemsPerPage="itemsPerPage"
                                                    :currentPage="currentPage" @input="onPageChange" />
                                            </div>
                                        </div>
                                        <div class="card" v-else-if="selectedCard === 'productsTotal'">
                                            <div class="card-content">
                                                <p class="title">Artikel</p>
                                                <table class="table is-fullwidth">
                                                    <thead>
                                                        <tr>
                                                            <th>Name</th>
                                                            <th>Anzahl</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(product, index) in paginatedProducts(currentPage)"
                                                            :key="index">
                                                            <td> <router-link v-bind:to="product.get_absolute_url">{{
                                                                product.name }}</router-link>
                                                            </td>
                                                            <td>{{ product.quantity }}</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <Pagination :totalItems="products.length" :itemsPerPage="itemsPerPage"
                                                    :currentPage="currentPage" @input="onPageChange" />
                                            </div>
                                        </div>
                                        <div class="card" v-else-if="selectedCard === 'productsNotAvailable'">
                                            <div class="card-content">
                                                <p class="title">Ausgeliehene Artikel</p>
                                                <table class="table is-fullwidth">
                                                    <thead>
                                                        <tr>
                                                            <th>Artikel</th>
                                                            <th>Anzahl</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(product, index) in paginatedBorrowedProducts(currentPage, filteredProducts)"
                                                            :key="index">
                                                            <td> <router-link v-bind:to="product.get_absolute_url">{{
                                                                product.name }}</router-link>
                                                            </td>
                                                            <td>{{ product.difference }}</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <Pagination :totalItems="filteredProducts.length"
                                                    :itemsPerPage="itemsPerPage" :currentPage="currentPage"
                                                    @input="onPageChange" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                    <div class="column is-6">
                        <div class="card">
                            <header class="card-header">
                                <p class="card-header-title">
                                    Funktionen
                                </p>
                            </header>
                            <div class="card-content">
                                <div class="content">
                                    <div class="buttons">
                                        <div class="column is-12">

                                            <router-link to="/product/create" class="button">
                                                Artikel hinzufügen</router-link>
                                            <router-link to="#" class="button">
                                                Artikel entfernen</router-link>
                                            <router-link to="#" class="button">
                                                Artikel bearbeiten</router-link>
                                            <router-link to="/wishlist/scan" class="button">
                                                Wunschliste Scannen</router-link>
                                            <button @click="logout()" class="button">Logout</button>
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
import Pagination from '@/components/Pagination';

export default {
    name: 'Adminpanel',
    components: {
        Pagination
    },
    data() {
        return {
            products: [],
            wishlists: [],
            wishlistCount: 0,
            productsAvailable: 0,
            productsNotAvailable: 0,
            productsTotal: 0,
            selectedCard: 'wishlist',
            currentPage: 1,
            itemsPerPage: 3
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
                    this.products = response.data.products
                    this.productsTotal = response.data.quantity;
                    this.productsAvailable = response.data.available_count
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        async getWishlists() {
            await axios
                .get(`/api/v1/wishlists`)
                .then((response) => {
                    this.wishlists = response.data.wishlists;
                    this.wishlistCount = response.data.count;
                    this.$store.commit("setIsLoading", false);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        showCard(card) {
            this.selectedCard = card;
            this.currentPage = 1
        },
        paginatedWishlists(page) {
            const startIndex = (page - 1) * this.itemsPerPage;
            return this.wishlists.slice(startIndex, startIndex + this.itemsPerPage);
        },
        paginatedProducts(page) {
            const startIndex = (page - 1) * this.itemsPerPage;
            return this.products.slice(startIndex, startIndex + this.itemsPerPage);
        },
        paginatedBorrowedProducts(page, borrowedProducts) {
            const startIndex = (page - 1) * this.itemsPerPage;
            return borrowedProducts.slice(startIndex, startIndex + this.itemsPerPage);
        },
        onPageChange(page) {
            this.currentPage = page;
        },
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
            return utilization.toFixed(2);
        },
        calculateBorrowedProducts() {
            let borrowedCount = 0;
            this.products.forEach((product) => {
                borrowedCount += product.quantity - product.available;
            });
            return borrowedCount;
        },
        filteredProducts() {
            return this.products.filter((product) => {
                // Differenz zwischen count und available berechnen
                product.difference = product.quantity - product.available;
                // Produkt zurückgeben, wenn count und available unterschiedlich sind
                return product.quantity !== product.available;
            });
        }
    }
}
</script>

<style scoped>
.tile-box:hover {
    background-color: #76d1cd;
    transition: 1s;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}
</style>