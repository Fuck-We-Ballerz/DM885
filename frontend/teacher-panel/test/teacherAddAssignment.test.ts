import { test, expect } from 'vitest'
import { load as loadAdd} from '../src/routes/(teacher)/teacher/assignment/add/+page.server.ts'
import { load as loadId, actions as actionsId } from '../src/routes/(teacher)/teacher/assignment/add/[id]/+page.server.ts'

test('load function in add', () => {
  expect(typeof loadAdd).toBe('function');
});

test('load function in id', () => {
  expect(typeof loadId).toBe('function');
});

test('actions object in id', () => {
  expect(typeof actionsId.default).toBe('function');
});