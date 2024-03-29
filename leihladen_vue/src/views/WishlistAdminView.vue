<template>
    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
        <div class="lds-dual-ring"></div>
    </div>
    <div class="container" v-if="!$store.state.isLoading">
        <div class="columns is-centered">
            <div class="column is-12">
                <h3 class="has-text-centered">Wunschliste: {{ wishlist_client_id }}</h3>
                <div class="table-container box">
                    <table class="table is-fullwidth">
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
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in wishlist.items" v-bind:key="item.product.id">
                                <td>{{ item.product.id }}</td>
                                <td>
                                    <router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link>
                                </td>
                                <td class="has-text-centered">{{ item.quantity }}</td>
                                <td class="has-text-centered">{{ getProductCount(item.product.id) }}</td>
                                <td class="has-text-centered" v-if="getProductAvailable(item.product.id) == 0"
                                    style="color:red">{{ getProductAvailable(item.product.id) }}</td>
                                <td class="has-text-centered" v-else style="color:green">{{
                                    getProductAvailable(item.product.id) }}</td>
                                <td class="has-text-centered">{{ currencyFormatter.format(item.product.deposit) }}</td>
                                <td class="has-text-centered">{{ currencyFormatter.format(item.product.fee) }}</td>
                                <td class="has-text-right">
                                    <a class="button is-success is-light is-small"
                                        @click="updateProductAvailability(item.product.id, 1)">
                                        <span class="icon">
                                            <i class="fas fa-plus"></i>
                                        </span>
                                    </a>
                                </td>
                                <td class="has-text-right">
                                    <a class="button is-danger is-light is-small"
                                        @click="updateProductAvailability(item.product.id, -1)">
                                        <span class="icon">
                                            <i class="fas fa-minus"></i>
                                        </span>
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
        <hr>
        <div class="box">
            <h4>Verlauf</h4>
            <div v-for="entry in log" :key="entry.product.id" class="log-entry">
                <span class="time">{{ entry.time }}</span>: {{ entry.message }}
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { toast } from 'bulma-toast'

export default {
    name: "WishlistAdmin",
    data() {
        return {
            wishlist: {
                items: [],
                date_added: ''
            },
            wishlist_client_id: '',
            products: [],
            log: []
        }
    },
    mounted() {
        this.$store.commit("setIsLoading", true);
        //client id aus url holen
        this.wishlist_client_id = this.$route.params.client_id;
        document.title = 'Wunschliste ' + this.wishlist_client_id + '| Leihladen'
        //Produkte und Wishlist holen
        this.getProducts()
        this.getWishlist(this.wishlist_client_id)
    },
    computed: {
        //Währung formatieren
        currencyFormatter() {
            return new Intl.NumberFormat('de-DE', {
                style: 'currency',
                currency: 'EUR',
                minimumFractionDigits: 2,
            });
        },
    },
    methods: {
        //Wunschliste des clients mit der client_id holen
        getWishlist() {
            axios.get(`/api/v1/wishlist/${this.wishlist_client_id}/`)
                .then(response => {
                    this.wishlist = JSON.parse(response.data.qr_code_text)
                    this.wishlist.date_added = response.data.date_added
                })
                .catch(error => {
                    console.error(error)
                    this.$router.push("/")
                })
        },
        //Alle Artikel holen
        getProducts() {
            axios
                .get(`/api/v1/products`)
                .then((response) => {
                    this.products = response.data.products
                    this.$store.commit("setIsLoading", false);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        //Verfügbarkeit des Artikels ermitteln
        getProductAvailable(productId) {
            const product = this.products.find(p => p.id === productId);
            return product ? product.available : '-';
        },
        //Stückzahl des Artikels ermitteln
        getProductCount(productId) {
            const product = this.products.find(p => p.id === productId);
            return product ? product.quantity : '-';
        },
        //Verfügbarkeit aktualisieren
        updateProductAvailability(id, value) {
            const product = this.products.find(p => p.id === id);

            if (!product) {
                toast({
                    message: `Dieser Artikel befindet sich nicht mehr im System.`,
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 4000,
                    position: "bottom-right",
                });

                return
            }

            const confirmationMessage = `Möchten Sie die Verfügbarkeit von "${product.name}" ${value > 0 ? 'erhöhen' : 'verringern'}?`;
            if (window.confirm(confirmationMessage)) {
                //Route zum bearbeiten von Verfügbarkeiten eines Artikels
                axios.put(`/api/v1/product/${id}/availability/`, { value: value })
                    .then(response => {
                        const updatedProduct = response.data;
                        //Artikel-Response in this.products finden
                        const index = this.products.findIndex(p => p.id === updatedProduct.id);
                        if (index > -1) {
                            this.products.splice(index, 1, updatedProduct);
                        }
                        const wishlistItem = this.wishlist.items.find(item => item.product.id === updatedProduct.id);
                        if (wishlistItem) {
                            wishlistItem.product = updatedProduct;
                        }

                        //Eintrag für den Verlauf erzeugen
                        const logEntry = {
                            product: updatedProduct,
                            message: `Verfügbarkeit für Artikel "${updatedProduct.name}" um ${Math.abs(value)} ${value > 0 ? 'erhöht' : 'verringert'}.`,
                            time: new Date().toLocaleTimeString()
                        };
                        //Neuer Eintrag auf Verlauf pushen
                        this.log.push(logEntry);

                        toast({
                            message: `Verfügbarkeit für Artikel "${updatedProduct.name}" um ${Math.abs(value)} ${value > 0 ? 'erhöht' : 'verringert'}.`,
                            type: "is-success",
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
                            position: "bottom-right",
                        });

                    })
                    .catch(error => {
                        console.error(error);

                        toast({
                            message: error.response.data.error,
                            type: "is-danger",
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
                            position: "bottom-right",
                        });

                    });
            }
        },
    },
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
}
</style>