// base.js/
//
//Flash messages functionality
document.addEventListener('DOMContentLoaded', function() {
	// Automatically close flash messages after 5 seconds
	setTimeout(function() {
		var flashMessages = document.getElementsByClassName('flash-message');
		for (var i = 0; i < flashMessages.length; i++) {
			flashMessages[i].style.display = 'none';
		}
	}, 5000);

	// Close flash message when close button is clicked
	document.addEventListener('click', function(event) {
		if (event.target.closest('.close-btn')) {
			event.target.closest('.flash-message').style.display = 'none';
		}
	});
});

// Modal functionality
document.addEventListener('click', function(event) {
	if (event.target.dataset.toggle === 'modal') {
		var modalId = event.target.dataset.target;
		document.querySelector(modalId).style.display = 'block';
	}
	if (event.target.dataset.dismiss === 'modal') {
		event.target.closest('.modal').style.display = 'none';
	}
});
