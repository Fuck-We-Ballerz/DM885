import { test, expect } from 'vitest'
import { load as loadLogin } from '../src/routes/(teacher)/teacher/+layout.ts'

test('load function in login', () => {
  expect(typeof loadLogin).toBe('function');
});