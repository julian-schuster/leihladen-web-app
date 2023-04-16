<template>
  <div class="column is-3">
    <div class="box">
      <figure class="image is-square mb-4">
        <img :src="product.get_thumbnail" />
      </figure>

      <div class="product-info">
        <h3 class="is-size-4 product-name">{{ product.name }}</h3>

        <router-link v-bind:to="product.get_absolute_url" class="button is-dark mt-2 product-button">
          Details
        </router-link>
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
};
</script>

<style scoped>
.image {
  margin-top: -1.25rem;
  margin-left: -1.25rem;
  margin-right: -1.25rem;
}
</style>