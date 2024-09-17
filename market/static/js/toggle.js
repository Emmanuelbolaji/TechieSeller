/**
 * Initializes the dropdown menu functionality when the DOM content is fully loaded.
 *
 * This function sets up an event listener on a dropdown toggle element to show or hide
 * the navigation menu when the toggle is clicked.
 */

document.addEventListener('DOMContentLoaded', function() {
	const dropdownToggle = document.querySelector('.dropdown-toggle');
	const nav = document.querySelector('.header-right nav');

	dropdownToggle.addEventListener('click', function() {
		nav.classList.toggle('active');
	});
});
