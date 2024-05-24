// place files you want to import through the `$lib` alias in this folder.
import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from '$lib/db/schema'
import {PRIVATE_DB_POSTGRES_PASSWORD, PRIVATE_DB_POSTGRES_USER} from '$env/static/private'
import {PUBLIC_POSTGRES_DB} from '$env/static/public'


import postgres from 'postgres';

const queryClient = postgres(`postgres://${PRIVATE_DB_POSTGRES_USER}:${PRIVATE_DB_POSTGRES_PASSWORD}@postgres-application:5432/${PUBLIC_POSTGRES_DB}`)

export const db = drizzle(queryClient, {schema: {...schema}});
