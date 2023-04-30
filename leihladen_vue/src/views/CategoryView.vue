<template>
  <div class="page-category container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">{{ category.name }}</h2>
      </div>
      <ProductBox v-for="product in category.products" v-bind:key="product.id" v-bind:product="product" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";
import ProductBox from "@/components/ProductBox";

export default {
  name: "Category",
  data() {
    return {
      category: {
        products: [],
      },
    };
  },
  components: { ProductBox },
  mounted() {
    this.getCategory();
  },
  watch: {
    $route(to, from) {
      if (to.name === "Category") {
        this.getCategory();
      }
    },
  },
  methods: {
    async getCategory() {
      const categorySlug = this.$route.params.category_slug;

      this.$store.commit("setIsLoading", true);

      axios
        .get(`/api/v1/products/${categorySlug}/`)
        .then((response) => {
          this.category = response.data;
          document.title = this.category.name + " | Leihladen";
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
          //Wenn Fehler auftritt zurück auf Startseite leiten
          this.$router.push("/")
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>