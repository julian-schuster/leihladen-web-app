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
                        <div class="tile is-parent" @click="showCard('categories')">
                            <article class="tile is-child box tile-box"
                                :class="{ 'selected': selectedCard === 'categories' }">
                                <p class="title"><i class="fa fa-folder-open" style="color: #a278f0fd;"></i>
                                    {{ this.categories.length }}
                                </p>
                                <p class="subtitle">Kategorien</p>
                            </article>
                        </div>
                    </div>
                </section>

                <div class="columns is-multiline">
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

                                                            <th>ID</th>
                                                            <th>Erstellt am</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(wishlist, index) in paginatedFilteredWishlists"
                                                            :key="index">

                                                            <td><router-link :to="'/wishlist/' + wishlist.client_id">{{
                                                                wishlist.client_id }} </router-link></td>
                                                            <td>{{ new Date(wishlist.date_added).toLocaleString()
                                                            }}</td>
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
                                                <div class="table-container">
                                                    <table class="table is-hoverable is-responsive">
                                                        <thead>
                                                            <tr>
                                                                <th style="width: 15%;">ID</th>
                                                                <th style="width: 60%;">Name</th>
                                                                <th style="width: 10%;">Anzahl</th>
                                                                <th style="width: 15%;"></th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr v-for="(product, index) in paginatedFilteredProducts"
                                                                :key="index">
                                                                <td>{{ product.id }}</td>
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
                                                                    <span @click="deleteProduct(product)"
                                                                        class="delete-wrapper">
                                                                        <i class="fa fa-trash delete-icon"></i>
                                                                    </span>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>


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
                                                            <th style="width: 15%;">ID</th>
                                                            <th style="width: 60%;">Name</th>
                                                            <th style="width: 10%;">Anzahl</th>
                                                            <th style="width: 15%;"></th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(product, index) in paginatedFilteredNotAvailableProducts"
                                                            :key="index">
                                                            <td>{{ product.id }}</td>
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
                                        <div class="card" v-else-if="selectedCard === 'categories'">
                                            <div class="card-content">
                                                <p class="title has-text-centered">Kategorien</p>
                                                <div class="field">
                                                    <p class="control has-icons-left">
                                                        <input class="input" type="text" placeholder="Suche Kategorie"
                                                            v-model="searchCategoriesQuery">
                                                        <span class="icon is-small is-left">
                                                            <i class="fas fa-search"></i>
                                                        </span>
                                                    </p>
                                                </div>
                                                <table class="table is-fullwidth">
                                                    <thead>
                                                        <tr>
                                                            <th>Name</th>
                                                            <th></th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(category, index) in paginatedCategories" :key="index">
                                                            <td>
                                                                <div v-if="!category.editing">
                                                                    <router-link :to="category.name.toLowerCase()">
                                                                        {{ category.name }}
                                                                    </router-link>
                                                                </div>
                                                                <div v-else>
                                                                    <div class="field">
                                                                        <div class="control">
                                                                            <input class="input" type="text" maxlength="30"
                                                                                v-model="category.newName"
                                                                                :placeholder="`${category.name}`">
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </td>
                                                            <td class="has-text-right">
                                                                <div v-if="!category.editing">
                                                                    <a @click="category.editing = true">
                                                                        <i class="fa fa-edit"></i>
                                                                    </a>
                                                                    <span @click="deleteCategory(category)"
                                                                        class="delete-wrapper">
                                                                        <i class="fa fa-trash delete-icon"></i>
                                                                    </span>
                                                                </div>
                                                                <div v-else style="margin-top:10px; white-space: nowrap;">
                                                                    <a @click="updateCategory(category)"
                                                                        style="margin-right: 15px;">
                                                                        <i class="fa fa-check"></i>
                                                                    </a>
                                                                    <a @click="category.editing = false">
                                                                        <i class="fa fa-times"></i>
                                                                    </a>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <Pagination v-if="totalCategoriesPages > 1"
                                                    :totalItems="filteredCategories.length" :itemsPerPage="itemsPerPage"
                                                    :currentPage="currentPage" @input="onPageChange" />
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
                                        <div class="column is-12 has-text-centered">
                                            <span>
                                                <router-link to="/product/create" class="button">
                                                    <span class="icon"><i class="fas fa-plus" style="color: #A9DF9C;"></i>
                                                    </span>
                                                    <span> Artikel hinzufügen</span>
                                                </router-link>
                                            </span>
                                            <span>
                                                <button class="button" @click="showAddCategory = !showAddCategory">
                                                    <span class="icon">
                                                        <i :class="showAddCategory ? 'fas fa-times' : 'fas fa-plus'"
                                                            :style="{ color: showAddCategory ? 'red' : '#a278f0fd' }"></i>
                                                    </span>
                                                    <span>{{ showAddCategory ? 'Abbrechen' : 'Kategorie hinzufügen'
                                                    }}</span>
                                                </button>
                                                <div v-if="showAddCategory">
                                                    <div class="field">
                                                        <label class="label">Kategorienamen eingeben:</label>
                                                        <div class="control">
                                                            <input class="input" type="text" maxlength="30"
                                                                v-model="categoryName">
                                                        </div>
                                                    </div>
                                                    <button class="button" @click="saveCategory"
                                                        :disabled="categoryName && categoryName === ''"><span
                                                            class="icon"><i class="fas fa-save"></i></span>
                                                        <span>Speichern</span>
                                                    </button>
                                                </div>
                                            </span>
                                            <span>
                                                <router-link to="/wishlist/scan" class="button">
                                                    <span class="icon"><i class="fas fa-qrcode"
                                                            style="color: #EFA00B;"></i></span>
                                                    <span>Artikel/Wunschliste Scannen</span>
                                                </router-link>
                                            </span>
                                            <span>
                                                <button @click="logout()" class="button">
                                                    <span class="icon"><i class="fas fa-sign-out-alt"
                                                            style="color: red;"></i></span> <span> Logout</span>
                                                </button>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <br>
                        <div class="card" style=" align-items: center; justify-content: center;">
                            <header class="card-header">
                                <p class="card-header-title is-centered">
                                    Auslastung
                                </p>
                            </header>
                            <div class="card-content">
                                <div class="content">
                                    <div class="title has-text-centered"><i class="fas fa-chart-pie"
                                            style="color: #3498DB;"></i> {{
                                                calculateUtilization }}%</div>
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
            categories: [],
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
            searchCategoriesQuery: '',
            showAddCategory: false,
            categoryName: "",
        }
    },
    methods: {
        saveCategory() {
            // Setze die Flag 'showAddCategory' auf false, um das Formular zum Hinzufügen einer Kategorie auszublenden.
            this.showAddCategory = false;

            // Sende eine POST-Anfrage an die API, um eine neue Kategorie zu erstellen.
            axios
                .post(`/api/v1/category/`, { categoryName: this.categoryName })
                .then((response) => {
                    // Rufe die Methode 'getCategories' auf, um die Liste der Kategorien zu aktualisieren.
                    this.getCategories()

                    //Erfolgsmeldung
                    toast({
                        message: `Kategorie '${this.categoryName}' wurde hinzugefügt.`,
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: "bottom-right",
                    });

                })
                .catch((error) => {
                    console.log(error);
                });
        },

        deleteCategory(category) {
            // Fordere eine Bestätigung vom Benutzer an, bevor die Kategorie gelöscht wird.
            if (confirm(`Sind Sie sicher, dass Sie Kategorie '${category.name}' löschen möchten? ACHTUNG: Alle Artikel in dieser Kategorie werden auch entfernt.`)) {
                // Sende eine DELETE-Anfrage an die API, um die ausgewählte Kategorie zu löschen.
                axios
                    .delete(`/api/v1/category/${category.id}`)
                    .then((response) => {
                        // Rufe die Methode 'getCategories' auf, um die Liste der Kategorien zu aktualisieren.
                        this.getCategories()

                        // Erfolgsmeldung
                        toast({
                            message: `Kategorie '${category.name}' wurde entfernt.`,
                            type: "is-success",
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
                            position: "bottom-right",
                        });
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            }
        },

        updateCategory(category) {
            // Setze die Flag 'editing' auf false, um den Bearbeitungsmodus zu deaktivieren.
            category.editing = false;

            // Sende eine PUT-Anfrage an die API, um den Namen der ausgewählten Kategorie zu aktualisieren.
            axios
                .put(`/api/v1/category/`, { id: category.id, newName: category.newName })
                .then((response) => {
                    // Rufe die Methode 'getCategories' auf, um die Liste der Kategorien zu aktualisieren.
                    this.getCategories()

                    // Erfolgsmeldung
                    toast({
                        message: `Kategorie '${category.name}' wurde zu '${category.newName}' umbenannt.`,
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: "bottom-right",
                    });
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        logout() {
            axios.defaults.headers.common["Authorization"] = ""

            // Entfernen des JWT-Tokens, des Benutzernamens und der Benutzer-ID aus dem lokalen Speicher
            localStorage.removeItem("token")
            localStorage.removeItem("username")
            localStorage.removeItem("userid")

            // Entfernen des Tokens aus dem Vuex Store
            this.$store.commit('removeToken')

            // Umleiten des Benutzers auf die Startseite
            this.$router.push('/')
        },
        async getProducts() {
            await axios
                .get(`/api/v1/products`)
                .then((response) => {
                    this.products = response.data.products

                    // Überprüfen, ob die API-Antwort die Gesamtzahl der Produkte enthält
                    if (response.data.quantity) {
                        this.productsTotal = response.data.quantity;
                    } else {
                        this.productsTotal = 0
                    }

                    // Speichern der Anzahl verfügbarer Produkte
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
                    // Speichern der Anzahl der Wunschlisten des Benutzers
                    this.wishlistCount = response.data.count;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        showCard(card) {
            this.selectedCard = card;
            this.currentPage = 1
        },
        onPageChange(page) {
            this.currentPage = page;
        },
        deleteProduct(product) {
            // Dialog-Box, um zu bestätigen, ob das Produkt wirklich gelöscht werden soll
            if (confirm(`Sind Sie sicher, dass Sie Artikel '${product.name}' löschen möchten?`)) {
                axios
                    .delete(`/api/v1/product/${product.id}`)
                    .then((response) => {
                        console.log(response);

                        // Aktualisieren der Produkte-Liste nach dem Löschen
                        this.products = this.getProducts()

                        // Erfolgsmeldung
                        toast({
                            message: `Artikel '${product.name}' wurde entfernt.`,
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
        },
        async getCategories() {
            await axios
                .get(`/api/v1/categories`)
                .then((response) => {
                    // Kategorien in Variable speichern
                    this.categories = response.data;

                    // Laden-Status auf false setzen
                    this.$store.commit("setIsLoading", false);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
    mounted() {
        // Titel der Seite
        document.title = 'Adminpanel | Leihladen'
        // Laden-Status true setzen
        this.$store.commit("setIsLoading", true);
        // Lädt die Produkte, Wunschlisten und Kategorien
        this.getProducts();
        this.getWishlists();
        this.getCategories();
    },
    watch: {
        // Überwacht die Gesamtzahl der Seiten
        totalPages(newTotal, oldTotal) {
            // Setzt die aktuelle Seite auf 1, wenn nur eine Seite vorhanden ist
            if (newTotal === 1 && oldTotal > 1) {
                this.currentPage = 1;
            }
            // Setzt die aktuelle Seite auf die letzte Seite, wenn die aktuelle Seite größer als die Gesamtzahl ist
            else if (this.currentPage > newTotal) {
                this.currentPage = newTotal;
            }
        }
    },
    computed: {
        // Berechne die Auslastung in Prozent
        calculateUtilization() {
            if (this.productsTotal === 0) {
                return 0;
            } else {

                const utilization = (this.productsTotal - this.productsAvailable) / this.productsTotal * 100;
                return utilization.toFixed(2);
            }
        },
        // Reduziere das Array der Produkte auf die Anzahl ausgeliehener Produkte und gib sie zurück
        calculateBorrowedProducts() {
            return this.products.reduce((borrowedCount, product) => borrowedCount + (product.quantity - product.available), 0);
        },
        filterNotAvailableProducts() {
            // Filtere die Produkte, die nicht verfügbar sind
            return this.products.filter((product) => {
                product.difference = product.quantity - product.available;
                return product.quantity !== product.available;
            });
        },
        filteredWishlists() {
            const searchQuery = this.searchWishlistQuery.toLowerCase();
            this.currentPage = 1

            // Falls kein Suchbegriff vorhanden ist, gib die gesamte Wunschliste zurück
            if (!searchQuery) {
                return this.wishlists
            }

            // Filtere die Wunschliste nach dem Suchbegriff und gib das Ergebnis zurück
            return this.wishlists.filter((wishlist) => {
                // Konvertiere die client_id des Eintrags in Kleinbuchstaben und prüfe, ob der Suchbegriff darin enthalten ist
                return wishlist.client_id.toLowerCase().includes(searchQuery);
            });
        },
        totalWishlistPages() {
            // Anzahl der Seiten für die paginierte Darstellung berechnen
            return Math.ceil(this.filteredWishlists.length / this.itemsPerPage);
        },
        paginatedFilteredWishlists() {
            // Start-Index für das aktuelle Seitenfenster berechnen
            const startIndex = (this.currentPage - 1) * this.itemsPerPage
            // Ausschnitt der gefilterten Wunschlisten zurückgeben
            return this.filteredWishlists.slice(startIndex, startIndex + this.itemsPerPage)
        },
        filteredProducts() {
            const searchQuery = this.searchProductQuery.toLowerCase();
            this.currentPage = 1

            if (!searchQuery) {
                return this.products
            }

            return this.products.filter((product) => {
                // Produkte filtern, deren Name oder ID den Suchbegriff enthält
                return product.name.toLowerCase().includes(searchQuery) || product.id.toLowerCase().includes(searchQuery);
            });

        },
        totalProductPages() {
            // Anzahl der Seiten für die paginierte Darstellung berechnen
            return Math.ceil(this.filteredProducts.length / this.itemsPerPage);
        },
        paginatedFilteredProducts() {
            // Index des ersten Elements auf der aktuellen Seite berechnen
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            // Ausschnitt der Produkte für die aktuelle Seite zurückgeben
            return this.filteredProducts.slice(startIndex, startIndex + this.itemsPerPage);
        },
        filteredNotAvailableProducts() {
            const searchQuery = this.searchNotAvailableProductQuery.toLowerCase();
            this.currentPage = 1;

            if (!searchQuery) {
                // Wenn keine Suche durchgeführt wird, alle nicht verfügbaren Produkte zurückgeben
                return this.filterNotAvailableProducts;
            }

            // Filtern nach Produkten, deren Name oder ID den Suchbegriff enthält
            return this.filterNotAvailableProducts.filter((product) => {
                return product.name.toLowerCase().includes(searchQuery) || product.id.toLowerCase().includes(searchQuery);
            });
        },
        totalNotAvailableProductPages() {
            // Anzahl der Seiten für die paginierte Darstellung berechnen
            return Math.ceil(this.filteredNotAvailableProducts.length / this.itemsPerPage);
        },
        paginatedFilteredNotAvailableProducts() {
            // Berechnen des Startindex für die paginierte Darstellung
            const startIndex = (this.currentPage - 1) * this.itemsPerPage
            // Rückgabe der Produkte für die aktuelle Seite
            return this.filteredNotAvailableProducts.slice(startIndex, startIndex + this.itemsPerPage)
        },
        filteredCategories() {
            const searchQuery = this.searchCategoriesQuery.toLowerCase();
            this.currentPage = 1

            if (!searchQuery) {
                // Wenn keine Suchanfrage vorhanden ist, alle Kategorien zurückgeben
                return this.categories
            }

            // Kategorien filtern, die den Suchbegriff enthalten
            return this.categories.filter((category) => {
                return category.name.toLowerCase().includes(searchQuery);
            });
        },
        totalCategoriesPages() {
            // Anzahl der Seiten für die paginierte Darstellung berechnen
            return Math.ceil(this.filteredCategories.length / this.itemsPerPage);
        },
        paginatedCategories() {
            // Berechnen des Startindex für die paginierte Darstellung
            const startIndex = (this.currentPage - 1) * this.itemsPerPage
            // Rückgabe der Kategorien für die aktuelle Seite
            return this.filteredCategories.slice(startIndex, startIndex + this.itemsPerPage)
        },
    }
}
</script>

<style scoped>
.tile-box:hover {
    transition: 1s;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
    cursor: pointer;

}

.tile-box {
    border: 2px solid transparent;
}

.selected {
    border-color: #398378;
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
    width: 250px;
    margin-right: 7px;
    margin-top: 7px;
}

.buttons .button i {
    margin-left: 0.5em;
}

.button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    white-space: nowrap;
    padding: 0.5rem;
}

.button i {
    width: 1rem;
    height: 1rem;
    margin-right: 0.5rem;
    align-items: center;
}

.product-name {
    white-space: nowrap;
}

a:hover i.fa-check {
    color: green;
}

a:hover i.fa-times {
    color: red;
}

.table-container {
    overflow-x: auto;
}


@media only screen and (max-width: 768px) {
    .table thead tr th {
        font-size: 0.8rem;
        padding: 0.5rem;
    }

    .table tbody tr td {
        font-size: 0.8rem;
        padding: 0.5rem;
    }
}
</style>