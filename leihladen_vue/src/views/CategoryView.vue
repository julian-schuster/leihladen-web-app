<template>
  <div class="page-category container">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">{{ category.name }}</h2>
      </div>
      <ProductBox v-for="product in visibleProducts" v-bind:key="product.id" v-bind:product="product" />
      <div class="column is-12">
        <Pagination v-if="category.products.length > 8" :totalItems="category.products.length"
          :itemsPerPage="itemsPerPage" :currentPage="currentPage" :totalPages="totalPages" @input="onPageChange" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";
import ProductBox from "@/components/ProductBox";
import Pagination from '@/components/Pagination.vue'

export default {
  name: "Category",
  data() {
    return {
      category: {
        products: [],

      },
      currentPage: 1,
      itemsPerPage: 8,
    };
  },
  components: { ProductBox, Pagination },
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
        });
      this.$store.commit("setIsLoading", false);
    },
    onPageChange(page) {
      this.currentPage = page;
    },
  },
  watch: {
    totalPages(newTotal, oldTotal) {
      if (newTotal === 1 && oldTotal > 1) {
        this.currentPage = 1;
      } else if (this.currentPage > newTotal) {
        this.currentPage = newTotal;
      }
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.category.products.length / this.itemsPerPage);
    },
    visibleProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.category.products.slice(start, end);
    }
  }
};
</script>