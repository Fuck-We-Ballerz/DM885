import { json } from '@sveltejs/kit'
import { db } from '$lib'
import * as schema from '$lib/db/schema'

export async function GET() {
	const res = await db.query.assignment.findMany()
    console.log("kk")

	return json(res);
}