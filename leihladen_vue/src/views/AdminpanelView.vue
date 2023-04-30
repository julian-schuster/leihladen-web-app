<template>
    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
        <div class="lds-dual-ring"></div>
    </div>
    <div class="container" v-if="!$store.state.isLoading">
        <div class="columns">
            <div class="column is-12">
                <section class="hero welcome is-small">
                    <div class="hero-body">
                        <div class="container">
                            <h1 class="title has-text-centered">
                                Adminpanel
                            </h1>
                        </div>
                    </div>
                </section>
                <section class="info-tiles">
                    <div class="tile is-ancestor has-text-centered">
                        <div class="tile is-parent" @click="showCard('wishlist')">
                            <article class="tile is-child box tile-box"
                                :class="{ 'selected': selectedCard === 'wishlist' }">
                                <p class="title"><i class="fas fa-list" style="color: #EFA00B;"></i> {{ wishlistCount }}</p>
                                <p class="subtitle">Wunschlisten</p>
                            </article>
                        </div>
                        <div class="tile is-parent" @click="showCard('productsTotal')">
                            <article class="tile is-child box tile-box"
                                :class="{ 'selected': selectedCard === 'productsTotal' }">
                                <p class="title"><i class="fas fa-box" style="color: #A9DF9C;"></i> {{ productsTotal }}</p>
                                <p class="subtitle">Artikel</p>
                            </article>
                        </div>
                        <div class="tile is-parent" @click="showCard('productsNotAvailable')">
                            <article class="tile is-child box tile-box"
                                :class="{ 'selected': selectedCard === 'productsNotAvailable' }">
                                <p class="title"><i class="fas fa-hand-holding" style="color: #FF5733;"></i> {{
                                    calculateBorrowedProducts }}</p>
                                <p class="subtitle">Artikel ausgeliehen</p>
                            </article>
                        </div>
                        <div class="tile is-parent">
                            <article class="tile is-child box ">
                                <p class="title"><i class="fas fa-chart-pie" style="color: #3498DB;"></i> {{
                                    calculateUtilization }}%</p>
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
                                                <p class="title has-text-centered">Wunschlisten</p>
                                                <div class="field">
                                                    <p class="control has-icons-left">
                                                        <input class="input" type="text" placeholder="Suche Wunschliste"
                                                            v-model="searchWishlistQuery">
                                                        <span class="icon is-small is-left">
                                                            <i class="fas fa-search"></i>
                                                        </span>
                                                    </p>
                                                </div>
                                                <table class="table is-fullwidth">
                                                    <thead>
                                                        <tr>
                                                            <th>id</th>
                                                            <th>client_id</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(wishlist, index) in paginatedFilteredWishlists"
                                                            :key="index">
                                                            <td>{{ wishlist.id }}</td>
                                                            <td><router-link :to="'/wishlist/' + wishlist.client_id">{{
                                                                wishlist.client_id }}</router-link></td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <Pagination v-if="totalWishlistPages > 1"
                                                    :totalItems="filteredWishlists.length" :itemsPerPage="itemsPerPage"
                                                    :currentPage="currentPage" @input="onPageChange" />
                                            </div>
                                        </div>
                                        <div class="card" v-else-if="selectedCard === 'productsTotal'">
                                            <div class="card-content">
                                                <p class="title has-text-centered">Artikel</p>
                                                <div class="field">
                                                    <p class="control has-icons-left">
                                                        <input class="input" type="text" placeholder="Suche Artikel"
                                                            v-model="searchProductQuery">
                                                        <span class="icon is-small is-left">
                                                            <i class="fas fa-search"></i>
                                                        </span>
                                                    </p>
                                                </div>
                                                <table class="table is-fullwidth">
                                                    <thead>
                                                        <tr>
                                                            <th>Name</th>
                                                            <th>Anzahl</th>
                                                            <th></th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(product, index) in paginatedFilteredProducts"
                                                            :key="index">
                                                            <td>
                                                                <router-link v-bind:to="product.get_absolute_url">
                                                                    <div class="product-name">{{ product.name }}</div>
                                                                </router-link>
                                                            </td>
                                                            <td>{{ product.quantity }}</td>
                                                            <td class="has-text-right">
                                                                <router-link :to="product.get_absolute_url + 'edit'">
                                                                    <i class="fa fa-edit"></i>
                                                                </router-link>

                                                                <span @click="deleteProduct(product.id)"
                                                                    class="delete-wrapper">
                                                                    <i class="fa fa-trash delete-icon"></i>
                                                                </span>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <Pagination v-if="totalProductPages > 1"
                                                    :totalItems="filteredProducts.length" :itemsPerPage="itemsPerPage"
                                                    :currentPage="currentPage" @input="onPageChange" />
                                            </div>
                                        </div>
                                        <div class="card" v-else-if="selectedCard === 'productsNotAvailable'">
                                            <div class="card-content">
                                                <p class="title has-text-centered">Ausgeliehene Artikel</p>
                                                <div class="field">
                                                    <p class="control has-icons-left">
                                                        <input class="input" type="text" placeholder="Suche Artikel"
                                                            v-model="searchNotAvailableProductQuery">
                                                        <span class="icon is-small is-left">
                                                            <i class="fas fa-search"></i>
                                                        </span>
                                                    </p>
                                                </div>
                                                <table class="table is-fullwidth">
                                                    <thead>
                                                        <tr>
                                                            <th>Artikel</th>
                                                            <th>Anzahl</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(product, index) in paginatedFilteredNotAvailableProducts"
                                                            :key="index">
                                                            <td> <router-link v-bind:to="product.get_absolute_url">
                                                                    <div class="product-name">{{ product.name }}</div>
                                                                </router-link>
                                                            </td>
                                                            <td>{{ product.difference }}</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <Pagination v-if="totalNotAvailableProductPages > 1"
                                                    :totalItems="filterNotAvailableProducts.length"
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
                                <p class="card-header-title is-centered">
                                    Funktionen
                                </p>
                            </header>
                            <div class="card-content">
                                <div class="content">
                                    <div class="buttons">
                                        <div class="column is-12">
                                            <router-link to="/product/create" class="button">
                                                <span class="icon"><i class="fas fa-plus" style="color: green;"></i> </span>
                                                <span> Artikel hinzufügen</span>
                                            </router-link>
                                            <router-link to="/wishlist/scan" class="button">
                                                <span class="icon"><i class="fas fa-qrcode" style="color: blue;"></i></span>
                                                <span>Wunschliste Scannen</span>
                                            </router-link>
                                            <button @click="logout()" class="button">
                                                <span class="icon"><i class="fas fa-sign-out-alt"
                                                        style="color: red;"></i></span> <span> Logout</span>
                                            </button>
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
import { toast } from "bulma-toast";

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
            itemsPerPage: 5,
            searchWishlistQuery: '',
            searchProductQuery: '',
            searchNotAvailableProductQuery: '',
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
                    if (response.data.quantity) {
                        this.productsTotal = response.data.quantity;
                    } else {
                        this.productsTotal = 0
                    }
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
        deleteProduct(id) {
            if (confirm("Sind Sie sicher, dass Sie dieses Produkt löschen möchten?")) {
                axios
                    .delete(`/api/v1/product/${id}`)
                    .then((response) => {
                        console.log(response);

                        this.products = this.products.filter(product => product.id !== id);

                        toast({
                            message: "Artikel wurde entfernt",
                            type: "is-success",
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: "bottom-right",
                        });
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            }
        }
    },
    mounted() {
        document.title = 'Adminpanel | Leihladen'
        this.$store.commit("setIsLoading", true);
        this.getProducts();
        this.getWishlists();
    },
    watch: {
        totalPages(newTotal, oldTotal) {
            if (newTotal === 1 && oldTotal > 1) {
                this.currentPage = 1;
            } else if (this.currentPage > newTotal) {
                this.currentPage = newTotal;
            }
        }
    },
    computed: {
        calculateUtilization() {
            if (this.productsTotal === 0) {
                return 0;
            } else {
                const utilization = (this.productsTotal - this.productsAvailable) / this.productsTotal * 100;
                return utilization.toFixed(2);
            }
        },
        calculateBorrowedProducts() {
            let borrowedCount = 0;
            this.products.forEach((product) => {
                borrowedCount += product.quantity - product.available;
            });
            return borrowedCount;
        },
        filterNotAvailableProducts() {
            return this.products.filter((product) => {
                // Differenz zwischen count und available berechnen
                product.difference = product.quantity - product.available;
                // Produkt zurückgeben, wenn count und available unterschiedlich sind
                return product.quantity !== product.available;
            });
        },
        filteredWishlists() {
            const searchQuery = this.searchWishlistQuery.toLowerCase();
            this.currentPage = 1

            if (!searchQuery) {
                return this.wishlists
            }

            return this.wishlists.filter((wishlist) => {
                return wishlist.client_id.toLowerCase().includes(searchQuery);
            });
        },
        totalWishlistPages() {
            return Math.ceil(this.filteredWishlists.length / this.itemsPerPage);
        },
        paginatedFilteredWishlists() {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage
            return this.filteredWishlists.slice(startIndex, startIndex + this.itemsPerPage)
        },
        filteredProducts() {
            const searchQuery = this.searchProductQuery.toLowerCase();
            this.currentPage = 1

            if (!searchQuery) {
                return this.products
            }

            return this.products.filter((product) => {
                return product.name.toLowerCase().includes(searchQuery);
            });
        },
        totalProductPages() {
            return Math.ceil(this.filteredProducts.length / this.itemsPerPage);
        },
        paginatedFilteredProducts() {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage
            return this.filteredProducts.slice(startIndex, startIndex + this.itemsPerPage)
        },
        filteredNotAvailableProducts() {
            const searchQuery = this.searchNotAvailableProductQuery.toLowerCase();
            this.currentPage = 1

            if (!searchQuery) {
                return this.filterNotAvailableProducts
            }

            return this.filterNotAvailableProducts.filter((product) => {
                return product.name.toLowerCase().includes(searchQuery);
            });
        },
        totalNotAvailableProductPages() {
            return Math.ceil(this.filteredNotAvailableProducts.length / this.itemsPerPage);
        },
        paginatedFilteredNotAvailableProducts() {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage
            return this.filteredNotAvailableProducts.slice(startIndex, startIndex + this.itemsPerPage)
        },
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

.selected {
    background-color: #76d1cd;
}

.delete-icon:hover {
    color: red;
    cursor: pointer;
}

.delete-wrapper {
    margin-left: 10px;
}

.buttons .button {
    display: inline-flex;
    align-items: center;
}

.buttons .button i {
    margin-left: 0.5em;
}

.product-name {
    word-break: break-all;
}
</style>