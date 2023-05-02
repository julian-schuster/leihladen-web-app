<template>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumbs">
      <ul>
        <li><a href="/"><span class="icon"><i class="fas fa-home"></i></span></a></li>
        <li v-for="(section, index) in sections" :key="index" :class="{ 'is-active': index === sections.length }">
          <span>
            <a :href="getUrl(index)" style="text-transform: capitalize;">{{
              decodeURIComponent(section)
            }}</a>
          </span>

        </li>
      </ul>
    </nav>
    <div class="columns">
      <div class="column is-7">
        <div class="preview">
          <figure class="image is-4by3 highlight thumbnail is-hidden-mobile">
            <a>
              <img v-bind:src="currentPreview" alt="Produktbild">
            </a>
          </figure>
        </div>
        <div class="thumbnails thumbnail" v-if="images.length > 1">
          <div class="columns is-multiline is-centered">
            <div class="column is-3" v-for="(image, index) in  product.get_images ">
              <figure class="image is-3by2 highlight">
                <a @click="currentIndex = index; updatePreview()">
                  <img v-bind:src=" image.url " alt="Produktbild">
                </a>
              </figure>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-5">
        <div class="content">
          <label class="label" for="name">Name</label>
          <p class="subtitle is-5">{{ product.name }}</p>
          <hr>
          <label class="label" for="category">Kategorie</label>
          <p class="subtitle is-5" v-if=" product.get_category_name "><a
              :href=" `/${product.get_category_name.toLowerCase()}` "
              style="  text-decoration: none; color: hsl(0, 0%, 29%);">{{
              product.get_category_name }}</a></p>
          <hr>
          <label class="label" for="description">Beschreibung</label>
          <p class="subtitle is-5">{{ product.description }}</p>
          <hr>
          <label class="label" for="date_added">Hinzugefügt am</label>
          <p class="subtitle is-5">{{ product.date_added }}</p>
          <hr>
          <label class="label" for="wishlist_add">Verfügbarkeit</label>
          <p class="subtitle is-5" v-if=" product.available == 0 " style="color:red"><i class="fas fa-times-circle"></i>
            Vorübergehend nicht verfügbar</p>
          <p class="subtitle is-5" v-else style="color:green"><i class="fas fa-check-circle"></i>
            {{ product.available }} Verfügbar
          </p>
          <hr>
          <label class="label" for="wishlist_add">Zur Wunschliste hinzufügen </label>
          <div class="field has-addons">
            <div class="control">
              <input type="number" class="input is-rounded" min="1" max="20" v-model=" quantity " placeholder="Menge">
            </div>
            <div class="control">
              <a class="button" @click=" addToWishlist ">
                <span class="icon"><i class="fas fa-plus" style="color:#398378;"></i></span>
              </a>
            </div>
          </div>
        </div>
      </div>
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
      images: [],
      currentIndex: 0,
      sections: [],
      currentPreview: null,
      currentIndex: 0,
    };
  },
  mounted() {
    this.sections = this.getSections();
    this.getProduct();
  },
  methods: {
    updatePreview() {
      this.currentPreview = this.product.get_images[this.currentIndex].url;
    },
    getSections() {
      const path = this.$route.path;
      return path.split('/').filter(section => section !== '');
    },
    getUrl(index) {
      return '/' + this.sections.slice(0, index + 1).join('/') + '/';
    },
    getProduct() {
      this.$store.commit("setIsLoading", true);

      const category_slug = this.$route.params.category_slug;
      const product_slug = this.$route.params.product_slug;

      console.log(product_slug)

      axios
        .get(`/api/v1/products/${category_slug}/${product_slug}/`)
        .then((response) => {
          this.product = response.data;
          this.currentPreview = this.product.get_images[0].url;
          this.product.date_added = new Date(this.product.date_added).toLocaleDateString();
          document.title = this.product.name + " | Leihladen";
          this.images = this.product.get_images.map((image) => image.url);
        })
        .catch((error) => {
          console.log(error);
          //Wenn Fehler auftritt zurück auf Startseite leiten
          // this.$router.push("/")
        });

      this.$store.commit("setIsLoading", false);
    },
    addToWishlist() {
      if (isNaN(this.quantity) || this.quantity < 1) {
        this.quantity = 1;
      }
      if (this.quantity > 20) {
        this.quantity = 20
      }

      const item = {
        product: this.product,
        quantity: this.quantity,
      };

      this.$store.commit("addToWishlist", item);

      toast({
        message: `Der Artikel "${this.product.name}" wurde ${this.quantity}x zur Wunschliste hinzugefügt`,
        type: "is-success",
        dismissible: true,
        pauseOnHover: true,
        duration: 4000,
        position: "bottom-right",
      });
    },
  }
};
</script>

<style scoped>
.highlight {
  border: 2px solid transparent;
  transition: border-color 0.3s, transform 0.3s;
}

.highlight:hover {
  border-color: #398378;
  transform: scale(1.05);
  border-radius: 5px;
}

.breadcrumb {
  color: grey;
  justify-content: left;
  background-color: #fff;
}

.breadcrumb li a:hover {
  color: black;

}

.breadcrumb li a {
  color: inherit;
  text-decoration: none;
}

.breadcrumb li .icon {
  margin-top: 5px;
}

.thumbnails {
  margin-top: 20px;
}

.thumbnail img {
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}
</style>