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
                <option value="asc" v-if="sortBy == 'date_added'">Neueste</option>
                <option value="desc" v-if="sortBy == 'date_added'">Älteste</option>
                <option value="asc" v-if="sortBy != 'date_added'">Aufsteigend</option>
                <option value="desc" v-if="sortBy != 'date_added'">Absteigend</option>
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
    // Die isLoading-Flag im globalen Store auf true setzen, um einen Ladeindikator anzuzeigen
    this.$store.commit("setIsLoading", true);
    this.getCategory();
  },
  watch: {
    $route(to, from) {
      // Wenn die Route zu einer Kategorie-Seite führt, getCategory() aufrufen, um die Kategorieinformationen zu aktualisieren
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
          // Stoppen des Lade-Spinners
          this.$store.commit("setIsLoading", false);

          // Sortieren der Produkte nach den gewählten Kriterien
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
      if (this.sortDirection === 'desc') { // Wenn die Sortierrichtung absteigend ist, wird der Sortierfaktor negativ gesetzt.
        sortFactor = -1;
      }
      switch (this.sortBy) { // Je nach ausgewähltem Sortierkriterium wird die Liste der Produkte sortiert.
        case 'name':
          this.category.products.sort((a, b) => sortFactor * a.name.localeCompare(b.name)); // Sortiert die Produkte nach dem Namen.
          break;
        case 'deposit':
          this.category.products.sort((a, b) => sortFactor * (a.deposit - b.deposit)); // Sortiert die Produkte nach der Kaution.
          break;
        case 'fee':
          this.category.products.sort((a, b) => sortFactor * (a.fee - b.fee)); // Sortiert die Produkte nach der Gebühr.
          break;
        default:
          this.category.products.sort((a, b) => sortFactor * (new Date(b.date_added) - new Date(a.date_added))); // Sortiert die Produkte nach dem Hinzufügungsdatum.
          break;
      }

      this.currentPage = 1 // Setzt die aktuelle Seite auf die erste Seite, wenn die Sortierung geändert wird.
    }
  },
  watch: {
    totalPages(newTotal, oldTotal) {
      // Überprüft, ob es nur eine Seite gibt und die aktuelle Seite mehr als 1 ist
      if (newTotal === 1 && oldTotal > 1) {
        this.currentPage = 1;
      }
      // Überprüft, ob die aktuelle Seite außerhalb des Bereichs der Seitenzahl liegt
      else if (this.currentPage > newTotal) {
        this.currentPage = newTotal;
      }
    }
  },
  computed: {
    // Berechnet die Gesamtzahl der Seiten
    totalPages() {
      return Math.ceil(this.category.products.length / this.itemsPerPage);
    },
    visibleProducts() {
      // Bestimmt den Start- und Endindex der sichtbaren Produkte
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      // Gibt eine neue Liste mit den sichtbaren Produkten zurück
      return this.category.products.slice(start, end);
    }
  }
};
</script>