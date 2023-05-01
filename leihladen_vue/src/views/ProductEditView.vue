<template>
    <div class="container">
        <form @submit.prevent="updateProduct">
            <div class="columns">
                <div class="column is-half">
                    <div class="columns is-multiline">
                        <div class="column is-12" v-if="product.get_images && product.get_images.length == 1">
                            <figure class="image is-square highlight">
                                <img v-bind:src="product.get_images && product.get_images[0] && product.get_images[0].url"
                                    alt="Produktbild">
                            </figure>
                        </div>
                        <div class="column is-6" v-else>
                            <figure class="image is-3by2 highlight">
                                <img v-bind:src="product.get_images && product.get_images[0] && product.get_images[0].url"
                                    alt="Produktbild">
                            </figure>
                        </div>
                        <div class="column is-6">
                            <figure class="image is-3by2 highlight" v-if="product.get_images && product.get_images[1]">
                                <img v-bind:src="product.get_images && product.get_images[1] && product.get_images[1].url"
                                    alt="Produktbild">
                            </figure>
                        </div>
                        <div class="column is-6">
                            <figure class="image is-3by2 highlight" v-if="product.get_images && product.get_images[2]">
                                <img v-bind:src="product.get_images && product.get_images[2] && product.get_images[2].url"
                                    alt="Produktbild">
                            </figure>
                        </div>
                        <div class="column is-6">
                            <figure class="image is-3by2 highlight" v-if="product.get_images && product.get_images[3]">
                                <img v-bind:src="product.get_images && product.get_images[3] && product.get_images[3].url"
                                    alt="Produktbild">
                            </figure>
                        </div>
                    </div>
                </div>
                <div class="column is-half">
                    <div class="content">
                        <h1 class="title is-3">
                            <label class="label" for="name">Name</label>
                            <input class="input" v-model="product.name" maxlength="30" required>
                        </h1>
                        <p class="subtitle is-5">
                            <label class="label" for="description">Beschreibung</label>
                            <textarea class="textarea" v-model="product.description" maxlength="255" required></textarea>
                        </p>
                        <div class="field">
                            <label class="label" for="category">Kategorie</label>
                            <div class="select">
                                <select v-model="product.category" required>
                                    <option value="">Bitte wählen</option>
                                    <option v-for="category in categories" :key="category.id" :value="category.id">
                                        {{ category.name }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="field has-addons" style="display: flex;">
                            <div class="control" style="margin-right: 10px; width: 150px;">
                                <label class="label" for="quantity">Bestand</label>
                                <input type="number" class="input" min="1" v-model="product.quantity" required>
                            </div>
                            <div class="control" style="width: 150px;">
                                <label class="label" for="quantity">Verfügbar</label>
                                <input type="number" class="input" min="0" :max="product.quantity"
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
                        <div class="control">
                            <button class="button" type="submit"> <span class="icon"><i class="fas fa-save"
                                        style="color:green"></i></span>
                                <span>Speichern</span>
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
                image4: null,
                quantity: 0,
                category: '',
            },
            categories: [],
            file1: null,
            file2: null,
            file3: null,
            file4: null,
            validImages: true,
        };
    },
    mounted() {
        this.getProduct();
        this.getCategories();
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
            formData.append('id', this.product.id);
            formData.append('name', this.product.name);
            formData.append('description', this.product.description);
            formData.append('quantity', this.product.quantity);
            formData.append('available', this.product.available);
            formData.append('category', this.product.category);

            let categoryId = this.product.category;
            let categoryName = "";
            for (let i = 0; i < this.categories.length; i++) {
                if (this.categories[i].id == categoryId) {
                    categoryName = this.categories[i].name;
                    break;
                }
            }

            if (this.file1) {
                formData.append('image', this.file1);
            }
            if (this.file2) {
                formData.append('image2', this.file2);
            }
            if (this.file3) {
                formData.append('image3', this.file3);
            }
            if (this.file4) {
                formData.append('image4', this.file4);
            }

            if (!this.file1 && !this.file2 && !this.file3 && !this.file4) {
                formData.append('noImageChange', true)
            }

            axios
                .put(`/api/v1/product/`, formData)
                .then((response) => {
                    this.product = response.data

                    toast({
                        message: `Artikel "${this.product.name}" wurde bearbeitet`,
                        type: "is-success",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: "bottom-right",
                    });

                    if (this.file1) {
                        this.product.get_images[0].url = URL.createObjectURL(this.file1);
                    }

                    if (this.file2) {
                        this.product.get_images[1].url = URL.createObjectURL(this.file2);
                    } else if (!this.file1 && !this.file2 && !this.file3 && !this.file4) {

                    } else {
                        this.product.get_images[1] = null;
                    }

                    if (this.file3) {
                        this.product.get_images[2].url = URL.createObjectURL(this.file3);
                    } else if (!this.file1 && !this.file2 && !this.file3 && !this.file4) {

                    } else {
                        this.product.get_images[2] = null;
                    }

                    if (this.file4) {
                        this.product.get_images[3].url = URL.createObjectURL(this.file4);
                    } else if (!this.file1 && !this.file2 && !this.file3 && !this.file4) {

                    } else {
                        this.product.get_images[3] = null;
                    }


                    this.file1 = null;
                    this.file2 = null;
                    this.file3 = null;
                    this.file4 = null;

                    this.$router.push(`${this.product.get_absolute_url}edit`);
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