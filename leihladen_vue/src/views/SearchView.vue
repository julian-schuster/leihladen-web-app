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
                                <option value="fee">Leigehbühr</option>
                            </select>
                        </div>
                        <div class="select">
                            <select v-model="sortDirection" @change="sortByCriteria">
                                <option value="asc">Aufsteigend</option>
                                <option value="desc">Absteigend</option>
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

        let url = window.location.search.substring(1)
        let params = new URLSearchParams(url)

        this.query = params.get('query')
        this.performSearch()
    },
    methods: {
        async performSearch() {
            this.$store.commit('setIsLoading', true)

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
        sortByCriteria() {
            let sortFactor = 1;
            if (this.sortDirection === 'desc') {
                sortFactor = -1;
            }
            switch (this.sortBy) {
                case 'name':
                    this.products.sort((a, b) => sortFactor * a.name.localeCompare(b.name));
                    break;
                case 'deposit':
                    this.products.sort((a, b) => sortFactor * (a.deposit - b.deposit));
                    break;
                case 'fee':
                    this.products.sort((a, b) => sortFactor * (a.fee - b.fee));
                    break;
                default:
                    this.products.sort((a, b) => sortFactor * (new Date(b.date_added) - new Date(a.date_added)));
                    break;
            }

            this.currentPage = 1
        },
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
        totalPages() {
            return Math.ceil(this.products.length / this.itemsPerPage);
        },
        visibleProducts() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.products.slice(start, end);
        }
    }
}

</script>