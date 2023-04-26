<template>
    <div class="box is-multiline">
        <h3>Wunschliste: {{ wishlist_client_id }}</h3>
        <div class="columns is-multiline is-mobile">
            <div class="column is-12">
                <table class="table is-fullwidth is-mobile">
                    <thead>
                        <tr>
                            <th>Artikel</th>
                            <th class="has-text-centered">Anzahl</th>
                            <th class="has-text-centered">Bestand</th>
                            <th class="has-text-centered">Verfügbar</th>
                            <th></th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in  wishlist.items " v-bind:key="item.product.id">
                            <td><router-link :to="item.product.get_absolute_url">{{
                                item.product.name
                            }}</router-link></td>
                            <td class=" has-text-centered">{{ item.quantity }}</td>
                            <td class="has-text-centered">{{ getProductCount(item.product.id) }}</td>
                            <td class="has-text-centered">{{ getProductAvailable(item.product.id) }}</td>
                            <td class="has-text-right"><button class="button is-success is-light"
                                    @click="updateProductAvailability(item.product.id, 1)">Verfügbar
                                    schalten</button></td>
                            <td class="has-text-right"><button class="button is-danger is-light has-text-right"
                                    @click="updateProductAvailability(item.product.id, -1)">Nicht Verfügbar
                                    schalten</button></td>
                        </tr>
                    </tbody>
                </table>
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
            products: []
        }
    },
    mounted() {
        this.wishlist_client_id = this.$route.params.client_id;
        document.title = 'Wunschliste ' + this.wishlist_client_id + '| Leihladen'


        this.getProducts()
        this.getWishlist(this.wishlist_client_id)
    },
    methods: {
        getWishlist() {
            axios.get(`/api/v1/wishlist/${this.wishlist_client_id}/`)
                .then(response => {
                    this.wishlist = JSON.parse(response.data.qr_code_text)
                    this.wishlist.date_added = response.data.date_added
                })
                .catch(error => {
                    console.error(error)
                })
        },
        getProducts() {
            axios
                .get(`/api/v1/products`)
                .then((response) => {
                    this.products = response.data.products
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        getProductAvailable(productId) {
            const product = this.products.find(p => p.id === productId);
            return product ? product.available : '-';
        },
        getProductCount(productId) {
            const product = this.products.find(p => p.id === productId);
            return product ? product.quantity : '-';
        },
        updateProductAvailability(id, value) {
            axios.put(`/api/v1/product/${id}/availability/`, { value: value })
                .then(response => {

                    const updatedProduct = response.data;
                    const index = this.products.findIndex(p => p.id === updatedProduct.id);
                    if (index > -1) {
                        this.products.splice(index, 1, updatedProduct);
                    }
                    const wishlistItem = this.wishlist.items.find(item => item.product.id === updatedProduct.id);
                    if (wishlistItem) {
                        wishlistItem.product = updatedProduct;
                    }

                    toast({
                        message: "Verfügbarkeit für " + response.data.name + " geändert",
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
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
                        duration: 2000,
                        position: "bottom-right",
                    });

                });
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            const formattedDate = `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`;
            return formattedDate;
        },

    },

}
</script>