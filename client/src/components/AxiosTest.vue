<template>
  <div>


<h1>Loosely Tobacco Width Detection <span class="badge badge-secondary">AIMS</span></h1>

    <div >
        <div class="input-group">
        <div class="input-group-prepend">
          <span class="input-group-text" id="inputGroupFileAddon01">Upload</span>
        </div>
        <div class="custom-file">
          <input type="file" ref="file" class="custom-file-input" id="inputGroupFile01"
            aria-describedby="inputGroupFileAddon01" @change="selectFile">
          <label class="custom-file-label" for="inputGroupFile01">Choose file</label>
        </div>
        <button class="btn btn-success"  @click="fetchName">
          Upload
        </button>



    
      </div>

<h1 v-if="is_process">Working Hard To Process😎 </h1>
<h1 v-else>Waiting For Your new Tabacoo 😁</h1>


    </div>
    <picture style="text-align: center;">
      <div v-for="(image,i) in images" :key="i" class="img" style="text-align: center;">



        <div class="card" style="width: 18rem; text-align: center;">
  <img class="card-img-top" :src="image.filename" :title="image.name" alt="Card image cap">
  <div class="card-body">
    <h5 class="card-title">{{image.name}}</h5>
  </div>
</div>

      </div>
    </picture>


  


    <div>
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
      images:'',
      is_process:false
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
      this.is_process = true;
      axios
        .get(baseURL)
        .then((response)=> {
          console.log(response.data);
          this.info = response.data['response'];
          this.images = response.data['files_info'];
          for (var i = 0; i < this.images.length; i++) {
            this.images[i]['filename'] = 'http://127.0.0.1:5000/static/' + this.images[i]['filename']; 
          }
          this.is_process = false;
        }
              // console.log("Get Response");
              // console.log(response);

        ); 
    }
  },

    
};
</script>
