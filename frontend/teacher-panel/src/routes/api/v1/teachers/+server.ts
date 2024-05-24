import { json } from '@sveltejs/kit'
import { db } from '$lib'
import { login } from '$lib/api/login.js';

export const GET = async ({request}) => {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
	const res = await db.query.teacher.findMany()

	return new Response(JSON.stringify({
        message: "Success",
        teacher: res
    }), { status: 200 });
}