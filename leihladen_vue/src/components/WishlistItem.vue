<template>
    <tr>
        <td><router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link></td>
        <td class="has-text-centered"><a @click="decrementQuanitity(item)"
                style="padding-right:10px; padding-left:5px; color: red;">-</a>{{ item.quantity }}
            <a @click="incrementQuanitity(item)" style="color:green">+</a>
        </td>
        <td class="has-text-centered">{{ getProductCount(item.product.id) }}</td>
        <td>
            <div v-if="getProductAvailable(item.product.id) == 0" style="color:red" class="has-text-centered"> {{
                getProductAvailable(item.product.id) }}
            </div>
            <div v-else style="color:green" class="has-text-centered"> {{ getProductAvailable(item.product.id) }}
            </div>
        </td>
        <td><button class="delete" @click="removeFromWishlist(item)" style="background-color: red;"></button></td>
    </tr>
</template>

<script>
import axios from 'axios'
import { toast } from "bulma-toast";

export default {
    name: 'WishlistItem',
    props: {
        initialItem: Object
    },
    data() {
        return {
            item: this.initialItem,
            products: []
        }
    },
    mounted() {
        this.getProducts()
    },
    methods: {
        getItemTotal(item) {
            return item.quantity
        },
        decrementQuanitity(item) {
            const product = this.products.find(p => p.id === item.product.id);

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

            item.quantity -= 1
            if (item.quantity === 0) {
                this.$emit('removeFromWishlist', item)

                toast({
                    message: `"${item.product.name}" wurde von Ihrer Wunschliste entfernt`,
                    type: "is-success",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 4000,
                    position: "bottom-right",
                });

            }
            this.updateWishlist()

            toast({
                message: `Anzahl von Artikel "${item.product.name}" um 1 verringert.`,
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 4000,
                position: "bottom-right",
            });

        },
        incrementQuanitity(item) {
            const product = this.products.find(p => p.id === item.product.id);

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

            if (item.quantity < product.quantity) {
                item.quantity += 1
                this.updateWishlist()

                toast({
                    message: `Anzahl von Artikel "${item.product.name}" um 1 erhöht.`,
                    type: "is-success",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 4000,
                    position: "bottom-right",
                });
            }

        },
        updateWishlist() {
            localStorage.setItem('wishlist', JSON.stringify(this.$store.state.wishlist))
        },
        removeFromWishlist(item) {
            const confirmationMessage = `Möchten Sie den Artikel "${item.product.name}" wirklich von Ihrer Wunschliste entfernen?`;
            if (window.confirm(confirmationMessage)) {
                this.$emit('removeFromWishlist', item)
                this.updateWishlist()
                toast({
                    message: `"${item.product.name}" wurde von Ihrer Wunschliste entfernt`,
                    type: "is-success",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 4000,
                    position: "bottom-right",
                });
            }
        },
        async getProducts() {
            await axios
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
    }
}

</script>