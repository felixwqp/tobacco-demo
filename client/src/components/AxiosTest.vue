<template>
  <div>
   

    <label class="btn btn-default">
      <input type="file" ref="file" @change="selectFile" />
    </label>
    <button class="btn btn-success"  @click="fetchName">
      Upload
    </button>
    <div class="inline-block">
      <div v-for="(image,i) in images" :key="i" class="img">
      <img :src="image.filename" :title="image.name" width="256" height="256" />
    <div class="caption">{{ image.name }}</div>

    </div>
</div>

<table class="table table-striped">
  <thead>
    <tr>
      <th>#Tobacco</th>
      <th>Mean(Pixel)</th>
      <th>Variance(Pixel)</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(strand,i) in info" :key="i">
       <th scope="row">{{ i  }}</th>  
       <td>{{ strand.mean }}</td> 
       <td>{{ strand.var }}</td>  
    </tr>
   </tbody>
</table>
</div>

</template>

<script>
import axios from 'axios';
export default {
  name: "axios-test",
  data() {
    return {
      info: '',
      selectedFiles: null,
      images:''
    }
  },
  methods: {
    // loadImage() {
    //   //  const baseURL = 'http://127.0.0.1:5000/image/';
    //    const axiosInfo = {
    //     method: 'get',
    //     url: 'http://localhost:20449/api/steps',
    //     headers: {
    //       'Content-type': 'image/jpeg'
    //     },
    //     params: {
    //       id: step.id
    //     }
    //  };
    //   console.log(axiosInfo);
    //   axios
    //     .get(baseURL)
    //     .then((response)=> {this.info = response.data;}
    //           // console.log("Get Response");
    //           // console.log(response);

    //     ); 
    
    // },
    selectFile() {
      this.selectedFiles = this.$refs.file.files[0]['name'];
      console.log(this.selectedFiles);
    },
    fetchName: function() {
      const baseURL = 'http://127.0.0.1:5000/name/' + this.selectedFiles;
      console.log(baseURL);
      axios
        .get(baseURL)
        .then((response)=> {
          console.log(response.data);
          this.info = response.data['response'];
          this.images = response.data['files_info'];
          for (var i = 0; i < this.images.length; i++) {
            this.images[i]['filename'] = 'http://127.0.0.1:5000/static/' + this.images[i]['filename']; 
          }
        }
              // console.log("Get Response");
              // console.log(response);

        ); 
    }
  },

    
};
</script>
