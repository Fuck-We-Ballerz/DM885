import { db} from '$lib';
import * as schema from '$lib/db/schema'
import type { Actions } from './$types';
import { PUBLIC_KEYCLOAK_POST_URL } from '$env/static/public'


export const actions = {
    default: async ({cookies, request}) => {
        const token = cookies.get('kc-cookie');
        const data = await request.formData();

        console.log(token);

        const teacher = {
            username: data.get('username'),
            firstName: data.get('firstName'),
            lastName: data.get('lastName'),
            enabled: "true",
            credentials: [
                {
                    type: "password",
                    value: "pass",  //initial temporary password
                    temporary: true
                }
            ],
            groups: ["teacher-group"]
        };

        const response = await fetch(`${ PUBLIC_KEYCLOAK_POST_URL }`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(teacher)
        });

        console.log(response.status);

        if (response.status === 201) {
            console.log('User created successfully');
            console.log("Inserting into postgress database");

            if (typeof teacher.firstName !== 'string' || typeof teacher.lastName !== 'string' || typeof teacher.username !== 'string') {
                console.log('Invalid teacher object');
            } else{
                console.log("insert into db")
                if(teacher.groups[0] === 'teacher-group'){
                    console.log("insert into teacher db")
                    await db.insert(schema.teacher).values({
                        name: teacher.firstName + " " + teacher.lastName,
                        username: teacher.username,
                    })
                }
                if(teacher.groups[0] === 'admin-group'){
                    await db.insert(schema.admin).values({
                        name: teacher.firstName + " " + teacher.lastName,
                        username: teacher.username,
                    })
                }
            }
        } else { 
            console.log('Failed to create user');
        }
    } 
} as Actions;