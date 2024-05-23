import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

export async function GET({params,request}) {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
    const configId = parseInt(params.id)
	const res = await db.query.assignmentConfig.findFirst({ where: eq(schema.teacher.id, configId)})

	return json(res);
}