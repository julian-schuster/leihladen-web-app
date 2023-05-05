<template>
  <div class="container">
    <div class="columns">
      <div class="column is-5">
        <figure class="image">
          <img class="is-rounded" style="width: 60%; height: 60%;" src="@/assets/leihladen_logo.png">
        </figure>
      </div>
      <div class="column is-7" style="margin-top:5%">
        <h1 class="title is-2">Willkommen im Leihladen</h1>
        <h2 class="subtitle is-4">leihen statt kaufen - teilen statt besitzen</h2>
        <form method="get" action="/search">
          <div class="field has-addons">
            <div class="control" style="width: 80%;">
              <input type="text" class="input is-rounded" placeholder="Nach Artikel suchen" name="query">
            </div>
            <div class="control">
              <button class="button">
                <span class="icon">
                  <i class="fas fa-search" style="color:#398378;"></i>
                </span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
    <hr>
    <div class="column is-12">
      <h1 class="title is-4">Neueste Artikel</h1>
      <div class="columns is-multiline">
        <ProductBox v-for="product in latestProducts" v-bind:key="product.id" v-bind:product="product" />
      </div>
    </div>
    <hr>
    <section class="section">
      <div class="container">
        <div class="columns is-multiline">
          <div class="column is-12-mobile is-4-desktop">
            <div class="box highlight">

              <h2 class="title is-4 has-text-centered">1. Artikel zur Wunschliste hinzufügen</h2>
              <div class="has-text-centered"> <span class="icon" style="margin-bottom:20px"><i class="fas fa-list fa-2x"
                    style="color: #EFA00B;"></i></span></div>

              <p>Suchen Sie nach den Artikeln, die Sie ausleihen möchten. Sobald Sie einen Artikel gefunden haben, den
                Sie ausleihen möchten, klicken Sie auf die Schaltfläche 'Zur Wunschliste hinzufügen'. Sie können so
                viele Artikel wie Sie möchten zur Wunschliste hinzufügen.</p>
            </div>
          </div>
          <div class="column is-12-mobile is-4-desktop">
            <div class="box highlight">
              <h2 class="title is-4 has-text-centered">2. Wunschliste abschließen und QR-Code erhalten</h2>
              <div class="has-text-centered"> <span class="icon" style="margin-bottom:20px"><i
                    class="fas fa-qrcode fa-2x"></i></span></div>
              <p>Wenn Sie mit dem Hinzufügen von Artikeln zur Wunschliste fertig sind, gehen Sie zur Wunschliste und
                überprüfen Sie, ob alle Artikel korrekt sind. Wenn alles stimmt, können Sie die Wunschliste abschließen
                und erhalten einen QR-Code. Sie können den QR-Code entweder auf Ihrem Smartphone speichern, die
                Wunschlisten Seite offen haben
                oder die Wunschliste ausdrucken und zum Leihladen bringen.</p>
            </div>
          </div>
          <div class="column is-12-mobile is-4-desktop">
            <div class="box highlight">
              <h2 class="title is-4 has-text-centered">3. Artikel ausleihen und zurückgeben</h2>
              <div class="has-text-centered"> <span class="icon" style="margin-bottom:20px"><i class="fas fa-share fa-2x"
                    style="color: #398378;"></i></span></div>
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

  .title {
    font-size: 18pt;
    text-align: center;
  }

  .subtitle {
    font-size: 14px;
    text-align: center;
  }
}

@media screen and (min-width: 768px) {
  .field.has-addons.has-addons-centered .control input {
    width: 500px;
  }
}

@media screen and (max-width: 768px) {
  .field.has-addons {
    justify-content: center;
  }
}

.highlight {
  border: 2px solid transparent;
  transition: border-color 0.3s, transform 0.3s;
}

.highlight:hover {
  /* border-color: #398378; */
  transform: scale(1.05);
  background-color: rgb(245, 245, 245);
}
</style>
