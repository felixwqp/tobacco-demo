<template>
  <div>

    <label class="btn btn-default">
      <input type="file" ref="file" @change="selectFile" />
    </label>
    <button class="btn btn-success"  @click="fetchName">
      Upload
    </button>

<table class="table table-striped">
  <thead>
    <tr>
      <th>#</th>
      <th>Mean</th>
      <th>Var</th>
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
      selectedFiles: null

    }
  },
  methods: {
    selectFile() {
      this.selectedFiles = this.$refs.file.files[0]['name'];
      console.log(this.selectedFiles);
    },
    fetchName: function() {
      const baseURL = 'http://127.0.0.1:5000/name/' + this.selectedFiles;
      console.log(baseURL);
      axios
        .get(baseURL)
        .then((response)=> {this.info = response.data;}
              // console.log("Get Response");
              // console.log(response);

        ); 
    }
  },

    
};
</script>
