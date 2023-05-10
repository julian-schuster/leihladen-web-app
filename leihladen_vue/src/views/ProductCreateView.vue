<template>
    <div class="container">
        <div class="columns is-centered">
            <div class="column is-half">
                <h2 class="title has-text-centered">Artikel hinzufügen</h2>
                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label class="label" for="id">Inventarnummer</label>
                        <div class="control">
                            <input id="title" v-model="product.id" maxlength="10" class="input" type="text" required>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label" for="title">Name</label>
                        <div class="control">
                            <input id="title" v-model="product.name" maxlength="30" class="input" type="text" required>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label" for="content">Beschreibung</label>
                        <div class="control">
                            <textarea id="content" v-model="product.description" class="textarea input" rows="5"
                                required></textarea>
                        </div>
                    </div>
                    <div class="field has-addons" style="display: flex;">
                        <div class="field" style="margin-right: 10px; width: 150px;">
                            <label class="label" for="categories">Kategorien</label>
                            <div class="select is-multiple">
                                <select multiple v-model="product.categories" required>
                                    <option v-for="category in categories" :key="category.id" :value="category.id">
                                        {{ category.name }}
                                    </option>
                                </select>
                            </div>
                        </div>

                        <div class="field is-flex">
                            <div class="control has-text-centered is-align-items-center is-justify-content-center">
                                <label class="label" for="smallPieces">Kleinteile</label>
                                <input type="checkbox" v-model="product.smallPieces" style="margin-top:14px">
                            </div>
                        </div>

                    </div>
                    <div class="field has-addons" style="display: flex;">
                        <div class="field">
                            <div class="control" style="margin-right: 10px; width: 150px;">
                                <label class="label" for="dimension">Dimension</label>
                                <input class="input" v-model="product.dimension" required>
                            </div>
                        </div>
                        <div class="field">
                            <div class="control" style="width: 150px;">
                                <label class="label" for="weight">Gewicht</label>
                                <input class="input" v-model="product.weight" required>
                            </div>
                        </div>
                    </div>
                    <div class="field has-addons" style="display: flex;">
                        <div class="field">
                            <div class="control" style="margin-right: 10px; width: 150px;">
                                <label class="label" for="deposit">Kaution</label>
                                <input type="number" class="input" v-model="product.deposit" required step="0.01">
                            </div>
                        </div>
                        <div class="field">
                            <div class="control" style="width: 150px;">
                                <label class="label" for="fee">Leihgebühr</label>
                                <input type="number" class="input" v-model="product.fee" required step="0.01">
                            </div>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Bilder</label>
                        <div class="drag-and-drop has-text-centered control highlight" @dragover="handleDragOver"
                            @dragleave="handleDragLeave" @drop="handleDrop">
                            <div class="box">
                                <input id="image" class="file-input" type="file" accept="image/jpeg, image/jpg, image/png"
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
                            Bitte laden Sie Bilddateien (jpg, jpeg, png) hoch.
                        </p>
                    </div>
                    <div class="field">
                        <label class="label" for="quantity">Anzahl</label>
                        <div class="control">
                            <input id="quantity" v-model.number="product.quantity" class="input" type="number" min="1"
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
                id: '',
                name: '',
                description: '',
                image1: null,
                image2: null,
                image3: null,
                image4: null,
                quantity: 1,
                dimension: '',
                weight: '',
                fee: 0,
                deposit: 0,
                smallPieces: false,
                categories: [],
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
        handleDragOver(event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = "copy";
            event.currentTarget.classList.add("dragging-over");
        },
        handleDragLeave(event) {
            event.currentTarget.classList.remove("dragging-over");
        },
        handleDrop(event) {
            event.currentTarget.classList.remove("dragging-over");
        },
        async getCategories() {
            await axios
                .get(`/api/v1/categories`)
                .then((response) => {
                    this.categories = response.data;
                })
                .catch((error) => {
                    console.log(error);
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
            formData.append('id', this.product.id);
            formData.append('name', this.product.name);
            formData.append('description', this.product.description);
            formData.append('categories', this.product.categories);
            formData.append('quantity', this.product.quantity);
            formData.append('weight', this.product.weight);
            formData.append('deposit', this.product.deposit);
            formData.append('fee', this.product.fee);
            formData.append('dimension', this.product.dimension);
            formData.append('smallPieces', this.product.smallPieces);
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

                    this.product.name = '';
                    this.product.description = '';
                    this.product.categories = [];
                    this.product.quantity = 0;
                    this.product.id = '';
                    this.product.smallPieces = false;
                    this.product.dimension = '';
                    this.product.weight = '';
                    this.product.deposit = 0;
                    this.product.fee = 0;
                    this.product.image1 = null;
                    this.product.image2 = null;
                    this.product.image3 = null;
                    this.product.image4 = null;
                    this.file1 = null;
                    this.file2 = null;
                    this.file3 = null;
                    this.file4 = null;
                })
                .catch((error) => {
                    toast({
                        message: "Ein Artikel mit dieser Inventarnummer existiert bereits.",
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

.highlight {
    border: 2px solid transparent;
    transition: border-color 0.3s, transform 0.3s;
}

.highlight:hover {
    border-color: #398378;
    transform: scale(1.05);
    background-color: rgb(245, 245, 245);
}

.drag-and-drop.dragging-over {
    border: 2px solid #398378;
    transform: scale(1.05);
    background-color: rgb(245, 245, 245);

}
</style>