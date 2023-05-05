<template>
    <tr>
        <td><router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link></td>
        <td class="has-text-centered"><a @click="decrementQuanitity(item)"
                style="padding-right:10px; padding-left:5px; color: red;">-</a>{{ item.quantity }}

            <a @click="incrementQuanitity(item)" style="color:green">+</a>
        </td>
        <td class="has-text-centered">{{ item.product.quantity }}</td>
        <td>
            <span v-for="product in products" :key="product.id">

                <div v-if="item.product.name === product.name">
                    <div v-if="product.available == 0" style="color:red" class="has-text-centered"> {{ product.available }}
                    </div>
                    <div v-else style="color:green" class="has-text-centered"> {{ product.available }}</div>
                </div>
            </span>
        </td>
        <td><button class="delete" @click="removeFromWishlist(item)" style="background-color: red;"></button></td>
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
            const product = this.products.find(p => p.id === item.product.id);
            if (item.quantity < product.quantity) {
                item.quantity += 1
                this.updateWishlist()
            }

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