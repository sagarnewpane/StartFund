import { fail } from '@sveltejs/kit';

// IMPORTANT: Define your FastAPI URL here.
// Replace 'http://localhost:8000' with your actual backend URL.
const FASTAPI_URL = 'http://localhost:8000';

/** @type {import('./$types').Actions} */
export const actions = {
	// The name 'login' matches the action="?/login" in the form
	login: async ({ request, cookies, fetch }) => {
		// 1. Get form data from the request
		const data = await request.formData();
		const email = data.get('email');
		const password = data.get('password');

		// Basic validation (optional, but good practice)
		if (!email || !password) {
			return fail(400, {
				message: 'Missing email or password.',
				email
			});
		}

		let response;
		try {
			// 2. Prepare data for FastAPI.
			// FastAPI usually expects form data for token authentication.
			const body = new URLSearchParams();
			body.append('username', email); // FastAPI's /token endpoint typically uses 'username' for email/user ID
			body.append('password', password);

			// 3. Call the FastAPI token endpoint
			response = await fetch(`${FASTAPI_URL}/api/login`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				},
				body: body.toString()
			});
		} catch (error) {
			console.error('Network or FastAPI connection error:', error);
			// Return a generic failure message to the client
			return fail(500, {
				message: 'Failed to connect to the authentication server.',
				email
			});
		}

		// 4. Handle authentication failure (e.g., 401 Unauthorized)
		if (!response.ok) {
			const errorData = await response.json();

			// Log the error for server-side debugging
			console.error('Login failed response:', response.status, errorData);

			// Return an error message to the client (LoginModal.svelte)
			return fail(response.status, {
				message: errorData.detail || 'Invalid credentials. Please try again.',
				email
			});
		}

		// 5. Authentication successful! Extract the token.
		const authData = await response.json();
		const jwtToken = authData.access_token;

		// Ensure the token structure is correct (FastAPI usually returns just the token value)
		if (!jwtToken) {
			console.error('FastAPI did not return an access_token:', authData);
			return fail(500, { message: 'Authentication successful but missing token.', email });
		}

		// 6. Set the secure, HttpOnly cookie (THE CRITICAL SECURITY STEP)
		// We prepend 'Bearer ' so the token stored in the cookie is ready for use in hooks.server.js
		cookies.set('jwt', `Bearer ${jwtToken}`, {
			path: '/', // Make the cookie available across the entire site
			httpOnly: true, // Crucial: JavaScript cannot access this cookie
			secure: process.env.NODE_ENV === 'production', // Use 'secure' in production (HTTPS)
			sameSite: 'strict', // Protects against CSRF
			maxAge: 60 * 60 * 24 * 7 // Cookie expires in 7 days
		});

		// 7. Return success. Since we are using a modal with `use:enhance`,
		// we return a success status instead of a redirect.
		return { success: true };
	}
};
