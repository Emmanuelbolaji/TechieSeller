document.addEventListener('DOMContentLoaded', function() {
	// Get references to modal elements
	const modal = document.getElementById('itemModal');
	const modalContent = document.querySelector('.modal-content');  // Reference to modal content
	const modalItemName = document.getElementById('modalItemName');
	const modalItemDescription = document.getElementById('modalItemDescription');
	const closeBtn = document.getElementsByClassName('close')[0];
	const cancelBtn = document.getElementById('modalCancelButton');

	/**
	 * Opens the modal and sets the item details.
	 *
	 * @param {string} name - The name of the item to display in the modal.
	 * @param {string} description - The description of the item to display in the modal.
	 */
	function openModal(name, description) {
		modalItemName.textContent = name;
		modalItemDescription.textContent = description;
		modal.style.display = 'block';
	}

	/**
	 * Closes the modal by hiding it.
	 */

	function closeModal() {
		modal.style.display = 'none';
	}

	// Event listener for "More Info" buttons
	document.querySelectorAll('.more-info-btn').forEach(button => {
		button.addEventListener('click', function() {
			const itemName = this.getAttribute('data-item-name');
		        const itemDescription = this.getAttribute('data-item-description');
		        openModal(itemName, itemDescription);
		});
	});

	// Close the modal when clicking the close button
	closeBtn.onclick = closeModal;

	// Close the modal when clicking the cancel button
	if (cancelBtn) {
		cancelBtn.onclick = closeModal;
	}

	// Close the modal when clicking outside the modal-content
	window.addEventListener('click', function(event) {
		if (event.target === modal) { 
			closeModal();
		}
	});
});
