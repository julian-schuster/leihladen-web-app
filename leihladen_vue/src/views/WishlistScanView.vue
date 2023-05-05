<template>
    <div class="container page-wishlist">
        <div class="columns is-multiline is-mobile is-centered">
            <div class="column is-12">
                <h1 class="title has-text-centered">Wunschliste Scannen</h1>
            </div>
            <div class="column is-6-desktop is-12-mobile is-centered">
                <div class="box">
                    <p class="error">{{ error }}</p>
                    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
                        <div class="lds-dual-ring"></div>
                    </div>
                    <p class="error" v-if="noFrontCamera">
                        Sie scheinen keine Frontkamera an Ihrem Gerät zu haben.
                    </p>
                    <p class="error" v-if="noRearCamera">
                        Sie scheinen keine Rückkamera an Ihrem Gerät zu haben.
                    </p>
                    <qrcode-stream :camera="camera" @decode="onDecode" @init="onInit" v-show="show"></qrcode-stream>
                </div>
                <div class="has-text-centered">
                    <button class="button is-info" @click="switchCamera"
                        v-if="isMobile() === 'rear' || isMobile() === 'front'">Kamera
                        wechseln</button>
                </div>
            </div>
            <div class="column is-12" v-if="wishlist.items.length > 0">
                <h3 class="has-text-centered">Wunschliste: {{ wishlist.client_id }}</h3>
                <div class="table-container box">
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
                                <td>
                                    <router-link :to="item.product.get_absolute_url">{{ item.product.name
                                    }}</router-link>
                                </td>
                                <td class="has-text-centered">{{ item.quantity }}</td>
                                <td class="has-text-centered">{{ getProductCount(item.product.id) }}</td>
                                <td class="has-text-centered" v-if="getProductAvailable(item.product.id) == 0"
                                    style="color:red">{{ getProductAvailable(item.product.id) }}</td>
                                <td class="has-text-centered" v-else style="color:green">{{
                                    getProductAvailable(item.product.id) }}</td>
                                <td class="has-text-right">
                                    <a class="button is-success is-light is-small"
                                        @click="updateProductAvailability(item.product.id, 1)">
                                        <span class="icon">
                                            <i class="fas fa-plus"></i>
                                        </span>
                                    </a>
                                </td>
                                <td class="has-text-right">
                                    <a class="button is-danger is-light is-small"
                                        @click="updateProductAvailability(item.product.id, -1)">
                                        <span class="icon">
                                            <i class="fas fa-minus"></i>
                                        </span>
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <hr>
                <div class="box">
                    <h4>Verlauf</h4>
                    <div v-for="entry in log" :key="entry.product.id" class="log-entry">
                        <span class="time">{{ entry.time }}</span>: {{ entry.message }}
                    </div>
                </div>
            </div>
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
                items: [],
                client_id: '',
            },
            products: [],
            camera: this.isMobile(),
            noRearCamera: false,
            noFrontCamera: false,
            error: '',
            show: true,
            log: []
        }
    },
    mounted() {
        document.title = 'Wunschliste Scan | Leihladen'
        this.$store.commit("setIsLoading", true);
        this.getProducts()
    },
    methods: {
        isMobile() {
            if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return 'rear'
            } else {
                return 'auto'
            }
        },
        checkIsMobile() {
            if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return 'true'
            } else {
                return 'false'
            }
        },
        switchCamera() {
            switch (this.camera) {
                case 'front':
                    this.camera = 'rear'
                    break
                case 'rear':
                    this.camera = 'front'
                    break
                case 'pause':
                    this.camera = this.isMobile()
                    break
            }
        },
        onDecode(decodedString) {
            const client_id = decodedString
            axios.get(`/api/v1/wishlist/${client_id}/`)
                .then(response => {
                    this.wishlist = JSON.parse(response.data.qr_code_text);
                    this.wishlist.client_id = client_id
                    this.turnCameraOff()
                })
                .catch(error => {
                    console.error(error)
                })

            this.turnCameraOn();

        },
        turnCameraOn() {
            this.camera = this.isMobile()
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
                const triedFrontCamera = this.camera === 'front'
                const triedRearCamera = this.camera === 'rear'
                const cameraMissingError = error.name === 'OverconstrainedError'

                if (triedRearCamera && cameraMissingError) {
                    this.noRearCamera = true
                }

                if (triedFrontCamera && cameraMissingError) {
                    this.noFrontCamera = true
                }
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
            const product = this.products.find(p => p.id === id);

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

            const confirmationMessage = `Möchten Sie die Verfügbarkeit von "${product.name}" ${value > 0 ? 'erhöhen' : 'verringern'}?`;
            if (window.confirm(confirmationMessage)) {

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

                        const logEntry = {
                            product: updatedProduct,
                            message: `Verfügbarkeit für Artikel "${updatedProduct.name}" um ${Math.abs(value)} ${value > 0 ? 'erhöht' : 'verringert'}.`,
                            time: new Date().toLocaleTimeString()
                        };
                        this.log.push(logEntry);

                        toast({
                            message: `Verfügbarkeit für Artikel "${updatedProduct.name}" um ${Math.abs(value)} ${value > 0 ? 'erhöht' : 'verringert'}.`,
                            type: "is-success",
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
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
                            duration: 4000,
                            position: "bottom-right",
                        });

                    });
            }
        },
    }

}
</script>

<style scoped></style>