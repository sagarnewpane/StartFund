export async function POST({ cookies }) {
	// clear access token cookie
	cookies.delete('access_token', { path: '/' });

	return new Response(JSON.stringify({ success: true }));
}
