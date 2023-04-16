<template>
  <div class="column is-3">
    <div class="box">
      <div class="column is-12 is-12-mobile">
        <figure class="image is-square">
          <img v-bind:src="product.get_thumbnail">
        </figure>
      </div>
      <div class="product-info">
        <h3 class="is-size-4 product-name">{{ product.name }}</h3>
        <div class="columns">

          <div class="column">
            <table class="table">
              <thead>
                <th>Bestand</th>
                <th>Verfügbar</th>
              </thead>
              <tbody>
                <tr>
                  <td>{{ product.count }}</td>
                  <td>{{ product.available }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="column has-text-right">
            <router-link v-bind:to="product.get_absolute_url" class="button mt-2 is-dark product-button">
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
</style>