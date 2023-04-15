<template>
    <tr>
        <td><router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link></td>
        <td>{{ item.quantity }}
            <a @click="decrementQuanitity(item)">-</a>
            <a @click="incrementQuanitity(item)">+</a>
        </td>
        <td>
            <span v-for="product in products" :key="product.id">
                <span v-if="item.product.name === product.name">
                    {{ product.available }}</span>
            </span>
        </td>
        <td><button class="delete" @click="removeFromWishlist(item)"></button></td>
    </tr>
</template>

<script>
import axios from 'axios'

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
            item.quantity -= 1
            if (item.quantity === 0) {
                this.$emit('removeFromWishlist', item)
            }
            this.updateWishlist()
        },
        incrementQuanitity(item) {
            item.quantity += 1
            this.updateWishlist()
        },
        updateWishlist() {
            localStorage.setItem('wishlist', JSON.stringify(this.$store.state.wishlist))
        },
        removeFromWishlist(item) {
            this.$emit('removeFromWishlist', item)
            this.updateWishlist()
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
    }
}

</script>