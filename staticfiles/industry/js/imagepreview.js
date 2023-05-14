const inputImage = document.getElementById("inputImage");
const displayImage = document.getElementById("displayImage");
const previewText = document.getElementById("kit-img-preview");

inputImage.addEventListener("change", () => {
  const file = inputImage.files[0];
  const reader = new FileReader();
  previewText.style.display = "block";
  reader.onload = () => {
    displayImage.src = reader.result;
  };

  reader.readAsDataURL(file);
});






  // Find the Add button by its ID
  const addButton = document.querySelector("#add");

  // Add a click event listener to the button
  addButton.addEventListener("click", function(e) {
    e.preventDefault();
    // Create a new div with the appended HTML
    const newDiv = document.createElement("div");
    newDiv.innerHTML = `
      <div class="row mb-3">
        <div class="col-sm-3">
          <input type="text" class="form-control kit-form-control" placeholder="Enter your Product Name">
        </div>
        <div class="col-sm-2">
          <select class="form-select kit-form-control" aria-label="Default select example">
            <option value="" selected disabled>B.S.</option>
            <option value="1">2050</option>
            <option value="2">2051</option>
            <option value="3">2052</option>
          </select>
        </div>
        <div class="col-sm-7">
          <input type="text" class="form-control kit-form-control" placeholder="Enter your Industry Capital">
        </div>
      </div>
    `;

    // Insert the new div before the Add button
    addButton.parentNode.insertBefore(newDiv, addButton);
  });
