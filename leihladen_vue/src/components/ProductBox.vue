<template>
  <div class="column is-3-desktop is-6-tablet">
    <div class="box">
      <div class="columns is-centered is-mobile">
        <div class="column is-12 is-12-mobile">
          <figure class="image is-square">
            <img :src="product.get_thumbnail">
          </figure>
        </div>
      </div>
      <div class="product-info">
        <h3 class="title is-size-4-desktop is-size-5-mobile is-clipped">{{ product.name }}</h3>
        <div class="columns is-mobile">
          <div class="column">
            <table class="table is-narrow">
              <thead>
                <tr>
                  <th>Bestand</th>
                  <th>Verfügbar</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{{ product.quantity }}</td>
                  <td>{{ product.available }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="columns is-centered is-mobile">
          <div class="column is-narrow">
            <router-link :to="product.get_absolute_url" class="button is-dark is-rounded">
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

.is-clipped {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-bottom: 5px
}
</style>