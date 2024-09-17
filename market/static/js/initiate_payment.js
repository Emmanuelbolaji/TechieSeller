/**
 * Initiates a payment process using Paystack.
 *
 * This function sets up and starts the payment process by calling the `payWithPaystack` function.
 * It generates a unique reference for the payment and provides necessary details like
 * the public key, email, amount, item ID, user ID, and callback URL.
 *
 * @param {string} publicKey - Your Paystack public key.
 * @param {string} email - The email address of the user making the payment.
 * @param {number} amount - The amount to be charged, in kobo (1 kobo = 0.01 NGN)
 * @param {string} itemId - The ID of the item being purchased.
 * @param {string} userId - The ID of the user making the payment.
 * @param {string} callbackUrl - The URL to redirect to after the payment process is complete.
 */


function initiatePayment(publicKey, email, amount, itemId, userId, callbackUrl) {
	payWithPaystack(
		publicKey,
		email,
		amount,
		'purchase_' + itemId + '_' + userId + '_' + Math.floor((Math.random() * 1000000000) + 1),
		callbackUrl
	);
}

