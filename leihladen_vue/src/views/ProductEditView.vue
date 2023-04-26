<template>
    <div class="container mt-6">
        <form @submit.prevent="updateProduct">
            <div class="columns is-multiline">
                <div class="column is-5 is-12-mobile">
                    <figure class="image is-5by4">
                        <img v-bind:src="product.get_image" alt="Produktbild">
                    </figure>
                </div>
                <div class="column is-6 is-12-mobile">
                    <div class="content">
                        <h1 class="title is-3">
                            <label class="label" for="name">Name</label>
                            <input class="input" v-model="product.name" required>
                        </h1>
                        <p class="subtitle is-5">
                            <label class="label" for="description">Beschreibung</label>
                            <textarea class="textarea" v-model="product.description" required></textarea>
                        </p>
                        <div class="field has-addons" style="display: flex;">
                            <div class="control" style="margin-right: 10px; width: 150px;">
                                <label class="label" for="quantity">Bestand</label>
                                <input type="number" class="input" min="1" v-model="product.quantity" required>
                            </div>
                            <div class="control" style="width: 150px;">
                                <label class="label" for="quantity">Verfügbar</label>
                                <input type="number" class="input" min="1" :max="product.quantity"
                                    v-model="product.available" required>
                            </div>
                        </div>
                        <div class="field">
                            <label class="label" for="image">Bild</label>
                            <div class="file has-name is-fullwidth">
                                <label class="file-label">
                                    <input id="image" class="file-input" type="file"
                                        accept="image/jpeg, image/jpg, image/png" @change="handleFileUpload">
                                    <span class="file-cta">
                                        <span class="file-icon">
                                            <i class="fas fa-upload"></i>
                                        </span>
                                        <span class="file-label">
                                            Bild auswählen...
                                        </span>
                                    </span>
                                    <span class="file-name" v-if="file">{{ file.name }}</span>
                                </label>
                            </div>
                            <p class="help is-danger" v-if="file && !isValidImage">Bitte laden Sie eine Bilddatei (jpg,
                                jpeg,
                                png) hoch.</p>
                            <div v-if="product.image">
                                <img :src="product.image" alt="Hochgeladenes Bild" class="image is-128x128">
                            </div>
                        </div>
                        <div class="control">
                            <button class="button is-dark" type="submit">
                                Speichern
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

export default {
    name: "ProductEdit",
    data() {
        return {
            product: {
                name: '',
                description: '',
                image: null,
                quantity: 0
            },
            categories: [
                { id: 1, name: "Garten" },
                { id: 2, name: "Brettspiele" },
                { id: 3, name: "Sport" }
            ],
            isValidImage: true,
            file: null
        };
    },
    mounted() {
        this.getProduct();
    },
    methods: {
        async getProduct() {
            const category_slug = this.$route.params.category_slug;
            const product_slug = this.$route.params.product_slug;

            await axios
                .get(`/api/v1/products/${category_slug}/${product_slug}`)
                .then((response) => {
                    this.product = response.data;
                    document.title = this.product.name + " | Leihladen";
                })
                .catch((error) => {
                    console.log(error);
                    //Wenn Fehler auftritt zurück auf Startseite leiten
                    this.$router.push("/")
                });
        },
        updateProduct() {
            const formData = new FormData();
            formData.append('id', this.product.id);
            formData.append('name', this.product.name);
            formData.append('description', this.product.description);
            formData.append('quantity', this.product.quantity);
            formData.append('available', this.product.available);

            if (this.file) {
                formData.append('image', this.file);
            }

            axios
                .put(`/api/v1/product/`, formData)
                .then((response) => {
                    console.log(response.data);

                    toast({
                        message: "Artikel wurde erfolgreich bearbeitet",
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: "bottom-right",
                    });

                    if (this.file) {
                        this.product.get_image = URL.createObjectURL(this.file);
                    }

                })
                .catch((error) => {
                    console.log(error);
                    toast({
                        message: "Etwas ist schiefgelaufen. Bitte nochmal versuchen.",
                        type: "is-danger",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: "bottom-right",
                    });
                });
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
                if (!allowedExtensions.exec(file.name)) {
                    this.isValidImage = false;
                    return;
                }
                this.file = file;
                this.product.image = URL.createObjectURL(file);
                this.isValidImage = true;
            }
        }
    },
};
</script>

<style scoped></style>