<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-6 is-12-mobile">
        <figure class="image is-3by2 is-square ">
          <a @click="showModal = true">
            <img v-bind:src="product.get_images && product.get_images[0] && product.get_images[0].url" alt="Produktbild"
              @click="zoomImage(0)">
          </a>
        </figure>
        <div class="columns is-multiline">
          <div class="column is-6" v-if="product.get_images && product.get_images[1]">
            <figure class="image is-3by2">
              <a @click="showModal = true">
                <img v-bind:src="product.get_images && product.get_images[1] && product.get_images[1].url"
                  alt="Produktbild" @click="zoomImage(1)">
              </a>
            </figure>
          </div>
          <div class="column is-6">
            <figure class="image is-3by2" v-if="product.get_images && product.get_images[2]">
              <a @click="showModal = true">
                <img v-bind:src="product.get_images && product.get_images[2] && product.get_images[2].url"
                  alt="Produktbild" @click="zoomImage(2)">
              </a>
            </figure>
          </div>
        </div>
      </div>
      <div class="column is-6 is-12-mobile">
        <div class="content">
          <h1 class="title is-3">{{ product.name }}</h1>
          <p class="subtitle is-5">{{ product.description }}</p>
          <hr>
          <div class="field has-addons">
            <div class="control">
              <input type="number" class="input is-rounded" min="1" v-model="quantity">
            </div>
            <div class="control">
              <a class="button is-dark" @click="addToWishlist">
                Zur Wunschliste hinzufügen
              </a>
            </div>
          </div>
        </div>
        <div class="column is-12 is-12-mobile">
          <table class="table">
            <thead>
              <th>Bestand</th>
              <th>Verfügbar</th>
            </thead>
            <tbody>
              <tr>
                <td>{{ product.quantity }}</td>
                <td>{{ product.available }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <div class="modal" :class="{ 'is-active': showModal }">
    <div class="modal-background"></div>
    <div class="modal-content">
      <p class="image">
        <img :src="images[currentIndex]" alt="Produktbild">
      </p>
    </div>
    <button class="modal-close is-large" aria-label="close" @click="showModal = false"></button>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

export default {
  name: "Product",
  data() {
    return {
      product: {},
      quantity: 1,
      showModal: false,
      images: [],
      currentIndex: 0,
    };
  },
  mounted() {
    this.getProduct();

  },
  methods: {
    getProduct() {
      this.$store.commit("setIsLoading", true);

      const category_slug = this.$route.params.category_slug;
      const product_slug = this.$route.params.product_slug;

      axios
        .get(`/api/v1/products/${category_slug}/${product_slug}`)
        .then((response) => {
          this.product = response.data;
          document.title = this.product.name + " | Leihladen";
          this.images = this.product.get_images.map((image) => image.url);
        })
        .catch((error) => {
          console.log(error);
          //Wenn Fehler auftritt zurück auf Startseite leiten
          this.$router.push("/")
        });

      this.$store.commit("setIsLoading", false);
    },
    addToWishlist() {
      if (isNaN(this.quantity) || this.quantity < 1) {
        this.quantity = 1;
      }

      const item = {
        product: this.product,
        quantity: this.quantity,
      };

      this.$store.commit("addToWishlist", item);

      toast({
        message: "Der Artikel wurde zur Wunschliste hinzugefügt",
        type: "is-success",
        dismissible: true,
        pauseOnHover: true,
        duration: 2000,
        position: "bottom-right",
      });
    },
    zoomImage(index) {
      this.showModal = true;
      this.currentIndex = index;
    },
  },
};
</script>

<style scoped>
.image {
  transition: transform 0.5s;
  transform-origin: center;
}

.image.zoomed {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(2);
  z-index: 9999;
}

.image:hover {
  border: 1px solid #ccc;
  box-shadow: 0 0 5px #ccc;
}
</style>