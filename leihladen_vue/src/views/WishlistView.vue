<template>
    <div class="page-wishlist">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Wunschliste</h1>
            </div>

            <div class="column is-12 box">
                <table class="table is-fullwidth" v-if="wishlistTotalLength">
                    <thead>
                        <tr>
                            <th>Artikel</th>
                            <th>Anzahl</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody>
                        <WishlistItem v-for="item in wishlist.items" v-bind:key="item.product.id"
                            v-bind:initialItem="item" />
                    </tbody>
                </table>

                <p v-else> Es befindet sich kein Artikel in der Wunschliste</p>

                <div class="column is-12 box">
                    <h2 class="subtitle">Zusammenfassung</h2>
                    <strong>{{ wishlistTotalLength }} Artikel</strong>
                    <hr>
                    <router-link to="/wishlist/checkout" class="button is-dark">Zum Checkout</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import WishlistItem from '@/components/WishlistItem.vue'

export default {
    name: 'Wishlist',
    components: {
        WishlistItem
    },
    data() {
        return {
            wishlist: {
                items: []
            }
        }
    },
    mounted() {
        this.wishlist = this.$store.state.wishlist
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