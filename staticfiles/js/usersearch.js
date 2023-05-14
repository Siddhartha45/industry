document.addEventListener("DOMContentLoaded", function() {
  // Get the table and all the input fields
  const table = document.getElementById("userTable");
  const searchInput = document.getElementById("usersearch");
  const roleInput = document.getElementById("role");
  const resetButton = document.getElementById("userreset");

  // Add an event listener to each input field that filters the table when it changes
  searchInput.addEventListener("input", filterTable);
  roleInput.addEventListener("change", filterTable);
  resetButton.addEventListener("click", resetFields);

  // Define the filterTable function
  function filterTable() {
    const searchValue = searchInput.value.trim().toLowerCase();
    const roleValue = roleInput.value;
  
    // Split the search value into individual words
    const searchWords = searchValue.split(' ');
  
    // Loop through all the rows in the table and hide/show them based on the filter values
    for (let i = 1; i < table.rows.length; i++) {
      const row = table.rows[i];
      const role = row.cells[2].textContent.trim().toLowerCase();
  
      let match = true;
  
      // Check if any of the row columns matches any of the search words
      for (let j = 0; j < searchWords.length; j++) {
        const searchWord = searchWords[j];
        if (searchWord !== "" && role.indexOf(searchWord) == -1) {
          match = false;
          break;
        }
      }
  
      // Check if the row matches the role filter
      if (roleValue !== "all" && role.toLowerCase() !== roleValue.toLowerCase()) {
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
    roleInput.value = "all";

    // Trigger the filterTable function to show all rows
    filterTable();
  }
});