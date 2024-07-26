document.addEventListener("DOMContentLoaded", function () {
  // Clear any existing Dropzone instances from the element
  Dropzone.instances.forEach((instance) => {
    if (instance.element.id === "dropFile") {
      instance.destroy(); // Destroy the existing instance
    }
  });

  // Initialize Dropzone
  let myDropzone = new Dropzone("#dropFile", {
    url: "/target", // Specify your upload URL here
  });

  myDropzone.on("addedfile", (file) => {
    console.log(`File added: ${file.name}`);
  });

  myDropzone.on("error", (file, response) => {
    console.error(`Error uploading ${file.name}:`, response);
  });

  myDropzone.on("success", (file, response) => {
    console.log(`Successfully uploaded ${file.name}:`, response);
  });
});
