import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'

export async function GET({params}) {
    const assignmentId = parseInt(params.id)
	const res = await db.query.assignment.findFirst({ where: eq(schema.assignment.id, assignmentId)})

	return json(res);
}