/**
 * Initializes and starts a Paystack payment process.
 *
 * @param {string} publicKey - The Paystack public key for your account.
 * @param {string} email - The email address of the customer making the payment.
 * @param {number} amount - The amount to be charged, in Naira. This will be converted to kobo.
 * @param {string} ref - A unique reference for the transaction.
 * @param {string} callback_url - The URL to redirect to after the payment is processed.
 */

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
