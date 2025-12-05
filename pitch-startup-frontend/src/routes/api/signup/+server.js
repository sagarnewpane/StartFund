export async function POST({ request, cookies }) {
	const { email, password, fullName } = await request.json();

	// call your backend login here
	const response = await fetch('http://localhost:8000/api/signup', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, password, fullName })
	});

	const data = await response.json();

	return new Response(JSON.stringify(data));
}
