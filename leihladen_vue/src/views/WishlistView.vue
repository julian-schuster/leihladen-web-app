<template>
    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
        <div class="lds-dual-ring"></div>
    </div>
    <div class="container page-wishlist is-fullheight" v-if="!$store.state.isLoading">
        <div class="columns is-multiline">
            <div class="column is-12 has-text-centered">
                <h1 class="title">Wunschliste</h1>
            </div>
            <div class="column is-12 box">
                <div class="table-container">
                    <table class="table is-fullwidth" v-if="wishlistTotalLength">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Artikel</th>
                                <th class="has-text-centered">Anzahl</th>
                                <th class="has-text-centered">Bestand</th>
                                <th class="has-text-centered">Verfügbar</th>
                                <th class="has-text-centered">Kaution</th>
                                <th class="has-text-centered">Leihgebühr</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <WishlistItem v-for="item in wishlist.items" v-bind:key="item.product.id"
                                v-bind:initialItem="item" v-on:removeFromWishlist="removeFromWishlist" />
                        </tbody>
                    </table>

                    <p v-else> Es befindet sich zurzeit kein Artikel in der Wunschliste</p>
                </div>
            </div>
            <div class="column is-12 box center-box" v-if="wishlistTotalLength">
                <h4 class="subtitle">Zusammenfassung</h4>
                <div>{{ wishlistTotalLength }} Artikel</div>
                <div>
                    Gesamtkaution: {{ currencyFormatter.format(totalDeposit) }}
                </div>
                <div>
                    Gesamtleihgebühr: {{ currencyFormatter.format(totalFee) }}
                </div>
                <hr>
                <p>Bitte beachten Sie, dass Ihre Wunschliste keine Reservierung darstellt und die Verfügbarkeit der Artikel
                    sich kurzfristig ändern kann.</p>
                <p>Die Kaution und Leihgebühr werden nur für verfügbare Artikel erhoben.
                    Sobald Sie einen Artikel zurückgeben, wird Ihre Kaution zurückerstattet.</p>
                <p>Ihre Wunschliste wird erst im System vermerkt, sobald Sie auf 'Wunschliste abschließen' klicken.</p>

                <div> <router-link to="/wishlist/checkout" class="button">
                        <span class="icon"><i class="fas fa-check-circle" style="color:green"></i></span>
                        <span>Wunschliste abschließen</span>
                    </router-link>
                </div>
                <br>
            </div>

        </div>
    </div>
</template>

<script>
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
            },
        }
    },
    mounted() {
        this.wishlist = this.$store.state.wishlist
        document.title = 'Wunschliste | Leihladen'
    },
    methods: {
        // Artikel von Wunschliste entfernen
        removeFromWishlist(item) {
            this.wishlist.items = this.wishlist.items.filter(i => i.product.id !== item.product.id)
        }
    },
    computed: {
        //Berechnet Anzahl der Artikel auf der Wunschliste
        wishlistTotalLength() {
            return this.wishlist.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
        //Berechnet Gesamtkaution
        totalDeposit() {
            return this.wishlist.items.reduce((acc, curVal) => {
                return acc += curVal.product.deposit * curVal.quantity
            }, 0)
        },
        //Berechnet Gesamte Leihgebühr
        totalFee() {
            return this.wishlist.items.reduce((acc, curVal) => {
                return acc += curVal.product.fee * curVal.quantity
            }, 0)
        },
        //Währung formatieren
        currencyFormatter() {
            return new Intl.NumberFormat('de-DE', {
                style: 'currency',
                currency: 'EUR',
                minimumFractionDigits: 2,
            });
        },
    }
}
</script>

<style scoped>
.table-container {
    max-width: 100%;
    overflow-x: auto;
    padding: 0 10px;
}

@media (min-width: 769px) {
    .table-container {
        padding: 0 20px;
    }
}

@media (max-width: 768px) {
    .column {
        padding: 0;
    }

    .center-box {
        text-align: center;
    }
}
</style>