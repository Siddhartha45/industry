document.addEventListener("DOMContentLoaded", function() {
  // Get the table and all the input fields
  const table = document.getElementById("industryList");
  const searchInput = document.getElementById("search");
  const investmentInput = document.getElementById("investmentInput");
  const productInput = document.getElementById("productInput");
  const ownershipInput = document.getElementById("ownershipInput");
  const resetButton = document.getElementById("reset");

  // Add an event listener to each input field that filters the table when it changes
  searchInput.addEventListener("input", filterTable);
  investmentInput.addEventListener("change", filterTable);
  productInput.addEventListener("change", filterTable);
  ownershipInput.addEventListener("change", filterTable);
  resetButton.addEventListener("click", resetFields);

  // Define the filterTable function
  function filterTable() {
    const searchValue = searchInput.value.trim().toLowerCase();
    const investmentValue = investmentInput.value;
    const productValue = productInput.value;
    const ownershipValue = ownershipInput.value;
  
    // Split the search value into individual words
    const searchWords = searchValue.split(' ');
  
    // Loop through all the rows in the table and hide/show them based on the filter values
    for (let i = 1; i < table.rows.length; i++) {
      const row = table.rows[i];
      const investment = row.cells[1].textContent.trim().toLowerCase();
      const product = row.cells[2].textContent.trim().toLowerCase();
      const ownership = row.cells[3].textContent.trim().toLowerCase();
  
      let match = true;
  
      // Check if any of the row columns matches any of the search words
      for (let j = 0; j < searchWords.length; j++) {
        const searchWord = searchWords[j];
        if (searchWord !== "" && investment.indexOf(searchWord) == -1 && ownership.indexOf(searchWord) == -1 && product.indexOf(searchWord) == -1) {
          match = false;
          break;
        }
      }
  
      // Check if the row matches the investment filter
      if (investmentValue !== "None" && investment.toLowerCase() !== investmentValue.toLowerCase()) {
        match = false;
      }
  
      // Check if the row matches the ownership filter
      if (ownershipValue !== "None" && ownership.toLowerCase() !== ownershipValue.toLowerCase()) {
        match = false;
      }
  
      // Check if the row matches the product filter
      if (productValue !== "None" && product.toLowerCase() !== productValue.toLowerCase()) {
        match = false;
      }
  
      // Show/hide the row based on the match variable
      if (match) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    }
  }
  
  

  // Define the resetFields function
  function resetFields() {
    // Reset the values of all input fields to their default values
    searchInput.value = "";
    investmentInput.value = "None";
    productInput.value = "None";
    ownershipInput.value = "None";

    // Trigger the filterTable function to show all rows
    filterTable();
  }
});