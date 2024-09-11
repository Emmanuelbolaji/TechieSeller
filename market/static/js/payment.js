document.addEventListener('DOMContentLoaded', function() {
	const form = document.querySelector('form');
	const confirmButton = document.querySelector('.payment-button');

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
