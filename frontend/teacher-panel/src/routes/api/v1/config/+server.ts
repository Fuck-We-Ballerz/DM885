import { json } from '@sveltejs/kit'
import { db } from '$lib'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

export async function GET({request}) {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
	const res = await db.query.assignmentConfig.findMany()

	return json(res);
}