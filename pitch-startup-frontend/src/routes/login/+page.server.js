// src/routes/login/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ request, cookies }) => {
		// 1. Get form data from the UI
		const formData = await request.formData();
		const email = formData.get('username')?.toString() ?? '';
		const password = formData.get('password')?.toString() ?? '';

		// 2. Send credentials to FastAPI
		const res = await fetch('http://127.0.0.1:8000/api/login', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ email, password })
		});

		if (!res.ok) {
			return fail(res.status, { message: 'Invalid credentials' });
		}

		const data = await res.json(); // FastAPI returns { access_token: "..." }

		// 3. SECURELY set the cookie here in SvelteKit
		cookies.set('access_token', data.access_token, {
			path: '/',
			httpOnly: true, // Critical: JS cannot read this
			sameSite: 'strict',
			secure: process.env.NODE_ENV === 'production',
			maxAge: 60 * 60 * 24 // 1 day
		});

		// 4. Redirect user
		throw redirect(302, '/');
	}
};
