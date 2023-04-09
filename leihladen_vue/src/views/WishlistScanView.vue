<template>
    <div class="page-wishlist">
        <div class="columns is-multiline is-mobile is-centered">
            <div class="column is-12">
                <h1 class="title">Wunschliste Scannen</h1>
            </div>
            <div class="column is-6 is-centered">
                <div class="box">
                    <p class="error">{{ error }}</p>
                    <qrcode-stream @init="onInit" @decode="onDecode">
                        <div class="loading-indicator" v-if="loading">
                            Wird geladen...
                        </div>
                    </qrcode-stream>
                </div>
            </div>
            <table class="table is-fullwidth">
                <thead>
                    <tr>
                        <th>Artikel</th>
                        <th>Stückzahl</th>
                        <th>Status</th>
                        <th>Verfügbarkeit ändern</th>
                    </tr>
                </thead>
                <tbody>

                    <tr v-for="item in wishlist.items" v-bind:key="item.product.id">

                        <td>{{ item.product.name }}</td>
                        <td>{{ item.quantity }}</td>
                        <td># Verfügbar</td>
                        <td><button>Verfügbar schalten</button><button>Nicht Verfügbar schalten</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import { QrcodeStream } from 'vue3-qrcode-reader'
import WishlistItem from '@/components/WishlistItem.vue'
import axios from 'axios'

export default {
    name: 'WishlistScan',
    components: {
        QrcodeStream,
        WishlistItem
    },
    data() {
        return {
            wishlist: {
                items: []
            },
            loading: false,
            error: '',
        }
    },
    mounted() {
        document.title = 'Wunschliste Scan | Leihladen'
    },
    methods: {
        onDecode(decodedString) {
            const client_id = decodedString
            axios.get(`/api/v1/wishlist/${client_id}/`)
                .then(response => {
                    const data = JSON.parse(response.data);
                    this.wishlist = data
                    console.log(this.wishlist);

                })
                .catch(error => {
                    console.error(error)
                })

        },
        async onInit(promise) {
            this.loading = true

            try {
                await promise
            } catch (error) {
                if (error.name === 'NotAllowedError') {
                    this.error = "ERROR: Sie müssen der Kamera eine Zugriffsberechtigung erteilen"
                } else if (error.name === 'NotFoundError') {
                    this.error = "ERROR: Keine Kamera auf diesem Gerät vorhanden"
                } else if (error.name === 'NotSupportedError') {
                    this.error = "ERROR: Sicherer Kontext erforderlich (HTTPS, localhost)"
                } else if (error.name === 'NotReadableError') {
                    this.error = "ERROR: Ist die Kamera bereits in Gebrauch?"
                } else if (error.name === 'OverconstrainedError') {
                    this.error = "ERROR: Installierte Kameras sind nicht geeignet"
                } else if (error.name === 'StreamApiNotSupportedError') {
                    this.error = "ERROR: Stream API wird in diesem Browser nicht unterstützt"
                } else if (error.name === 'InsecureContextError') {
                    this.error = 'ERROR: Der Zugriff auf die Kamera ist nur in einem sicheren Kontext möglich. Verwenden Sie HTTPS oder localhost anstelle von HTTP.';
                } else {
                    this.error = `ERROR: Camera error (${error.name})`;
                }
            } finally {
                this.loading = false
            }
        },

    }

}
</script>

<style scoped>
.loading-indicator {
    font-weight: bold;
    font-size: 2rem;
    text-align: center;
}
</style>