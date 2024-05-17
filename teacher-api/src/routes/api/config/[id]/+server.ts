import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'

export async function GET({params}) {
    const configId = parseInt(params.id)
	const res = await db.query.assignmentConfig.findFirst({ where: eq(schema.teacher.id, configId)})

	return json(res);
}