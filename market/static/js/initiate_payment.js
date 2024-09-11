function initiatePayment(publicKey, email, amount, itemId, userId, callbackUrl) {
	payWithPaystack(
		publicKey,
		email,
		amount,
		'purchase_' + itemId + '_' + userId + '_' + Math.floor((Math.random() * 1000000000) + 1),
		callbackUrl
	);
}

