<template>
  <div class="home">
    <div class="container">
      <section>
        <div class="hero-body">
          <div class="container has-text-centered">
            <h1 class="title is-2">Willkommen im Leihladen</h1>
            <h2 class="subtitle is-4">leihen statt kaufen – teilen statt besitzen</h2>
          </div>
        </div>
      </section>
      <hr>
      <section class="section">
        <div class="container">
          <div class="columns is-multiline">
            <div class="column is-12-mobile is-4-desktop">
              <div class="box">
                <h2 class="title is-4">1. Artikel zur Wunschliste hinzufügen</h2>
                <p>Suchen Sie nach den Artikeln, die Sie ausleihen möchten. Sobald Sie einen Artikel gefunden haben, den
                  Sie ausleihen möchten, klicken Sie auf die Schaltfläche 'Zur Wunschliste hinzufügen'. Sie können so
                  viele Artikel wie Sie möchten zur Wunschliste hinzufügen.</p>
              </div>
            </div>
            <div class="column is-12-mobile is-4-desktop">
              <div class="box">
                <h2 class="title is-4">2. Wunschliste abschließen und QR-Code erhalten</h2>
                <p>Wenn Sie mit dem Hinzufügen von Artikeln zur Wunschliste fertig sind, gehen Sie zur Wunschliste und
                  überprüfen Sie, ob alle Artikel korrekt sind. Wenn alles stimmt, können Sie die Wunschliste abschließen
                  und erhalten einen QR-Code. Sie können den QR-Code entweder auf Ihrem Smartphone speichern, die
                  Wunschlisten Seite offen haben
                  oder die Wunschliste ausdrucken und zum Leihladen bringen.</p>
              </div>
            </div>
            <div class="column is-12-mobile is-4-desktop">
              <div class="box">
                <h2 class="title is-4">3. Artikel ausleihen und zurückgeben</h2>
                <p>Wenn Sie im Leihladen ankommen, zeigen Sie einfach den QR-Code vor und die Mitarbeiter werden Ihnen die
                  Artikel aus Ihrer Wunschliste aushändigen.
                  Preis und Ausleihdauer werden vor Ort besprochen. Um den Prozess der Rückgabe zu erleichtern zeigen Sie
                  wieder den QR-Code der benutzen Wunschliste vor.
                  Artikel können auch ohne QR-Code ausgeliehen und zurückgegeben werden.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
    <hr>
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-3 has-text-centered">Neueste Artikel</h2>
      </div>
      <ProductBox v-for="product in latestProducts" v-bind:key="product.id" v-bind:product="product" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ProductBox from "@/components/ProductBox";

export default {
  name: "HomeView",
  data() {
    return {
      latestProducts: [],
    };
  },
  components: { ProductBox },
  mounted() {
    this.getLatestProducts();

    document.title = "Startseite | Leihladen";
  },
  methods: {
    async getLatestProducts() {
      this.$store.commit("setIsLoading", true);

      await axios
        .get("/api/v1/latest-products/")
        .then((response) => {
          this.latestProducts = response.data;
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>

<style scoped>
.box {
  height: 100%;
}

@media screen and (max-width: 768px) {
  .column.is-12-mobile.is-4-desktop {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style>
