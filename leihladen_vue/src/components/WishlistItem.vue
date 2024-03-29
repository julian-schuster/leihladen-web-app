<template>
    <tr>
        <td>{{ item.product.id }}</td>
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
        // Gibt die Anzahl eines Produkts zurück
        getItemTotal(item) {
            return item.quantity
        },

        // Verringert die Menge eines Artikels in der Wunschliste um 1
        decrementQuanitity(item) {

            if (!this.product) {
                // Fehlermeldung anzeigen, wenn das Produkt nicht verfügbar ist
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
                // Bestätigungsnachricht anzeigen, bevor ein Artikel aus der Wunschliste entfernt wird
                const confirmationMessage = `Möchten Sie den Artikel "${item.product.name}" wirklich von Ihrer Wunschliste entfernen?`;
                if (window.confirm(confirmationMessage)) {
                    this.$emit('removeFromWishlist', item)

                    // Bestätigungsnachricht anzeigen, wenn der Artikel erfolgreich entfernt wurde
                    toast({
                        message: `"${item.product.name}" wurde von Ihrer Wunschliste entfernt`,
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: "bottom-right",
                    });
                } else {
                    item.quantity = 1
                    return
                }
            }
            this.updateWishlist()

            // Bestätigungsnachricht anzeigen, wenn die Menge eines Artikels erfolgreich reduziert wurde
            toast({
                message: `Anzahl von Artikel "${item.product.name}" um 1 verringert.`,
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 4000,
                position: "bottom-right",
            });

        },

        // Erhöht die Menge eines Artikels in der Wunschliste um 1
        incrementQuanitity(item) {

            if (!this.product) {
                // Fehlermeldung anzeigen, wenn das Produkt nicht verfügbar ist
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

                // Bestätigungsnachricht anzeigen, wenn die Menge eines Artikels erfolgreich erhöht wurde
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

        // Aktualisiert die Wunschliste in localStorage
        updateWishlist() {
            localStorage.setItem('wishlist', JSON.stringify(this.$store.state.wishlist))
        },

        // Entfernt einen Artikel aus der Wunschliste
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
        // Produkt von der API holen und es in this.product speichern
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
    },
    computed: {
        // Formatierung für Währungen im deutschen Format
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