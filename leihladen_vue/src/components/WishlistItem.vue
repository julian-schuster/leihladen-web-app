<template>
    <tr>
        <td><router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link></td>
        <td>{{ item.quantity }}</td>
        <td># Verfügbar</td>
        <td><button class="delete"></button></td>
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
        }
    }
}

</script>