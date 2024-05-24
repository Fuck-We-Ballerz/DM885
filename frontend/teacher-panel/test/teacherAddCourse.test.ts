import { test, expect } from 'vitest'
import { load as loadAdd, actions as actionsAdd } from '../src/routes/(teacher)/teacher/course/add/+page.server.ts'

test('load function in add', () => {
  expect(typeof loadAdd).toBe('function');
});

test('actions object in add', () => {
  expect(typeof actionsAdd.default).toBe('function');
});