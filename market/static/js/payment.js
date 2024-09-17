document.addEventListener('DOMContentLoaded', function() {
	// Get references to form and payment button elements
	const form = document.querySelector('form');
	const confirmButton = document.querySelector('.payment-button');

	/**
	 * Handles form submission.
	 * Prevents default form submission behavior, disables the payment button,
	 * simulates payment processing, and then submits the form after a short delay.
	 * Updates the button text to show processing and confirmation states.
	 */
	form.addEventListener('submit', function(e) {
		e.preventDefault();
		confirmButton.disabled = true;
		confirmButton.textContent = 'Processing...';

		// Simulate payment processing
		setTimeout(() => {
			confirmButton.textContent = 'Payment Confirmed!';
		        confirmButton.classList.add('payment-confirmed');

			// Actually submit the form after a delay
			setTimeout(() => {
				form.submit();
			}, 1000);
		}, 2000);
	});

	// Add hover effect
	confirmButton.addEventListener('mouseover', function() {
		this.style.transform = 'scale(1.05)';
	});

	confirmButton.addEventListener('mouseout', function() {
		this.style.transform = 'scale(1)';
	});
});
