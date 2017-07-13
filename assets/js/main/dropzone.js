Dropzone.options.movieDropzone = { 
// The configuration we've talked about above
  autoProcessQueue: true,
  uploadMultiple: true,
  parallelUploads: 100,
  maxFiles: 10,
  url: "/upload/decision",
  acceptedFiles: "image/*,.doc,.docx,.pdf,.xls,.xlsx",
  
  // The setting up of the dropzone
  init: function() {
    var myDropzone = this;
  
    // Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
    // of the sending event because uploadMultiple is set to true.
    this.on('sending', function (data, xhr, formData) {
      $("#movie-form :input").each(function() {
        name = $(this).attr("name");
        if(name != 'undefined') {
          formData.append(name, $(this).val());
        }
      })
      formData.append("Username", $("#slug").val());
    });
  },
  
  success: function(file, response){
    console.log(file);
    console.log(response);
    console.log(response.filename);
    $('#image').val(response.filename);
  }
}
