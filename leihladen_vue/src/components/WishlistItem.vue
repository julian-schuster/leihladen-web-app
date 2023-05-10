<template>
    <tr>
        <td><router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link></td>
        <td class="has-text-centered" style="white-space: nowrap;"><a @click="decrementQuanitity(item)"
                style="padding-right:10px; padding-left:5px; color: red;">-</a>{{ item.quantity }}
            <a @click="incrementQuanitity(item)" style="color:green">+</a>
        </td>

        <td class="has-text-centered">{{ product.quantity }}</td>

        <td>
            <div v-if="product.available == 0" style="color:red" class="has-text-centered"> {{
                product.available }}
            </div>
            <div v-else style="color:green" class="has-text-centered"> {{ product.available }}
            </div>
        </td>
        <td class="has-text-centered">{{ currencyFormatter.format(item.product.deposit) }}</td>
        <td class="has-text-centered">{{ currencyFormatter.format(item.product.fee) }}</td>
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
            products: [],
            product: []
        }
    },
    mounted() {
        this.getProduct()
    },
    methods: {
        getItemTotal(item) {
            return item.quantity
        },
        decrementQuanitity(item) {

            if (!this.product) {
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

            if (!this.product) {
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

            if (item.quantity < this.product.quantity) {
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
        async getProduct() {
            axios
                .get(`/api/v1/products` + this.initialItem.product.get_absolute_url)
                .then((response) => {
                    this.product = response.data;
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
    },
    computed: {
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