
const message = document.getElementById("message");
const button = document.getElementById("submitBtn");
const file = document.getElementById("file");


button.addEventListener("click", function (event) {
  if (file.files.length === 0) {
    message.innerHTML = "No File selected, Please select a file!";
  } else {
    message.innerHTML = "Processing Image....";
  }
});