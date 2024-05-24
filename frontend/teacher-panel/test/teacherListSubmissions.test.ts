import { test, expect } from 'vitest'
import { load as loadList } from '../src/routes/(teacher)/teacher/submission/+page.server.ts'

test('load function in list', () => {
  expect(typeof loadList).toBe('function');
});