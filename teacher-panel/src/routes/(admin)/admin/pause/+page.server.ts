import { drizzle } from 'drizzle-orm/postgres-js'
import * as schema from '$lib/db/schema'
import type { Actions } from './$types'
import type { PageServerLoad } from './$types'
import postgres from 'postgres'
import { eq } from 'drizzle-orm'

// const queryClient = postgres('postgres://admin:admin@postgres_application:5432/testdb') //Docker
const queryClient = postgres('postgres://admin:admin@localhost:5432/testdb')
const db = drizzle(queryClient, {schema: {...schema}});

export async function load({params}) {
        const teachers = await db.query.teacher.findMany() ?? []

        // console.log(teachers[0].name)

        let output = teachers.map((teacher) => {
            return {
                name: teacher.name,
                username: teacher.username,
                isPaused: teacher.is_paused
            }
        })
        // console.log(output)
        return {
            teachers: output
        }
}


export const actions = {
    default: async ({cookies, request}) => {
        const data = await request.formData();
        console.log(data)
        for (const entry of data.entries()) {  //entries [username, value]
        console.log(`inserting ${entry[0]} into teacher`)
        
        await db.update(schema.teacher)
                .set({is_paused: entry[1] === 'on' ? true : false})
                .where(eq(schema.teacher.username, entry[0].toString()))
        }
    }
} as Actions;