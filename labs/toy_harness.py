# -*- coding: utf-8 -*-
"""Deterministic teaching runtime. No model, network, file writes or subprocesses.

This task-specific validator is not a production sandbox or authorization library.
The timeout is an injected observation, not a real timed execution mechanism.
"""
import argparse
import json

FIXTURE = (40, 60)
SCENARIOS = ('success', 'wrong', 'denied', 'timeout', 'loop')


def plan(scenario):
    read = {'kind': 'tool', 'name': 'read_invoices', 'args': {'tenant': 'A'}}
    if scenario == 'denied':
        return [{'kind': 'tool', 'name': 'read_invoices', 'args': {'tenant': 'B'}}]
    if scenario == 'loop':
        return [read.copy() for _ in range(8)]
    return [read,
            {'kind': 'tool', 'name': 'sum_values', 'args': {'values': list(FIXTURE)}},
            {'kind': 'final', 'value': 99 if scenario == 'wrong' else 100}]


def run(scenario='success', max_steps=4, proposals=None):
    if scenario not in SCENARIOS:
        raise ValueError('unknown scenario')
    if type(max_steps) is not int or not 1 <= max_steps <= 8:
        raise ValueError('max_steps must be an integer from 1 to 8')
    script = plan(scenario) if proposals is None else proposals
    events, observed, computed = [], None, None

    def event(phase, detail):
        events.append({'step': step, 'phase': phase, 'detail': detail})

    def stop(state, detail):
        event('STOP', detail)
        return {'state': state, 'events': events}

    for index, proposal in enumerate(script):
        step = index + 1
        if step > max_steps:
            step = max_steps
            return stop('step_budget', 'No new proposal or tool executed after the limit')
        event('PROPOSE', proposal)
        if not isinstance(proposal, dict):
            return stop('schema_error', 'Proposal must be an object')
        if proposal.get('kind') == 'final':
            if set(proposal) != {'kind', 'value'} or type(proposal['value']) is not int:
                return stop('schema_error', 'Final must contain one integer value')
            event('VERIFY', {'candidate': proposal['value'], 'computed': computed})
            if computed is not None and proposal['value'] == computed == 100:
                return stop('completed', 'Verified final with observed computation evidence')
            return stop('verification_failed', 'Final lacks matching computation evidence')
        if set(proposal) != {'kind', 'name', 'args'} or proposal.get('kind') != 'tool':
            return stop('schema_error', 'Tool proposal fields do not match the schema')
        name, args = proposal['name'], proposal['args']
        if not isinstance(args, dict):
            return stop('schema_error', 'Arguments must be an object')
        if name == 'read_invoices':
            if set(args) != {'tenant'} or type(args['tenant']) is not str:
                return stop('schema_error', 'Read requires exactly one string tenant')
            event('VALIDATE', 'Read schema accepted')
            if args['tenant'] != 'A':
                event('AUTHORIZE', 'DENY: task capability permits tenant A only')
                return stop('policy_denied', 'No tool execution and no foreign data returned')
            event('AUTHORIZE', 'ALLOW: tenant A read')
            event('EXECUTE', 'read_invoices')
            if scenario == 'timeout':
                event('OBSERVE', {'error': 'simulated_timeout'})
                return stop('tool_timeout', 'No result; no automatic retry in this teaching runtime')
            observed = list(FIXTURE)
            event('OBSERVE', {'values': observed})
        elif name == 'sum_values':
            values = args.get('values')
            if set(args) != {'values'} or not isinstance(values, list) or not values or any(type(v) is not int for v in values):
                return stop('schema_error', 'Sum requires a nonempty integer list')
            event('VALIDATE', 'Sum schema accepted')
            if observed is None or values != observed:
                event('AUTHORIZE', 'DENY: values do not match the observed fixture')
                return stop('policy_denied', 'No ungrounded computation')
            event('AUTHORIZE', 'ALLOW: computation over observed fixture')
            event('EXECUTE', 'sum_values')
            computed = sum(values)
            event('OBSERVE', {'total': computed})
        else:
            return stop('schema_error', 'Unknown tool name')
    step = len(script)
    return stop('planner_exhausted', 'Planner stopped without a verified final')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario', choices=SCENARIOS, nargs='?', default='success')
    parser.add_argument('--max-steps', type=int, default=4)
    options = parser.parse_args()
    result = run(options.scenario, options.max_steps)
    for item in result['events']:
        print(json.dumps(item, ensure_ascii=False))
    print(json.dumps({'state': result['state']}, ensure_ascii=False))
