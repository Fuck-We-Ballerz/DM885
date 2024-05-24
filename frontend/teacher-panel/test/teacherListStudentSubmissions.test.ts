import { test, expect } from 'vitest'
import { load as loadList } from '../src/routes/(teacher)/teacher/submission/[id]/+page.server.ts'

test('load function in listStudentSubmissions', () => {
  expect(typeof loadList).toBe('function');
});