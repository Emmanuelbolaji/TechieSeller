document.addEventListener('DOMContentLoaded', function() {
	// Get references to DOM elements
	const searchInput = document.getElementById('searchInput');
	const itemsTableBody = document.getElementById('itemsTableBody');
	const noMatchMessage = document.getElementById('noMatchMessage');

	/**
	* Filters table rows based on the search input value.
	*/
	searchInput.addEventListener('input', function() {
		const searchTerm = this.value.toLowerCase();
		const rows = itemsTableBody.getElementsByTagName('tr');
		let matchFound = false;

		for (let row of rows) {
			const name = row.cells[0].textContent.toLowerCase();
			const price = row.cells[1].textContent.toLowerCase();
			const barcode = row.cells[2].textContent.toLowerCase();

			if (name.includes(searchTerm) || price.includes(searchTerm) || barcode.includes(searchTerm)) {
				row.style.display = '';if (name.includes(searchTerm) || price.includes(searchTerm) || barcode.includes(searchTerm)) {
					row.style.display = '';
					matchFound = true;
				} else {
					row.style.display = 'none';
				}
			}

			noMatchMessage.style.display = matchFound ? 'none' : 'block';
		});
	});

