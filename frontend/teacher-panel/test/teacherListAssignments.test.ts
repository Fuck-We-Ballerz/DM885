import { test, expect } from 'vitest'
import { load as loadList, actions as actionsList } from '../src/routes/(teacher)/teacher/assignment/list/+page.server.ts'

test('load function in list', () => {
  expect(typeof loadList).toBe('function');
});

test('actions object in list', () => {
  expect(typeof actionsList.updateAssignment).toBe('function');
  expect(typeof actionsList.deleteAssignment).toBe('function');
});