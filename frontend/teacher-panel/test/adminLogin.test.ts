import { test, expect } from 'vitest'
import { load as loadLogin } from '../src/routes/(admin)/admin/+layout.ts'

test('load function in login', () => {
  expect(typeof loadLogin).toBe('function');
});