<template>
    <div class="container">
        <div class="columns is-centered">
            <div class="column is-half">
                <h2 class="title has-text-centered">Artikel hinzufügen</h2>
                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label class="label" for="title">Name</label>
                        <div class="control">
                            <input id="title" v-model="product.name" maxlength="30" class="input" type="text" required>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label" for="content">Beschreibung</label>
                        <div class="control">
                            <textarea id="content" v-model="product.description" maxlength="255" class="textarea" rows="5"
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
                        <label class="label">Bilder</label>
                        <div class="drag-and-drop has-text-centered control">
                            <div class="box">
                                <input id="image" class="file-input" type="file" accept="image/jpeg, image/jpg"
                                    @change="handleFileUpload" multiple />
                                <div class="drag-text">
                                    <i class="fas fa-cloud-upload-alt fa-2x"></i>
                                    <h3 class="title is-4">Bilder hierher ziehen oder klicken</h3>
                                </div>
                            </div>
                        </div>
                        <div class="images-container columns is-multiline is-mobile is-centered">
                            <div v-for="(file, index) in [file1, file2, file3, file4]" :key="index"
                                class="column is-narrow mb-4">
                                <div v-if="file">
                                    <div class="file-name" style="width: 150px">{{ file.name }}</div>
                                    <div v-if="product['image' + (index + 1)]">
                                        <img :src="product['image' + (index + 1)]" alt="Hochgeladenes Bild"
                                            class="image is-128x128" />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <p class="help is-danger" v-if="!validImages">
                            Bitte laden Sie Bilddateien (jpg, jpeg) hoch.
                        </p>
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
                            <button class="button is-success" type="submit"> <span class="icon">
                                    <i class="fas fa-check-circle"></i></span> <span> Bestätigen</span></button>
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
                image1: null,
                image2: null,
                image3: null,
                image4: null,
                quantity: 0
            },
            categories: [],
            file1: null,
            file2: null,
            file3: null,
            file4: null,
            validImages: true,
            isImageUploaded: false,
        };
    },
    mounted() {
        document.title = "Artikel hinzufügen | Leihladen";
        this.getCategories()
    },
    methods: {
        async getCategories() {
            await axios
                .get(`/api/v1/categories`)
                .then((response) => {
                    this.categories = response.data;
                })
                .catch((error) => {
                    console.log(error);
                    //Wenn Fehler auftritt zurück auf Startseite leiten
                    this.$router.push("/")
                });
        },
        submitForm() {
            if (!this.isImageUploaded) {
                toast({
                    message: "Bitte laden Sie mindestens ein Bild hoch.",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 4000,
                    position: "bottom-right",
                });
                return;
            }

            if (this.product.quantity <= 0) {
                toast({
                    message: "Bitte geben Sie eine Anzahl größer als 0 ein.",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 4000,
                    position: "bottom-right",
                });
                return;
            }

            const formData = new FormData();
            formData.append('name', this.product.name);
            formData.append('description', this.product.description);
            formData.append('category', this.product.category);
            formData.append('quantity', this.product.quantity);
            formData.append('image', this.file1);
            if (this.file2) {
                formData.append('image2', this.file2);
            }
            if (this.file3) {
                formData.append('image3', this.file3);
            }
            if (this.file4) {
                formData.append('image4', this.file4);
            }
            axios
                .post(`/api/v1/product/`, formData)
                .then((response) => {
                    console.log(response.data);

                    toast({
                        message: `Artikel "${this.product.name}" wurde ${this.product.quantity}x hinzugefügt`,
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: "bottom-right",
                    });

                    this.product.name = ''
                    this.product.description = ''
                    this.product.category = ''
                    this.product.quantity = 0
                    this.product.image1 = null
                    this.product.image2 = null
                    this.product.image3 = null
                    this.product.image4 = null
                    this.file1 = null;
                    this.file2 = null;
                    this.file3 = null;
                    this.file4 = null
                })
                .catch((error) => {
                    console.log(error);
                    toast({
                        message: "Etwas ist schiefgelaufen. Bitte nochmal versuchen.",
                        type: "is-danger",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: "bottom-right",
                    });
                });
        },
        handleFileUpload(event) {
            const files = event.target.files;
            const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

            this.file1 = null;
            this.product.image1 = null;
            this.file2 = null;
            this.product.image2 = null;
            this.file3 = null;
            this.product.image3 = null;
            this.file4 = null;
            this.product.image4 = null;


            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                if (!allowedExtensions.exec(file.name)) {
                    this.validImages = false;
                    return;
                } else {
                    this.validImages = true;
                }
                if (i === 0) {
                    this.file1 = file;
                    this.product.image1 = URL.createObjectURL(file);
                    this.isImageUploaded = true
                } else if (i === 1) {
                    this.file2 = file;
                    this.product.image2 = URL.createObjectURL(file);
                } else if (i === 2) {
                    this.file3 = file;
                    this.product.image3 = URL.createObjectURL(file);
                } else if (i === 3) {
                    this.file4 = file;
                    this.product.image4 = URL.createObjectURL(file);
                }
            }
        },
        validateImages() {
            if (this.file1 || this.file2 || this.file3 || this.file4) {
                return true;
            } else {
                return false;
            }
        },
    },
    computed: {
        isValidImages() {
            return this.validateImages();
        },
    },
};
</script>

<style scoped>
.file-name {
    display: inline-block;
    width: 30%;
    border-style: none;
    margin-left: -15px
}

.images-container {
    display: flex;
    justify-content: space-between;
}
</style>