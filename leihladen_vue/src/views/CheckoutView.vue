<template>
    <div class="page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Fertige Wunschliste</h1>
            </div>

            <div class="column is-12 box">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Artikel</th>
                            <th>Stückzahl</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="item in wishlist.items" v-bind:key="item.product.id">
                            <td>{{ item.product.name }}</td>
                            <td>{{ item.quantity }}</td>
                        </tr>
                    </tbody>

                    <tfoot>
                        <tr>
                            <td></td>
                            <td>{{ wishlistTotalLength }}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
            <div class="column is-12 box">
                <h2 class="subtitle">QR-Code</h2>
                <canvas ref="qrcode"></canvas>
                <p class="has-text-grey mb-4">Bitte zeigen Sie diesen QR-Code entweder ausgedruckt oder auf Ihrem Smartphone
                    im Leihladen vor.</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import QRCode from 'qrcode'

export default {
    name: 'Checkout',
    components: {
        QRCode
    },
    data() {
        return {
            wishlist: {
                items: []
            },
            clientId: '',
            hasWishlist: false
        }
    },
    mounted() {
        document.title = 'Wunschliste Abschluss | Leihladen'

        this.wishlist = this.$store.state.wishlist
        this.clientId = this.$store.state.clientId

        const qrCodeText = JSON.stringify(this.wishlist)

        this.createQRCode(qrCodeText)
        this.createWishlist(qrCodeText)

    },
    methods: {
        getItemQuantity(item) {
            return item.quantity
        },
        createQRCode(qrCodeText) {
            QRCode.toCanvas(this.$refs.qrcode, qrCodeText, function (error) {
                if (error) console.error(error)
            })
        },
        createWishlist(qrCodeText) {
            axios.post('/api/v1/wishlist/', { qr_code_text: qrCodeText, client_id: this.clientId })
                .then(response => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.error(error)
                })
        },
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