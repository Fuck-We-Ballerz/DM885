import { boolean, interval, foreignKey, integer, pgTable, primaryKey, serial, text, timestamp, unique, varchar } from 'drizzle-orm/pg-core';

export const assignmentConfig = pgTable('assignment_config', {
  id: serial('id').primaryKey(),
//   name: varchar('name', {length: 64}).notNull(),   //Postgress db does not support name yet
  max_ram: integer('max_ram').notNull(),
  max_cpu: integer('max_cpu').notNull(),
  max_time: interval('max_time').notNull(),
  max_submission: integer('max_submission').notNull(),
});

export const assignment = pgTable('assignment', {
  id: serial('id').primaryKey(),
  title: varchar('title', {length: 64}).notNull(),
  start_date: timestamp('start_date', { mode: 'string' }).notNull().defaultNow(),
  end_date: timestamp('end_date', { mode: 'string' }).notNull().defaultNow(),
  is_visible: boolean('is_visible').notNull(),
  docker_image: varchar('docker_image', {length: 64}),
  course_id: integer('course_id').notNull().references(() => course.id),
  config_id: integer('config_id').notNull().references(() => assignmentConfig.id),
});

// Convert the below tables to match the two above tables
export const student = pgTable('student', {
    id: serial('id').primaryKey(),
    name: varchar('name', {length: 64}).notNull(),
    password: varchar('password', {length: 64}).notNull(),
    username: varchar('username', {length: 64}).notNull().unique(),
    open_assignment_count: integer('open_assignment_count').default(0).notNull(),
});

export const teacher = pgTable('teacher', {
    id: serial('id').primaryKey(),
    name: varchar('name', {length: 64}).notNull(),
    password: varchar('password', {length: 64}).notNull(),
    username: varchar('username', {length: 64}).notNull(),
    is_paused: boolean('is_paused').default(false).notNull(),
});

export const admin = pgTable('admin', {
    id: serial('id').primaryKey(),
    name: varchar('name', {length: 64}).notNull(),
    password: varchar('password', {length: 64}).notNull(),
    username: varchar('username', {length: 64}).notNull(),
});

export const submission = pgTable('submission', {
    id: serial('id').primaryKey(),
    grade: varchar('grade', {length: 64}).default('Not graded').notNull(),
    status: varchar('status', {length: 64}).default('Pending').notNull(),
    submission: varchar('submission', {length: 64}),
    submission_std: varchar('submission_std', {length: 64}).default('').notNull(),
    submission_err: varchar('submission_err', {length: 64}).default('').notNull(),
    submission_time: timestamp('submission_time').notNull(),
    assignment_id: integer('assignment_id').notNull().references(() => assignment.id),
    student_id: integer('student_id').notNull().references(() => student.id),
});

export const course = pgTable('course', {
    id: serial('id').primaryKey(),
    name: text('name')
});

export const student_to_course = pgTable('student_to_course', {
    id: serial('id').primaryKey(),
    student_id: integer('student_id').notNull().references(() => student.id),
    course_id: integer('course_id').notNull().references(() => course.id),
})

export const teacher_to_course = pgTable('teacher_to_course', {
    id: serial('id').primaryKey(),
    teacher_id: integer('teacher_id').notNull().references(() => teacher.id),
    course_id: integer('course_id').notNull().references(() => course.id),
})

export const student_to_assignment = pgTable('student_to_assignment', {
    assignment_id: integer('assignment_id').primaryKey().references(() => assignment.id),
    student_id: integer('student_id').primaryKey().references(() => student.id),
});

export const teacher_to_assignment = pgTable('teacher_to_assignment', {
    assignment_id: integer('assignment_id').primaryKey().references(() => assignment.id),
    teacher_id: integer('teacher_id').primaryKey().references(() => teacher.id),
});