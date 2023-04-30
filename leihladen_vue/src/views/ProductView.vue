<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-6 is-12-mobile">
        <figure class="image is-3by2 is-square highlight">
          <a @click="showModal = true">
            <img v-bind:src="product.get_images && product.get_images[0] && product.get_images[0].url" alt="Produktbild"
              @click="zoomImage(0)" style="object-fit: cover; width: 100%; height: 100%;">
          </a>
        </figure>
        <div class="columns is-multiline">
          <div class="column is-6" v-if="product.get_images && product.get_images[1]">
            <figure class="image is-3by2 highlight">
              <a @click="showModal = true">
                <img v-bind:src="product.get_images && product.get_images[1] && product.get_images[1].url"
                  alt="Produktbild" @click="zoomImage(1)" style="object-fit: cover; width: 100%; height: 100%;">
              </a>
            </figure>
          </div>
          <div class="column is-6">
            <figure class="image is-3by2 highlight" v-if="product.get_images && product.get_images[2]">
              <a @click="showModal = true">
                <img v-bind:src="product.get_images && product.get_images[2] && product.get_images[2].url"
                  alt="Produktbild" @click="zoomImage(2)" style="object-fit: cover; width: 100%; height: 100%;">
              </a>
            </figure>
          </div>
        </div>
      </div>
      <div class="column is-6 is-12-mobile">
        <div class="content">
          <label class="label" for="name">Name</label>
          <p class="subtitle is-5">{{ product.name }}</p>
          <hr>
          <label class="label" for="description">Beschreibung</label>
          <p class="subtitle is-5">{{ product.description }}</p>
          <hr>
          <label class="label" for="date_added">Hinzugefügt am</label>
          <p class="subtitle is-5">{{ product.date_added }}</p>
          <hr>
          <label class="label" for="wishlist_add">Aktuell verfügbar</label>
          <p class="subtitle is-5" v-if="product.available == 0" style="color:red"> {{ product.available }}</p>
          <p class="subtitle is-5" v-else style="color:green"> {{ product.available }}</p>
          <hr>
          <label class="label" for="wishlist_add">Zur Wunschliste hinzufügen </label>
          <div class="field has-addons">
            <div class="control">
              <input type="number" class="input is-rounded" min="1" v-model="quantity" placeholder="Menge">
            </div>
            <div class="control">
              <a class="button is-success" @click="addToWishlist">
                <span class="icon"><i class="fas fa-plus"></i></span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal" :class="{ 'is-active': showModal }">
    <div class="modal-background"></div>
    <div class="modal-content">
      <button class="modal-close is-large" aria-label="close" @click="showModal = false"></button>
      <img :src="images[currentIndex]" alt="Produktbild" class="modal-image">
    </div>
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
          this.product.date_added = new Date(this.product.date_added).toLocaleDateString();
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
        message: `Der Artikel "${this.product.name}" wurde zur Wunschliste hinzugefügt`,
        type: "is-success",
        dismissible: true,
        pauseOnHover: true,
        duration: 4000,
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

.highlight {
  border: 2px solid transparent;
  transition: border-color 0.3s, transform 0.3s;
}

.highlight:hover {
  border-color: #ddd;
  transform: scale(1.1);
}

.modal-content {
  position: relative;
  height: 100%;
}

.modal-image {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>