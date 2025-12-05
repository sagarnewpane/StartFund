export async function POST({ request, cookies }) {
	const { email, password } = await request.json();

	// call your backend login here
	const response = await fetch('http://localhost:8000/api/login', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, password })
	});

	const data = await response.json();

	// set access token cookie
	cookies.set('access_token', data.access_token, {
		path: '/',
		httpOnly: false, // you want to read it on client, so keep false
		sameSite: 'strict',
		secure: false, // set true in production
		maxAge: 60 * 60 // 1 hour
	});

	return new Response(JSON.stringify({ success: true }));
}
