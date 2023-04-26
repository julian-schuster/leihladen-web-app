<template>
    <div class="page-wishlist">
        <div class="columns is-multiline is-mobile is-centered">
            <div class="column is-12">
                <h1 class="title">Wunschliste Scannen</h1>
            </div>
            <div class="column is-6 is-centered">
                <div class="box">
                    <p class="error">{{ error }}</p>
                    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
                        <div class="lds-dual-ring"></div>
                    </div>
                    <qrcode-stream :camera="camera" @decode="onDecode" @init="onInit" v-show="show"></qrcode-stream>
                </div>
            </div>
            <table class="table is-fullwidth">
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
                    <tr v-for="item in wishlist.items" v-bind:key="item.product.id">
                        <td>{{ item.product.name }}</td>
                        <td class="has-text-centered">{{ item.quantity }}</td>
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
</template>

<script>
import { QrcodeStream } from 'vue3-qrcode-reader'
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'WishlistScan',
    components: {
        QrcodeStream
    },
    data() {
        return {
            wishlist: {
                items: []
            },
            products: [],
            camera: 'auto',
            error: '',
            show: true
        }
    },
    mounted() {
        document.title = 'Wunschliste Scan | Leihladen'
        this.$store.commit("setIsLoading", true);
        this.getProducts()
    },
    methods: {
        onDecode(decodedString) {
            const client_id = decodedString
            axios.get(`/api/v1/wishlist/${client_id}/`)
                .then(response => {
                    this.wishlist = JSON.parse(response.data.qr_code_text);
                    this.turnCameraOff()
                })
                .catch(error => {
                    console.error(error)
                })
            this.turnCameraOn()
        },
        turnCameraOn() {
            this.camera = 'auto'
        },
        turnCameraOff() {
            this.show = false
            this.camera = 'pause'
        },
        timeout(ms) {
            return new Promise(resolve => {
                window.setTimeout(resolve, ms)
            })
        },
        async onInit(promise) {
            this.$store.commit("setIsLoading", true);
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
            }
            finally {
                if (this.show) {
                    this.$store.commit("setIsLoading", false)
                } else {
                    await this.timeout(1000)
                    this.show = true
                    this.$store.commit("setIsLoading", false)
                }
            }
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
                    console.log(response.data);
                    toast({
                        message: response.data.message,
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: "bottom-right",
                    });

                    this.getProducts()
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
        }
    }

}
</script>

<style scoped></style>