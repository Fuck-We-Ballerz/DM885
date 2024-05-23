import { json } from '@sveltejs/kit'
import { db } from '$lib'
import * as schema from '$lib/db/schema'

export async function GET({request}) {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
	const res = await db.query.course.findMany()

	return json(res);
}