import { test, expect } from 'vitest'
import { load as loadConfig, actions as actionsConfig } from '../src/routes/(teacher)/teacher/config/edit/[id]/+page.server.ts'

test('load function in config', () => {
  expect(typeof loadConfig).toBe('function');
});

test('actions object in config', () => {
  expect(typeof actionsConfig.default).toBe('function');
});