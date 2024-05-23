import { json } from '@sveltejs/kit'
import { db } from '$lib'
import { login } from '$lib/api/login.js';

export const GET = async ({request}) => {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
	const res = await db.query.teacher.findMany()

	return json(res);
}