import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from '$lib/db/schema'
import type { PageServerLoad } from './$types';
import type { Actions } from './$types';

import postgres from 'postgres';

// const queryClient = postgres('postgres://admin:admin@postgres_application:5432/testdb') //Docker
const queryClient = postgres('postgres://admin:admin@localhost:5432/testdb')
const db = drizzle(queryClient, {schema: {...schema}});

export const actions = {
    default: async ({cookies, request}) => {
        const token = cookies.get('kc-cookie');
        const data = await request.formData();

        // console.log(token);

        const teacher = {
            username: data.get('username'),
            firstName: data.get('firstName'),
            lastName: data.get('lastName'),
            enabled: "true",
            credentials: [
                {
                    type: "password",
                    value: "pass",
                    temporary: true
                }
            ],
            // groups: ["teacher-group"]
            groups: ["admin-group"]
        };

        // const test = {
        //     email: "user@example.com",
        //     firstName: "John",
        //     lastName: "Doe",
        //     enabled: "true",
        //     username: "user",
        //     credentials: [
        //         {
        //             type: "password",
        //             value: "pass",
        //             temporary: true
        //         }
        //     ],
        //     // clientRoles: {
        //     //     "4f336bd8-d7b0-4e86-be7b-854df377bb1d": ["teacher"]
        //     // }
        //     groups: ["teacher-group"]  //<-- clientRoles not working for js keyclaok but assigning group and inheriting role does.
        // };

        console.log(JSON.stringify(teacher));

        // const response = await fetch('http://localhost:3200/admin/realms/DM885/users?username=admin', {
        //     method: 'GET',
        //     headers: {
        //         'Authorization': `Bearer ${token}`,
        //         'Content-Type': 'application/json'
        //     }
        // });
        // if(response.status === 200){
        //     const r = await response.json();
        //     console.log(r[0].id);
        //     console.log(JSON.stringify(r));
        // }

        const response = await fetch('http://localhost:3200/admin/realms/DM885/users', {
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
                throw new Error('Invalid teacher object');
            } else{
                if(teacher.groups[0] === 'teacher-group')
                    await db.insert(schema.teacher).values({
                        name: teacher.firstName + " " + teacher.lastName,
                        username: teacher.username,
                        password: "pass",
                        is_paused: false,
                    })
                if(teacher.groups[0] === 'admin-group')
                    await db.insert(schema.admin).values({
                        name: teacher.firstName + " " + teacher.lastName,
                        username: teacher.username,
                        password: "pass",
                    })
            }
        } else { 
            console.error('Failed to create user');
        }
    }
} as Actions;