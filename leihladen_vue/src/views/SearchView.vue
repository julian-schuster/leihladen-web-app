<template>
    <div class="container">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Suche</h1>
                <h2 class="is-size-5 has-text-grey">Suchbegriff: "{{ query }}"</h2>
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
        }
    },
    mounted() {
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
                }).catch(error => {
                    console.log(error);
                })
            this.$store.commit('setIsLoading', false)
        },
        onPageChange(page) {
            this.currentPage = page;
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