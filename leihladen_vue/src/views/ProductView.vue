<template>
  <div class="container" v-if="product.name">
    <nav class="breadcrumb" aria-label="breadcrumbs">
      <ul>
        <li><a href="/"><span class="icon"><i class="fas fa-home"></i></span></a></li>
        <li v-for="(section, index) in sections" :key="index" :class="{ 'is-active': index === sections.length }">
          <span>
            <a :href="getUrl(index)" style="text-transform: capitalize;">
              {{ index === sections.length - 1 ? decodeURIComponent(product.name) : decodeURIComponent(section) }}
            </a>
          </span>
        </li>
      </ul>
    </nav>
    <div class="columns">
      <div class="column is-6">
        <div class="column is-12">
          <div class="image has-text-centered" v-if="!this.isMobile()">
            <div class="responsive-image-container">
              <VueMagnifier :src="currentPreview" v-if="currentPreview" />
            </div>
          </div>
          <div class="thumbnails thumbnail" v-if="images.length > 1 || this.isMobile()">
            <div class="columns is-multiline is-centered">
              <div class="column is-12-mobile is-6-tablet is-3-desktop" v-for="(image, index) in images">
                <figure class="image is-3by2 highlight">
                  <a @click="currentIndex = index; updatePreview()">
                    <img v-bind:src="image" alt="Produktbild">
                  </a>
                </figure>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-6">
        <div class="content">
          <h1 class="title">{{ product.name }}</h1>
          <hr>
          <div class="field">
            <div class="control">
              <span>{{ product.description }}</span>
            </div>
          </div>
          <hr>
          <dl class="is-horizontal">
            <div class="columns">
              <div class="column is-6">
                <div class="field">
                  <label class="label">Gewicht</label>
                  <div class="control">
                    <span>{{ product.weight }}</span>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Dimension</label>
                  <div class="control">
                    <span>{{ product.dimension }}</span>
                  </div>
                </div>
              </div>
              <div class="column is-6">
                <div class="field">
                  <label class="label">Kaution</label>
                  <div class="control">
                    <span>{{ product.deposit }}€</span>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Leihgebühr</label>
                  <div class="control">
                    <span>{{ product.fee }}€</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="columns">
              <div class="column is-6">
                <div class="field">
                  <label class="label">Kleinteile</label>
                  <div class="control">
                    <span v-if="product.smallPieces">Ja</span>
                    <span v-else>Nein</span>
                  </div>
                </div>
              </div>
              <div class="column is-6">
                <div class="field">
                  <label class="label">Bestand</label>
                  <div class="control">
                    <span>{{ product.quantity }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="columns">
              <div class="column is-6">
                <div class="field">
                  <label class="label">Hinzugefügt am</label>
                  <div class="control">
                    <span>{{ product.date_added }}</span>
                  </div>
                </div>
              </div>
              <div class="column is-6">
                <div class="field">
                  <label class="label">Verfügbarkeit</label>
                  <div class="control">
                    <span v-if="product.available == 0" style="color:red"><i class="fas fa-times-circle"></i> Nicht
                      verfügbar</span>
                    <span v-else style="color:green"><i class="fas fa-check-circle"></i> Verfügbar</span>
                  </div>
                </div>
              </div>
            </div>
          </dl>
          <hr>
          <h2 class="subtitle">Zur Wunschliste hinzufügen</h2>
          <div class="field has-addons">
            <div class="control">
              <input type="number" class="input is-rounded" min="1" :max="product.quantity" v-model="quantity"
                placeholder="Menge">
            </div>
            <div class="control">
              <a class="button" @click="addToWishlist">
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
import VueMagnifier from '@websitebeaver/vue-magnifier'
import '@websitebeaver/vue-magnifier/styles.css'

export default {
  name: "Product",
  components: {
    VueMagnifier
  },
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
      this.currentPreview = this.product.get_images[this.currentIndex];
    },
    getSections() {
      const path = this.$route.path;
      return path.split('/').filter(section => section !== '');
    },
    getUrl(index) {
      return '/' + this.sections.slice(0, index + 1).join('/') + '/';
    },
    isMobile() {
      if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        return true
      } else {
        return false
      }
    },
    getProduct() {
      this.$store.commit("setIsLoading", true);

      const category_slug = this.$route.params.category_slug;
      const product_slug = this.$route.params.product_slug;

      axios
        .get(`/api/v1/products/${category_slug}/${product_slug}/`)
        .then((response) => {
          this.product = response.data;
          this.currentPreview = this.product.get_images[0];
          this.product.date_added = new Date(this.product.date_added).toLocaleDateString();
          document.title = this.product.name + " | Leihladen";
          this.images = this.product.get_images;
        })
        .catch((error) => {
          console.log(error);
          //Wenn Fehler auftritt zurück auf Startseite leiten
          // this.$router.push("/")
        });

      this.$store.commit("setIsLoading", false);
    },
    addToWishlist() {
      const item = {
        product: this.product,
        quantity: this.quantity,
      };

      const localUserWishlist = JSON.parse(JSON.stringify(this.$store.state.wishlist));
      const filteredProduct = localUserWishlist.items.filter(item => item.product.id == this.product.id);

      // Überprüfen, ob die Gesamtmenge des Artikels ausreicht, um den Artikel zur Wunschliste hinzuzufügen
      if (filteredProduct.length === 0) {
        if (this.product.quantity < this.quantity) {
          toast({
            message: `Sie können nicht mehr Artikel zur Wunschliste hinzufügen, als aktuell im Bestand sind.`,
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 4000,
            position: "bottom-right",
          });
          return;
        }
      } else if (filteredProduct.length === 1) {
        const totalQuantity = filteredProduct[0].product.quantity;
        const wishlistQuantity = filteredProduct[0].quantity;
        const newQuantity = this.quantity;

        if (wishlistQuantity + newQuantity > totalQuantity) {
          toast({
            message: `Die Gesamtmenge des Artikels "${this.product.name}" auf Ihrer Wunschliste entspricht bereits dem Bestand.`,
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 4000,
            position: "bottom-right",
          });
          return;
        }
      }

      if (item.quantity > 0) {
        this.$store.commit("addToWishlist", item);

        toast({
          message: `Der Artikel "${this.product.name}" wurde ${this.quantity}x zur Wunschliste hinzugefügt`,
          type: "is-success",
          dismissible: true,
          pauseOnHover: true,
          duration: 4000,
          position: "bottom-right",
        });
      } else if (item.quantity == 0) {
        toast({
          message: `Die Stückzahl muss mindestens 1 betragen.`,
          type: "is-danger",
          dismissible: true,
          pauseOnHover: true,
          duration: 4000,
          position: "bottom-right",
        });
      }

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

@media (max-width: 768px) {
  .label {
    text-align: center;
  }

  .subtitle {
    text-align: center;
  }

  .field.has-addons {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
  }

  .control {
    text-align: center;
  }

  h1 {
    text-align: center;
  }
}
</style>