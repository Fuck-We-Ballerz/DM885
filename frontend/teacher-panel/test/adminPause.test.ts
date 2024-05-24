import { test, expect } from 'vitest'
import { load as loadPause, actions as actionsPause } from '../src/routes/(admin)/admin/pause/+page.server.ts'

test('load function in pause', () => {
  expect(typeof loadPause).toBe('function');
});

test('actions object in pause', () => {
  expect(typeof actionsPause.default).toBe('function');
});