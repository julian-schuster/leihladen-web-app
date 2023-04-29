<template>
    <div class="container mt-6">
        <form @submit.prevent="updateProduct">
            <div class="columns is-multiline">
                <div class="column is-6 is-12-mobile">
                    <figure class="image is-3by2 is-square">
                        <img v-bind:src="product.get_images && product.get_images[0] && product.get_images[0].url"
                            alt="Produktbild">
                    </figure>
                    <div class="columns is-multiline">
                        <div class="column is-6" v-if="product.get_images && product.get_images[1]">
                            <figure class="image is-3by2">
                                <img v-bind:src="product.get_images && product.get_images[1] && product.get_images[1].url"
                                    alt="Produktbild">
                            </figure>
                        </div>
                        <div class="column is-6" v-if="product.get_images && product.get_images[2]">
                            <figure class="image is-3by2">
                                <img v-bind:src="product.get_images && product.get_images[2] && product.get_images[2].url"
                                    alt="Produktbild">
                            </figure>
                        </div>
                    </div>
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
                                <div v-for="(file, index) in [file1, file2, file3]" :key="index"
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
                image1: null,
                image2: null,
                image3: null,
                quantity: 0
            },
            categories: [
                { id: 1, name: "Garten" },
                { id: 2, name: "Brettspiele" },
                { id: 3, name: "Sport" }
            ],
            file1: null,
            file2: null,
            file3: null,
            validImages: true,
            isValidImage1: true,
            isValidImage2: true,
            isValidImage3: true,
            fileName1: null,
            fileName2: null,
            fileName3: null,
            isImageUploaded: false,
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
            if (!this.isImageUploaded) {
                toast({
                    message: "Bitte laden Sie mindestens ein Bild hoch.",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
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
                    duration: 2000,
                    position: "bottom-right",
                });
                return;
            }

            const formData = new FormData();
            formData.append('id', this.product.id);
            formData.append('name', this.product.name);
            formData.append('description', this.product.description);
            formData.append('quantity', this.product.quantity);
            formData.append('available', this.product.available);
            formData.append('image', this.file1);
            if (this.file2) {
                formData.append('image2', this.file2);
            }
            if (this.file3) {
                formData.append('image3', this.file3);
            }

            axios
                .put(`/api/v1/product/`, formData)
                .then((response) => {
                    this.product = response.data

                    toast({
                        message: "Artikel wurde erfolgreich bearbeitet",
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: "bottom-right",
                    });

                    if (this.file1) {
                        this.product.get_images[0].url = URL.createObjectURL(this.file1);
                    }
                    if (this.file2) {
                        this.product.get_images[1].url = URL.createObjectURL(this.file2);
                    } else {
                        this.product.get_images[1] = null
                    }
                    if (this.file3) {
                        this.product.get_images[2].url = URL.createObjectURL(this.file3);
                    } else {
                        this.product.get_images[2] = null
                    }

                    this.file1 = null;
                    this.file2 = null;
                    this.file3 = null;

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
            const files = event.target.files;
            const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

            this.file1 = null;
            this.product.image1 = null;
            this.isValidImage1 = false;
            this.fileName1 = '';
            this.file2 = null;
            this.product.image2 = null;
            this.isValidImage2 = false;
            this.fileName2 = '';
            this.file3 = null;
            this.product.image3 = null;
            this.isValidImage3 = false;
            this.fileName3 = '';

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
                    this.isValidImage1 = true;
                    this.fileName1 = file.name;
                    this.isImageUploaded = true
                } else if (i === 1) {
                    this.file2 = file;
                    this.product.image2 = URL.createObjectURL(file);
                    this.isValidImage2 = true;
                    this.fileName2 = file.name;
                } else if (i === 2) {
                    this.file3 = file;
                    this.product.image3 = URL.createObjectURL(file);
                    this.isValidImage3 = true;
                    this.fileName3 = file.name;
                }
            }
        },
        fileName(index) {
            if (index === 1) {
                return this.file1.name;
            } else if (index === 2) {
                return this.file2.name;
            } else if (index === 3) {
                return this.file3.name;
            }
        }, validateImages() {
            if (this.file1 || this.file2 || this.file3) {
                return true;
            } else {
                return false;
            }
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