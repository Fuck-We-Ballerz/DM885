import { drizzle } from 'drizzle-orm/postgres-js'
import * as schema from '$lib/db/schema'
import type { Actions } from './$types'
import type { PageServerLoad } from './$types'
import postgres from 'postgres'
import { eq } from 'drizzle-orm'
import { PUBLIC_KEYCLOAK_POST_URL } from '$env/static/public';


const queryClient = postgres('postgres://admin:admin@postgres_application:5432/testdb') //Docker
// const queryClient = postgres('postgres://admin:admin@localhost:5432/testdb')
const db = drizzle(queryClient, {schema: {...schema}});

export async function load({params}) {
        const teachers = await db.query.teacher.findMany() ?? []
        const students = await db.query.student.findMany() ?? []

        // console.log(teachers[0].name)

        let teachersOutput = teachers.map((teacher) => {
            return {
                name: teacher.name,
                id: teacher.id,
                username: teacher.username
            }
        })

        let studentOutput = students.map((student) => {
            return {
                name: student.name,
                id: student.id,
                username: student.username
            }
        })

        return {
            teachers: teachersOutput,
            students: studentOutput
        }
}


export const actions = {
    default: async ({cookies, request}) => {
        const token = cookies.get('kc-cookie');
        console.log(token)
        
        const data = await request.formData();
        console.log(data)


        for (const entry of data.entries()) {  //entries [username, "on"] indicating user to delete
            const username = entry[0].toString();

            const resTeacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, username)})
            const resStudent = await db.query.student.findFirst({ where: eq(schema.student.username, username)})

            if(resTeacher){
                const teacherIdDb = resTeacher.id         
                
                console.log(`${ PUBLIC_KEYCLOAK_POST_URL}`)
                console.log(`${ PUBLIC_KEYCLOAK_POST_URL }?username=${username}`)
                console.log(`fetch user from keycloak`)
                // const response = await fetch(`http://localhost:3200/admin/realms/DM885/users?username=${username}`, { //local
                const response = await fetch(`${ PUBLIC_KEYCLOAK_POST_URL }?username=${username}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                console.log(response.status)

                if(response.status === 200){
                    const responJ = await response.json();
                    console.log(JSON.stringify(responJ))
                    const userId = responJ[0].id;
                    
                    console.log(`Deleting user from keycloak`)
                    // const responseDelete = await fetch(`http://localhost:3200/admin/realms/DM885/users/${userId}`, { //local
                    const responseDelete = await fetch(`${ PUBLIC_KEYCLOAK_POST_URL }/${userId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    });

                    if(responseDelete.status === 204){
                        console.log(`Deleted ${username} from keycloak`);

                        console.log(`Deleting ${username} from teacher db table`)
                        await db.delete(schema.teacher)
                                .where(eq(schema.teacher.id, teacherIdDb))
                        
                        console.log(`Deleting from teacher_to_assignment db table`)
                        await db.delete(schema.teacherToAssignment)
                                .where(eq(schema.teacherToAssignment.teacher_id, teacherIdDb))
        
                        console.log(`Deleting from teacher_to_course db table`)
                        await db.delete(schema.teacher_to_course)
                                .where(eq(schema.teacher_to_course.teacher_id, teacherIdDb))  
                    } else{
                        console.log(`Failed to delete ${username} from keycloak`);
                    }
                } else{
                    console.log(`Failed to get ${username} from keycloak`);
                    console.log(response.status)
                }
            } else if(resStudent){
                const studentIdDb = resStudent.id

                console.log(`Deleting ${username} from student db table`)
                await db.delete(schema.student)
                        .where(eq(schema.student.id, studentIdDb))
                
                console.log("Deleting student from student_to_assignment db table")
                await db.delete(schema.studentToAssignment)
                        .where(eq(schema.studentToAssignment.student_id, studentIdDb))

                console.log("Deleting student from student_to_course db table")
                await db.delete(schema.student_to_course)
                        .where(eq(schema.student_to_course.student_id, studentIdDb))
                
                console.log("Deleting student from submission db table")
                await db.delete(schema.submission)
                        .where(eq(schema.submission.student_id, studentIdDb))

            }
        }
    }
} as Actions;