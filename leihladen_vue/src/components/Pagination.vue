<template>
    <div class="pagination">
        <button class="button" :disabled="currentPage === 1" @click="prevPage">Zurück</button>
        <span>{{ currentPage }}/{{ pageCount }}</span>
        <button class="button" :disabled="currentPage === pageCount" @click="nextPage">Weiter</button>
    </div>

    <!-- <div>
        <button @click="prevPage">Zurück</button>
        <span>{{ currentPage }}/{{ totalPages }}</span>
        <button @click="nextPage">Weiter</button>
    </div> -->
</template>
  
<script>
export default {
    props: {
        currentPage: {
            type: Number,
            required: true,
        },
        totalItems: {
            type: Number,
            required: true
        },
        itemsPerPage: {
            type: Number,
            default: 10
        }
    },
    methods: {
        prevPage() {
            this.$emit('input', this.currentPage - 1);
        },
        nextPage() {
            this.$emit('input', this.currentPage + 1);
        },
    },
    computed: {
        pageCount() {
            return Math.ceil(this.totalItems / this.itemsPerPage);
        },
        pages() {
            const pages = [];
            for (let i = 1; i <= this.pageCount; i++) {
                pages.push(i);
            }
            return pages;
        }
    },
};
</script>
  