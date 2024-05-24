// test/listSingleStudentSubmission.test.ts
import { test, expect } from 'vitest'
import { load as loadList } from '../src/routes/(teacher)/teacher/submission/[id]/[student]/+page.server.ts'

test('load function in listSingleStudentSubmission', () => {
  expect(typeof loadList).toBe('function');
});