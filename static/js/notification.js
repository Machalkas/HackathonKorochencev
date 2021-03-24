function notification(mess, color="blue") {
	new jBox('Notice', {
		content: mess,
        color: color,
        delayOnHover: true,
        showCountdown: true,
		attributes: {
			x: 'left',
			y: 'bottom'
		},
		position: {  // The position attribute defines the distance to the window edges
			x: 50,
			y: 5
		}
	});
}