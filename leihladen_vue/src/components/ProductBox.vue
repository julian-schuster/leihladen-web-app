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
        <div class="subtitle is-6 has-text-centered" v-if="$route.path === '/'">Hinzugefügt am: {{ product.date_added }}
        </div>
        <div class="columns">
          <div class="column details has-text-centered">
            <p class="subtitle is-5" v-if="product.available == 0" style="color:red; font-size: 14pt; margin-bottom:5%"><i
                class="fas fa-times-circle"></i>
              {{ product.available }} verfügbar</p>
            <p class="subtitle is-5" v-else style="color:green;font-size: 14pt;  margin-bottom:5%"><i
                class="fas fa-check-circle"></i>
              {{ product.available }} verfügbar
            </p>
          </div>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script>
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
  },
  mounted() {
    this.product.date_added = new Date(this.product.date_added).toLocaleDateString();
  },

};
</script>

<style scoped>
.image {
  margin-top: -1.25rem;
  margin-left: -1.25rem;
  margin-right: -1.25rem;
}

.is-clipped {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-bottom: 5px
}

.highlight {
  border: 2px solid transparent;
}

.highlight:hover {
  border-color: #398378;
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