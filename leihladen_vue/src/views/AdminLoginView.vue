<template>
    <div class="container page-admin-login">
        <div class="columns">
            <div class="column is-4 is-offset-4 box">
                <h1 class="title">Admin Login</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Login</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'AdminLogin',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    mounted() {
        // Setzt den Titel des Dokuments
        document.title = 'Admin Login | Leihladen'

        // Wenn der Benutzer bereits authentifiziert ist, wird er automatisch zur Admin-Oberfläche umgeleitet
        if (this.$store.state.isAuthenticated) {
            this.$router.push("/adminpanel")
        }

    },
    methods: {
        async submitForm() {
            // Setzt den Autorisierungsheader auf einen leeren String und löscht den Token aus dem lokalen Speicher
            axios.defaults.headers.common['Authorization'] = ""
            localStorage.removeItem("token")

            // Formular-Daten werden in einem Objekt gespeichert
            const formData = {
                username: this.username,
                password: this.password
            }

            // Sendet einen POST-Request an den Server, um einen neuen Token zu erhalten
            await axios.post("/api/v1/token/login", formData).then(response => {
                // Holt den Token aus der Server-Antwort und speichert ihn im Vuex-Store und im lokalen Speicher
                const token = response.data.auth_token
                this.$store.commit('setToken', token)
                axios.defaults.headers.common['Authorization'] = "Token " + token
                localStorage.setItem("token", token)

                // Weiterleitung zur ursprünglichen Seite oder zur Admin-Oberfläche
                const toPath = this.$route.query.to || '/adminpanel'
                this.$router.push(toPath)
            }).catch(error => {
                // Wenn ein Fehler auftritt dem Benutzer anzeigen
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                } else {
                    this.errors.push('Etwas ist schiefgelaufen. Bitte nochmal versuchen.')
                    console.log(JSON.stringify(error));
                }
            })
        }
    }
}
</script>