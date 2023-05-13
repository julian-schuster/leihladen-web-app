<template>
  <router-link :to="product.get_absolute_url" class="column is-3-desktop is-6-tablet">
    <div class="box highlight">
      <div class="columns is-centered is-mobile">
        <div class="column is-12 is-9-mobile">
          <figure class="image is-square">
            <img :src="product.get_image">
          </figure>
        </div>
      </div>
      <div class="product-info">
        <div class="title is-size-4-desktop is-size-5-mobile is-clipped has-text-centered">{{ product.name }}</div>
        <div class="subtitle is-6 has-text-centered" style="margin-bottom: 5%;">Kaution: {{
          currencyFormatter.format(product.deposit) }}</div>
        <div class="subtitle is-6 has-text-centered" style="margin-bottom: 5%;">Leihgebühr: {{
          currencyFormatter.format(product.fee) }}</div>
        <div class="subtitle is-6 has-text-centered">Hinzugefügt am: {{ formatDate(product.date_added) }}
        </div>
        <div class="columns">
          <div class="column details has-text-centered">
            <p class="subtitle is-5" v-if="product.available == 0" style="color:red; font-size: 14pt; margin-bottom:5%"><i
                class="fas fa-times-circle"></i>
              Nicht verfügbar</p>
            <p class="subtitle is-5" v-else style="color:green;font-size: 14pt;  margin-bottom:5%"><i
                class="fas fa-check-circle"></i>
              Verfügbar
            </p>
          </div>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script>

import { format } from 'date-fns'

export default {
  name: "ProductBox",
  props: {
    product: Object,
  },
  data() {
    return {

    }
  },
  methods: {
    formatDate(date) {
      return format(new Date(date), 'dd.MM.yyyy')
    }
  },
  mounted() {

  },
  computed: {
    currencyFormatter() {
      return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 2,
      });
    },
  }

};
</script>

<style scoped>
.image {
  margin-top: -0.5rem;
  margin-left: -0.5rem;
  margin-right: -0.5rem;
}

.is-clipped {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-bottom: 5px
}

.highlight {
  border: 2px solid transparent;
  border-style: solid;
  border-color: rgb(228, 224, 224);
}

.highlight:hover {
  background-color: rgb(245, 245, 245);
}

.button {
  text-align: center;
  color: #fff;
  width: 100%;
  padding: 0;
  border: 0px;
  outline: none;
  margin-top: 5px;
}

.details {
  padding: 0;
}
</style>