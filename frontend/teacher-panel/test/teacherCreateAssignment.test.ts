import { test, expect, vi } from 'vitest'
import { actions } from '../src/routes/(teacher)/teacher/assignment/create/+page.server.ts'

test('actions object', () => {
  expect(typeof actions.newConfig).toBe('function');
  expect(typeof actions.newAssignment).toBe('function');
  expect(typeof actions.deleteConfig).toBe('function');
});