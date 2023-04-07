<template>
    <div class="page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Fertige Wunschliste</h1>
            </div>

            <div class="column is-12 box">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Artikel</th>
                            <th>Stückzahl</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="item in wishlist.items" v-bind:key="item.product.id">
                            <td>{{ item.product.name }}</td>
                            <td>{{ item.quantity }}</td>
                        </tr>
                    </tbody>

                    <tfoot>
                        <tr>
                            <td></td>
                            <td>{{ wishlistTotalLength }}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
            <div class="column is-12 box">
                <h2 class="subtitle">QR-Code</h2>
                <p class="has-text-grey mb-4">Bitte zeigen Sie diesen QR-Code entweder ausgedruckt oder auf Ihrem Smartphone
                    im Leihladen vor.</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Checkout',
    data() {
        return {
            wishlist: {
                items: []
            },
            qrcode: Object,
        }
    },
    mounted() {
        document.title = 'Wunschliste Abschluss | Leihladen'

        this.wishlist = this.$store.state.wishlist
    },
    methods: {
        getItemQuantity(item) {
            return item.quantity
        }
    },
    computed: {
        wishlistTotalLength() {
            return this.wishlist.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        }
    }
}
</script>