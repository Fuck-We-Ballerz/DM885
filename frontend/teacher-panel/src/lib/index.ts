// place files you want to import through the `$lib` alias in this folder.
import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from '$lib/db/schema'

import postgres from 'postgres';

const queryClient = postgres('postgres://admin:admin@postgres_application:5432/testdb')

export const db = drizzle(queryClient, {schema: {...schema}});
