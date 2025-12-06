// src/hooks.server.ts
export const handle = async ({ event, resolve }) => {
	// 1. Get the cookie we set in the login action
	const token = event.cookies.get('access_token');

	if (token) {
		// Optional: Verify token with FastAPI here if you want extra security
		// For now, we trust the cookie existence
		event.locals.user = {
			isAuthenticated: true,
			token: token
		};
	} else {
		event.locals.user = null;
	}

	return resolve(event);
};
