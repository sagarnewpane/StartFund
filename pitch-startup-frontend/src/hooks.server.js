export const handle = async ({ event, resolve }) => {
	const token = event.cookies.get('access_token');

	event.locals.user = token ? { token } : null;

	return resolve(event);
};
