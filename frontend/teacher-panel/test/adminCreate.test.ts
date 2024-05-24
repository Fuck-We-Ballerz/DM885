import { test, expect } from 'vitest'
import { actions as actionsCreate } from '../src/routes/(admin)/admin/create/+page.server.ts'

test('actions object in create', () => {
  expect(typeof actionsCreate.default).toBe('function');
});