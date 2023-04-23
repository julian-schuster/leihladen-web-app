<template>
    <div class="container">
        <div class="columns is-centered">
            <div class="column is-half">
                <h2 class="title has-text-centered">Artikel hinzufügen</h2>
                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label class="label" for="title">Name</label>
                        <div class="control">
                            <input id="title" v-model="product.name" class="input" type="text" required>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label" for="content">Beschreibung</label>
                        <div class="control">
                            <textarea id="content" v-model="product.description" class="textarea" rows="5"
                                required></textarea>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Kategorie</label>
                        <div class="control">
                            <div class="select">
                                <select v-model="product.category">
                                    <option v-for="category in categories" :key="category.id" :value="category.id">{{
                                        category.name }}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label" for="image">Bild</label>
                        <div class="file has-name is-fullwidth">
                            <label class="file-label">
                                <input id="image" class="file-input" type="file" accept="image/jpeg, image/jpg, image/png"
                                    @change="handleFileUpload" required>
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
                        <p class="help is-danger" v-if="file && !isValidImage">Bitte laden Sie eine Bilddatei (jpg, jpeg,
                            png) hoch.</p>
                        <div v-if="product.image">
                            <img :src="product.image" alt="Hochgeladenes Bild" class="image is-128x128">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label" for="quantity">Anzahl</label>
                        <div class="control">
                            <input id="quantity" v-model.number="product.quantity" class="input" type="number" min="0"
                                required>
                        </div>
                    </div>
                    <div class="field">
                        <div class="control">
                            <button class="button is-primary" type="submit">Bestätigen</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>

import axios from "axios";
import { toast } from "bulma-toast";

export default {
    name: 'ProductCreate',
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

            file: null,
            isValidImage: true
        };
    },
    mounted() {
        document.title = "Artikel hinzufügen | Leihladen";
    },
    methods: {
        submitForm() {
            if (this.product.quantity <= 0) {
                toast({
                    message: "Bitte geben Sie eine Anzahl größer als 0 ein.",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right",
                });
                return;
            }

            const formData = new FormData();
            formData.append('name', this.product.name);
            formData.append('description', this.product.description);
            formData.append('category', this.product.category);
            formData.append('quantity', this.product.quantity);
            formData.append('image', this.file);

            axios
                .post(`/api/v1/product/`, formData)
                .then((response) => {
                    console.log(response.data);

                    toast({
                        message: "Artikel erfolgreich erstellt",
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: "bottom-right",
                    });

                    this.product.name = ''
                    this.product.description = ''
                    this.product.category = ''
                    this.product.quantity = 0
                    this.product.image = null
                    this.file = null
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