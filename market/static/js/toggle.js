ddEventListener('DOMContentLoaded', function() {
	const dropdownToggle = document.querySelector('.dropdown-toggle');
	const nav = document.querySelector('.header-right nav');

	dropdownToggle.addEventListener('click', function() {
		nav.classList.toggle('active');
	});
});
