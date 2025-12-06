// src/routes/dashboard/+page.server.ts
import { redirect } from '@sveltejs/kit';

export const load = async ({ locals, fetch }) => {
	// 1. Protect the route
	if (!locals.user) {
		throw redirect(302, '/login');
	}

	// 2. Call FastAPI using the token
	const res = await fetch('http://127.0.0.1:8000/users/me', {
		headers: {
			Authorization: `Bearer ${locals.user.token}`
		}
	});

	const profile = await res.json();

	return { profile };
};
