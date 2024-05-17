import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'

export async function GET({params}) {
    const courseId = parseInt(params.id)
	const res = await db.query.course.findFirst({ where: eq(schema.course.id, courseId)})

	return json(res);
}