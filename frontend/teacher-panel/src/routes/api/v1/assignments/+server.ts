import { json } from '@sveltejs/kit'
import { db } from '$lib'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

export async function GET({request}) {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
	const res = await db.query.assignment.findMany()
    console.log("kk")

	return json(res);
}