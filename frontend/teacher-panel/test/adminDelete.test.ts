import { test, expect } from 'vitest'
import { load as loadDelete, actions as actionsDelete } from '../src/routes/(admin)/admin/delete/+page.server.ts'

test('load function in delete', () => {
  expect(typeof loadDelete).toBe('function');
});

test('actions object in delete', () => {
  expect(typeof actionsDelete.default).toBe('function');
});