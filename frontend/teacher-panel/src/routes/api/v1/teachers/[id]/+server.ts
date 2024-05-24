import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

export async function GET({params, request}) {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
    const teacherId = parseInt(params.id)
	const res = await db.query.teacher.findFirst({ where: eq(schema.teacher.id, teacherId)})

    return new Response(JSON.stringify({
        message: "Success",
        teacher: res
    }), { status: 200 });
}