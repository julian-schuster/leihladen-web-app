<template>
  <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
    <div class="lds-dual-ring"></div>
  </div>
  <div class="container" v-if="!$store.state.isLoading">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">{{ category.name }}</h2>
        <h2 class="is-size-5 has-text-grey has-text-centered"> {{ this.category.products.length
        }} Artikel</h2>
      </div>
      <div class="column is-12">
        <div class="field">
          <label class="label">Sortieren nach:</label>
          <div class="control">
            <div class="select" style="margin-right:5px">
              <select v-model="sortBy" @change="sortByCriteria">
                <option value="date_added">Hinzugefügt am</option>
                <option value="name">Name</option>
                <option value="deposit">Kaution</option>
                <option value="fee">Leigehbühr</option>
              </select>
            </div>
            <div class="select">
              <select v-model="sortDirection" @change="sortByCriteria">
                <option value="asc">Aufsteigend</option>
                <option value="desc">Absteigend</option>
              </select>
            </div>
          </div>
        </div>
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
      sortBy: 'date_added',
      sortDirection: 'asc'
    };
  },
  components: { ProductBox, Pagination },
  mounted() {
    this.$store.commit("setIsLoading", true);
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

      axios
        .get(`/api/v1/products/${categorySlug}/`)
        .then((response) => {
          this.category = response.data;
          document.title = this.category.name + " | Leihladen";
          this.$store.commit("setIsLoading", false);
          this.sortByCriteria();
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

          this.$router.push("/")

        });
    },
    onPageChange(page) {
      this.currentPage = page;
    },
    sortByCriteria() {
      let sortFactor = 1;
      if (this.sortDirection === 'desc') {
        sortFactor = -1;
      }
      switch (this.sortBy) {
        case 'name':
          this.category.products.sort((a, b) => sortFactor * a.name.localeCompare(b.name));
          break;
        case 'deposit':
          this.category.products.sort((a, b) => sortFactor * (a.deposit - b.deposit));
          break;
        case 'fee':
          this.category.products.sort((a, b) => sortFactor * (a.fee - b.fee));
          break;
        default:
          this.category.products.sort((a, b) => sortFactor * (new Date(b.date_added) - new Date(a.date_added)));
          break;
      }

      this.currentPage = 1
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