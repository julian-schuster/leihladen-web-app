<template>
    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
        <div class="lds-dual-ring"></div>
    </div>
    <div class="container" v-if="!$store.state.isLoading">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title has-text-centered">Suchergebnisse</h1>
                <h2 class="is-size-5 has-text-grey has-text-centered">Suchbegriff: "{{ query }}"</h2>
                <h2 class="is-size-5 has-text-grey has-text-centered">{{ this.products.length }} Artikel</h2>
            </div>
            <div class="column is-12">
                <div class="field">
                    <label class="label">Sortieren nach:</label>
                    <div class="control">
                        <div class="select" style="margin-right:5px">
                            <select v-model="sortBy" @change="sortByCriteria">
                                <option value="date_added">Hinzugefügt am</option>
                                <option value="name">Name</option>
                                <option value="deposit">Kaution</option>
                                <option value="fee">Leihgebühr</option>
                            </select>
                        </div>
                        <div class="select">
                            <select v-model="sortDirection" @change="sortByCriteria">
                                <option value="asc" v-if="sortBy == 'date_added'">Neueste</option>
                                <option value="desc" v-if="sortBy == 'date_added'">Älteste</option>
                                <option value="asc" v-if="sortBy != 'date_added'">Aufsteigend</option>
                                <option value="desc" v-if="sortBy != 'date_added'">Absteigend</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <ProductBox v-for="product in visibleProducts" v-bind:key="product.id" v-bind:product="product" />
            <div class="column is-12">
                <Pagination v-if="products.length > 8" :totalItems="products.length" :itemsPerPage="itemsPerPage"
                    :currentPage="currentPage" :totalPages="totalPages" @input="onPageChange" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox.vue'
import Pagination from '@/components/Pagination.vue'
export default {
    name: 'Search',
    components: {
        ProductBox,
        Pagination
    },
    data() {
        return {
            products: [],
            query: '',
            currentPage: 1,
            itemsPerPage: 8,
            sortBy: 'date_added',
            sortDirection: 'asc'
        }
    },
    mounted() {
        this.$store.commit("setIsLoading", true);
        document.title = 'Suche | Leihladen'

        // url holen
        let url = window.location.search.substring(1)
        let params = new URLSearchParams(url)

        //query aus url holen
        this.query = params.get('query')
        //suchen
        this.performSearch()
    },
    methods: {
        async performSearch() {
            this.$store.commit('setIsLoading', true)
            //Artikel suchen anhand von query
            await axios.post('/api/v1/products/search/', { 'query': this.query })
                .then(response => {
                    this.products = response.data
                    this.$store.commit("setIsLoading", false);
                }).catch(error => {
                    console.log(error);
                })
            this.$store.commit('setIsLoading', false)
            this.sortByCriteria();
        },
        onPageChange(page) {
            this.currentPage = page;
        },
        // Sortieren anhand von Kriterien
        sortByCriteria() {
            let sortFactor = 1;
            if (this.sortDirection === 'desc') { // Wenn die Sortierrichtung absteigend ist, wird der Sortierfaktor negativ gesetzt.
                sortFactor = -1;
            }
            switch (this.sortBy) { // Je nach ausgewähltem Sortierkriterium wird die Liste der Produkte sortiert.
                case 'name':
                    this.products.sort((a, b) => sortFactor * a.name.localeCompare(b.name)); // Sortiert die Produkte nach dem Namen.
                    break;
                case 'deposit':
                    this.products.sort((a, b) => sortFactor * (a.deposit - b.deposit)); // Sortiert die Produkte nach der Kaution.
                    break;
                case 'fee':
                    this.products.sort((a, b) => sortFactor * (a.fee - b.fee)); // Sortiert die Produkte nach der Gebühr.
                    break;
                default:
                    this.products.sort((a, b) => sortFactor * (new Date(b.date_added) - new Date(a.date_added))); // Sortiert die Produkte nach dem Hinzufügungsdatum.
                    break;
            }

            this.currentPage = 1 // Setzt die aktuelle Seite auf die erste Seite, wenn die Sortierung geändert wird.

        },
    },
    watch: {
        totalPages(newTotal, oldTotal) {
            // Überprüft, ob es nur eine Seite gibt und die aktuelle Seite mehr als 1 ist
            if (newTotal === 1 && oldTotal > 1) {
                this.currentPage = 1;
            } else if (this.currentPage > newTotal) {
                this.currentPage = newTotal;
            }
        }
    },
    computed: {
        // Berechnet die Gesamtzahl der Seiten
        totalPages() {
            return Math.ceil(this.products.length / this.itemsPerPage);
        },
        visibleProducts() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            // Gibt eine neue Liste mit den sichtbaren Produkten zurück
            return this.products.slice(start, end);
        }
    }
}

</script>