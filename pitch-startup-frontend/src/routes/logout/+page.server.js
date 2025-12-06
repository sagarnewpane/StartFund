import { redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ cookies }) => {
		// 1. Delete the session cookie
		cookies.delete('access_token', { path: '/' });

		// 2. Redirect the user back to home or login
		throw redirect(303, '/login');
	}
};
