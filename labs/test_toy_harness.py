# -*- coding: utf-8 -*-
"""Check the teaching runtime's externally observable contracts."""
import unittest
from toy_harness import run


class RuntimeContractTests(unittest.TestCase):
    def test_success_requires_observed_computation(self):
        result = run('success')
        self.assertEqual(result['state'], 'completed')
        final_only = run(proposals=[{'kind': 'final', 'value': 100}])
        self.assertEqual(final_only['state'], 'verification_failed')

    def test_denied_read_never_executes_or_returns_data(self):
        result = run('denied')
        self.assertEqual(result['state'], 'policy_denied')
        self.assertFalse(any(e['phase'] in ('EXECUTE', 'OBSERVE') for e in result['events']))

    def test_wrong_answer_is_not_completion(self):
        self.assertEqual(run('wrong')['state'], 'verification_failed')

    def test_timeout_stops_without_computation(self):
        result = run('timeout')
        self.assertEqual(result['state'], 'tool_timeout')
        executions = [e['detail'] for e in result['events'] if e['phase'] == 'EXECUTE']
        self.assertEqual(executions, ['read_invoices'])

    def test_budget_stops_before_an_extra_proposal(self):
        result = run('success', 2)
        self.assertEqual(result['state'], 'step_budget')
        self.assertEqual(sum(e['phase'] == 'PROPOSE' for e in result['events']), 2)
        self.assertFalse(any(e['phase'] == 'VERIFY' for e in result['events']))
        self.assertEqual(run('loop', 4)['state'], 'step_budget')

    def test_rejects_malformed_and_unknown_tools_before_execution(self):
        examples = [None, {'kind': 'tool', 'name': 'shell', 'args': {}},
                    {'kind': 'tool', 'name': 'read_invoices', 'args': {'tenant': 'A', 'extra': 1}},
                    {'kind': 'final', 'value': True}]
        for proposal in examples:
            with self.subTest(proposal=proposal):
                result = run(proposals=[proposal])
                self.assertEqual(result['state'], 'schema_error')
                self.assertFalse(any(e['phase'] == 'EXECUTE' for e in result['events']))

    def test_cannot_sum_unobserved_or_modified_values(self):
        call = {'kind': 'tool', 'name': 'sum_values', 'args': {'values': [100]}}
        self.assertEqual(run(proposals=[call])['state'], 'policy_denied')
        read = {'kind': 'tool', 'name': 'read_invoices', 'args': {'tenant': 'A'}}
        self.assertEqual(run(proposals=[read, call])['state'], 'policy_denied')

    def test_invalid_budget_and_exhausted_planner(self):
        for limit in (0, 9, True):
            with self.assertRaises(ValueError):
                run(max_steps=limit)
        self.assertEqual(run(proposals=[])['state'], 'planner_exhausted')


if __name__ == '__main__':
    unittest.main()
