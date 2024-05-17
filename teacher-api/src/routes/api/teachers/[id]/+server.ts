import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'

export async function GET({params}) {
    const teacherId = parseInt(params.id)
	const res = await db.query.teacher.findFirst({ where: eq(schema.teacher.id, teacherId)})

	return json(res);
}