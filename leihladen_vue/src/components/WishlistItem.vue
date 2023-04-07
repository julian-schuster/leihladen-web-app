<template>
    <tr>
        <td><router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link></td>
        <td>{{ item.quantity }}
            <a @click="decrementQuanitity(item)">-</a>
            <a @click="incrementQuanitity(item)">+</a>
        </td>
        <td># Verfügbar</td>
        <td><button class="delete" @click="removeFromWishlist(item)"></button></td>
    </tr>
</template>

<script>
export default {
    name: 'WishlistItem',
    props: {
        initialItem: Object
    },
    data() {
        return {
            item: this.initialItem
        }
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
        }
    }
}

</script>