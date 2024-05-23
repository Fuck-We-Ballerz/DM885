import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'

/**
 * Pauses or unpauses an assignment.
 */
export const POST = async ({params, request}) => {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
    const teacherId = parseInt(params.id);
    const data = await request.json();
    if (!data.is_visible) {
        return new Response(JSON.stringify({
            message: "Missing boolean is_visible"
        }), { status: 400 });
    }
    const [new_state] = await db.update(schema.assignment)
                            .set({is_visible: data.is_visible})
                            .where(eq(schema.assignment.id, data.assignment_id))
                            .returning({is_visible: schema.assignment.is_visible});
    

    return new Response(JSON.stringify({
        message: "Success", 
        is_visible: new_state.is_visible
    }), { status: 201 } );
}
