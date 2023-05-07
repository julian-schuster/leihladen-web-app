<template>
    <div class="pagination-wrapper">
        <div class="pagination">
            <button v-if="currentPage !== 1" class="button has-text-left" @click="prevPage">Zurück</button>
            <span v-else style="width:80px"></span>
            <div class="current-page-wrapper">
                <span class="has-text-centered">{{ currentPage }}/{{ pageCount }}</span>
            </div>
            <button v-if="currentPage !== pageCount" class="button" @click="nextPage">Weiter</button>
            <span v-else style="width:80px"></span>
        </div>
    </div>
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
  
<style scoped>
.pagination-wrapper {
    display: flex;
    justify-content: center;
}

.pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.current-page-wrapper {
    flex: 1;
    text-align: center;
}

.button {
    width: 80px;
}
</style>
  