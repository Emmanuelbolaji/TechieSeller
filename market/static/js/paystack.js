function payWithPaystack(publicKey, email, amount, ref, callback_url) {
	let handler = PaystackPop.setup({
		key: publicKey,
		email: email,
		amount: amount * 100, // Convert to kobo
		currency: 'NGN',
		ref: ref,
		callback: function(response) {
			window.location.href = callback_url + "?reference=" + response.reference;
		},
		onClose: function() {
			alert('Transaction was not completed, window closed.');
		}});
	handler.openIframe()
