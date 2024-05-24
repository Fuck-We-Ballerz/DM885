import { test, expect } from 'vitest'
import { load as loadDelete} from '../src/routes/(teacher)/teacher/assignment/delete/+page.server.ts'
import { load as loadId, actions as actionsId } from '../src/routes/(teacher)/teacher/assignment/delete/[id]/+page.server.ts'

test('load function in delete', () => {
  expect(typeof loadDelete).toBe('function');
});

test('load function in id', () => {
  expect(typeof loadId).toBe('function');
});

test('actions object in id', () => {
  expect(typeof actionsId.default).toBe('function');
});