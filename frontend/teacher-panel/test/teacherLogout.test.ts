import { test, expect } from 'vitest'
import { load as loadLogout } from '../src/routes/(teacher)/teacher/logout/+page.ts'

test('load function in logout', () => {
  expect(typeof loadLogout).toBe('function');
});