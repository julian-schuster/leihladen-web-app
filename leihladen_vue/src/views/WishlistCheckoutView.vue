<template>
    <div class="container page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title has-text-centered">Übersicht und QR-Code der Wunschliste</h1>
            </div>
            <div class="column is-12 box">
                <div class="table-container">
                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>Artikel</th>
                                <th class="has-text-centered">Kaution</th>
                                <th class="has-text-centered">Leihgebühr</th>
                                <th class="has-text-centered">Anzahl</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in wishlist.items" v-bind:key="item.product.id">

                                <td><router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link>
                                </td>
                                <td class="has-text-centered">{{ currencyFormatter.format(item.product.deposit) }}</td>
                                <td class="has-text-centered">{{ currencyFormatter.format(item.product.fee) }}</td>
                                <td class="has-text-centered">{{ item.quantity }}</td>
                            </tr>
                        </tbody>
                        <tfoot>
                            <tr>
                                <td></td>
                                <td class="has-text-centered">
                                    {{ currencyFormatter.format(totalDeposit) }}
                                </td>
                                <td class="has-text-centered">
                                    {{ currencyFormatter.format(totalFee) }}
                                </td>
                                <td class="has-text-centered">{{ wishlistTotalLength }}</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
            <div class="column is-12 box center-box">
                <h2 class="subtitle">QR-Code</h2>
                <canvas ref="qrcode"></canvas>
                <p class="has-text-grey mb-4">Bitte zeigen Sie diesen QR-Code entweder ausgedruckt oder auf Ihrem Smartphone
                    im Leihladen vor.</p>
                <div>
                    <button class="button" @click="generatePDF">
                        <span class="icon"><i class="far fa-file-pdf" style="color:blue"></i></span>
                        <span>PDF generieren</span>
                    </button>
                </div>
                <br>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import QRCode from 'qrcode'
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import { toast } from "bulma-toast";



export default {
    name: 'WishlistCheckout',
    components: {
        QRCode
    },
    data() {

        return {
            wishlist: {
                items: []
            },
            clientId: '',
        }
    },
    mounted() {
        document.title = 'Wunschliste Abschluss | Leihladen'

        this.wishlist = this.$store.state.wishlist
        this.clientId = this.$store.state.clientId

        const qrCodeText = JSON.stringify(this.wishlist)

        this.createQRCode(this.clientId)
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

                    toast({
                        message: response.data.status,
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: "bottom-right",
                    });

                })
                .catch(error => {
                    console.error(error)

                    toast({
                        message: "Etwas ist schiefgelaufen. Bitte nochmal versuchen.",
                        type: "is-danger",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: "bottom-right",
                    });
                })
        },
        generatePDF() {
            // Erstelle ein neues jsPDF-Objekt
            const doc = new jsPDF();

            // Füge den Titel "Wunschliste" hinzu
            doc.setFontSize(18);
            doc.text('Wunschliste | Leihladen', doc.internal.pageSize.getWidth() / 2, 15, { align: 'center' });

            // Füge die Client ID hinzu
            doc.setFontSize(12);
            doc.text(`Client ID: ${this.clientId}`, 10, 30);

            // Füge das Datum hinzu
            const now = new Date();
            const date = now.toLocaleDateString();
            doc.text(`Erstellt am: ${date}`, doc.internal.pageSize.getWidth() - 60, 30);

            // Füge eine Tabelle hinzu
            const headers = [['Artikel', 'Kaution', 'Gebühr', 'Anzahl']];
            let totalDeposit = 0;
            let totalFee = 0;
            const data = this.wishlist.items.map(item => {
                totalDeposit += item.product.deposit * item.quantity;
                totalFee += item.product.fee * item.quantity;
                return [item.product.name, item.product.deposit + ' €', item.product.fee + ' €', item.quantity];
            });
            doc.autoTable({
                head: headers,
                body: data,
                startY: 40,
                margin: { top: 40 },
            });

            // Füge die Gesamtkaution hinzu
            doc.setFontSize(12);
            doc.text(`Gesamtkaution: ${totalDeposit.toFixed(2)} €`, 10, doc.autoTable.previous.finalY + 10);

            // Füge die Gesamtleihgebühr hinzu
            doc.setFontSize(12);
            doc.text(`Gesamtleihgebühr: ${totalFee.toFixed(2)} €`, 10, doc.autoTable.previous.finalY + 20);

            // Füge den QR-Code hinzu
            QRCode.toDataURL(this.clientId, { errorCorrectionLevel: 'L' }, function (err, url) {
                if (err) console.error(err);
                doc.addImage(url, 'PNG', 20, doc.autoTable.previous.finalY + 40, 30, 30);
                doc.text('Bitte zeigen Sie den QR-Code im Leihladen vor.', 60, doc.autoTable.previous.finalY + 60);

                // Füge den Footer hinzu
                const contactInfo = 'Kontakt:\nMusterstraße 123, 12345 Musterstadt\ninfo@leihladen.de\n0123 / 456 789';
                const openingHours = 'Öffnungszeiten:\nFr: 16:00-17:30 Uhr';
                const footerX = doc.internal.pageSize.getWidth() / 2;
                const footerY = doc.internal.pageSize.getHeight() - 20;
                doc.setFontSize(10);
                doc.text(contactInfo, footerX - 50, footerY, { align: 'left' });
                doc.text(openingHours, footerX + 50, footerY, { align: 'right' });

                doc.save('Wunschliste.pdf');
            });
        }

    },
    computed: {
        wishlistTotalLength() {
            return this.wishlist.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
        totalDeposit() {
            return this.wishlist.items.reduce((acc, curVal) => {
                return acc += curVal.product.deposit * curVal.quantity
            }, 0)
        },
        totalFee() {
            return this.wishlist.items.reduce((acc, curVal) => {
                return acc += curVal.product.fee * curVal.quantity
            }, 0)
        },
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

<style scoped>
.table-container {
    max-width: 100%;
    overflow-x: auto;
    padding: 0 10px;
}

@media (min-width: 769px) {
    .table-container {
        padding: 0 20px;
    }
}

@media (max-width: 768px) {
    .column {
        padding: 0;
    }

    .center-box {
        text-align: center;
    }
}
</style>