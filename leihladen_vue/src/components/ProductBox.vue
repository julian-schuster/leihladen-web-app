<template>
  <div class="column is-3-desktop is-6-tablet">
    <div class="box highlight">
      <div class="columns is-centered is-mobile">
        <div class="column is-12 is-12-mobile">
          <figure class="image is-square ">
            <img :src="product.get_image">
          </figure>
        </div>
      </div>
      <div class="product-info">
        <h3 class="title is-size-4-desktop is-size-5-mobile is-clipped has-text-centered">{{ product.name }}</h3>
        <div class="columns">
          <div class="column details">
            <router-link :to="product.get_absolute_url" class="button is-success is-fullwidth">
              Details
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
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
    getProducts() {
      axios
        .get(`/api/v1/products`)
        .then((response) => {
          this.products = response.data.products
          console.log(this.products);
        })
        .catch((error) => {
          console.log(error);
        });
    },
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
  border-color: #ddd;
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