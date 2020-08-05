
<template>
  <div>
    <nav class="navbar">
      <form class="searchbar">
        <label>
          <span class='screen-reader-only'>Search:</span>
          <input 
            v-model="tag" 
            placeholder="Search for photos"
            type="text" 
            class="searchbar-input">
        </label>
        <button 
          type="submit" 
          class="btn btn--green btn--go" 
          @click.prevent="search">
            Go
        </button>
      </form>
    </nav>
   <div class="wrapper">
      <p v-if="loading" class="text-centered">
        Loading...
      </p>
      <ul v-else class="image-card-grid">
        <image-card
          v-for="image in images"
          :key="image.id"
          :image="image" />
      </ul>
   </div>
  </div>
</template>

<script>
// import config from '../../config';
import axios from 'axios';
import ImageCard from '@/components/ImageCard';
export default {
  name: 'home',
  components: {
    ImageCard
  },
  data() {
    return {
      loading: false,
      tag: '',
      images: []
    }
  },
  methods: {
    search() {
      this.loading = true;
      this.fetchImages()
        .then((response) => {
          this.images = response.data.photos.photo;
          this.loading = false;
        })
        .catch((error) => {
          console.log("An error ocurred: ", error);
        })
    },
    fetchImages() {
      return axios({
        method: 'get',
        url: 'https://api.flickr.com/services/rest',
        params: {
          method: 'flickr.photos.search',
          api_key: 'bc6d10133b5d0c3fea70d2e6b47994fd',
          tags: this.tag,
          extras: 'url_n, owner_name, date_taken, views',
          page: 1,
          format: 'json',
          nojsoncallback: 1,
          per_page: 30,
        }
      })
    },
  }
};
</script>
