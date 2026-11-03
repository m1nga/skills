#!/usr/bin/env python3
"""Evidence-bound, local-only gap recommendations and private session journal."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

RESERVE = 2
LIMITS = ['Eligibility assertions are supplied by the caller, not independently verified.',
          'No monitoring, permission inference, task execution, or canonical task updates.']


class GapError(Exception):
    pass


class JSONParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({'schema_version': 1, 'status': 'error', 'error': message}))
        self.exit(2)


def fail(message):
    raise GapError(message)


def read(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        fail('Cannot read valid JSON: ' + str(path))


def version(data):
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        fail('Unsupported or missing schema_version; expected 1')


def integer(value):
    return type(value) is int and value >= 0


def context(data):
    version(data)
    p, c = data.get('project'), data.get('current_work')
    if not isinstance(p, dict) or not all(isinstance(p.get(k), str) and p[k] for k in ('id', 'title')):
        fail('Invalid project')
    if not isinstance(c, dict) or not all(isinstance(c.get(k), str) and c[k] for k in ('title', 'return_to')) or c.get('agent_status') not in ('running', 'waiting_for_user', 'finished', 'unknown'):
        fail('Invalid current_work')


def source_reasons(root, candidate):
    if not isinstance(candidate, dict):
        return ['invalid_source']
    source = candidate.get('source')
    if not isinstance(source, dict) or not isinstance(source.get('path'), str) or not isinstance(source.get('sha256'), str):
        return ['invalid_source']
    rel = Path(source['path'])
    if rel.is_absolute() or '..' in rel.parts or '.breakinggap' in rel.parts or not rel.parts:
        return ['unsafe_source']
    path = root
    for part in rel.parts:
        path = path / part
        if path.is_symlink():
            return ['unsafe_source']
    try:
        path.resolve().relative_to(root)
        if not path.is_file():
            return ['missing_source']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    except (OSError, ValueError):
        return ['missing_or_unsafe_source']
    return [] if digest == source['sha256'] else ['stale_source']


def reasons(root, c, budget, intent='any'):
    if not isinstance(c, dict):
        return ['invalid_candidate']
    out = []
    for key in ('id', 'title', 'action', 'done_when', 'pause_after', 'resume_hint', 'project'):
        if not isinstance(c.get(key), str) or not c[key].strip():
            out.append('invalid_' + key)
    if c.get('kind') not in ('advance', 'resume', 'learn'):
        out.append('invalid_kind')
    if intent != 'any' and c.get('kind') != intent:
        out.append('intent_mismatch')
    for key, allowed in [('state', ('ready',)), ('owner', ('human', 'either')), ('authorized', (True,)), ('interruptible', (True,)), ('conflict_check', ('clear',))]:
        if (key in ('authorized', 'interruptible') and c.get(key) is not True) or c.get(key) not in allowed:
            out.append('ineligible_' + key)
    m = c.get('minutes')
    if not isinstance(m, dict) or not all(integer(m.get(k)) for k in ('setup', 'work', 'wrap')) or m.get('work', 0) <= 0:
        out.append('invalid_minutes')
    elif sum(m[k] for k in ('setup', 'work', 'wrap')) > budget - RESERVE:
        out.append('over_budget')
    out.extend(source_reasons(root, c))
    return out


def recommend(root, data, minutes, intent):
    context(data)
    if not integer(minutes):
        fail('Minutes must be a nonnegative integer')
    candidates = data.get('candidates')
    if not isinstance(candidates, list):
        fail('candidates must be an array')
    ids = [c.get('id') for c in candidates if isinstance(c, dict)]
    if any(isinstance(x, str) and ids.count(x) > 1 for x in ids):
        fail('Duplicate candidate IDs')
    excluded, eligible = [], []
    for c in candidates:
        why = reasons(root, c, minutes, intent)
        if why:
            excluded.append({'id': c.get('id') if isinstance(c, dict) else None, 'reasons': why})
        else:
            eligible.append(c)
    status = {'waiting_for_user': 'needs_attention', 'finished': 'ready_to_review'}.get(data['current_work']['agent_status'])
    chosen = None
    if not status:
        eligible.sort(key=lambda c: (c['project'] != data['project']['id'], sum(c['minutes'][k] for k in ('setup', 'work', 'wrap')), c['id']))
        chosen = eligible[0] if eligible else None
        status = 'suggested' if chosen else 'no_match'
    return dict(schema_version=1, status=status, project=data['project'], current_work=data['current_work'], budget_minutes=minutes, return_reserve_minutes=RESERVE, chosen=chosen, excluded=excluded, limitations=LIMITS)


def atomic(path, data, exclusive=False):
    if path.is_symlink():
        fail('Refusing symlink output')
    temp = path.with_name('.' + path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        fd = os.open(str(temp), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        if exclusive:
            # Atomic no-overwrite publication; works on local macOS/Linux/Windows.
            os.link(temp, path)
        else:
            os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def storage(root):
    folder = root / '.breakinggap'
    if folder.is_symlink():
        fail('Unsafe session directory')
    folder.mkdir(mode=0o700, exist_ok=True)
    if not folder.is_dir():
        fail('Invalid session directory')
    if os.name != 'nt':
        folder.chmod(0o700)
    return folder


def journal(path):
    if path.is_symlink():
        fail('Unsafe session file')
    if not path.exists():
        return None
    data = read(path)
    version(data)
    if not isinstance(data.get('history'), list) or not isinstance(data.get('session'), dict):
        fail('Invalid session journal; preserved unchanged')
    for s in [data['session']] + data['history']:
        if not isinstance(s, dict) or s.get('state') not in ('active', 'paused', 'done') or not isinstance(s.get('notes'), list) or not isinstance(s.get('proposal'), dict):
            fail('Invalid session journal; preserved unchanged')
        if s is not data['session'] and s['state'] != 'done':
            fail('Invalid historical session; preserved unchanged')
        try:
            uuid.UUID(s.get('id', ''))
            for key in ('created_at', 'updated_at'):
                datetime.datetime.fromisoformat(s[key])
        except (ValueError, TypeError, KeyError, AttributeError):
            fail('Invalid session identity/timestamps; preserved unchanged')
        p = s['proposal']
        context(p)
        budget = p.get('budget_minutes')
        if p.get('status') != 'suggested' or not integer(budget) or p.get('return_reserve_minutes') != RESERVE or p['current_work']['agent_status'] not in ('running', 'unknown'):
            fail('Invalid stored proposal; preserved unchanged')
        why = reasons(path.parent.parent, p.get('chosen'), budget)
        if any(r not in ('stale_source', 'missing_source', 'missing_or_unsafe_source') for r in why):
            fail('Invalid stored candidate; preserved unchanged')
        for note in s['notes']:
            if not isinstance(note, dict) or note.get('state') not in ('paused', 'done') or not all(isinstance(note.get(k), str) for k in ('note', 'next', 'recorded_at')):
                fail('Invalid saved notes; preserved unchanged')
            try:
                datetime.datetime.fromisoformat(note['recorded_at'])
            except ValueError:
                fail('Invalid note timestamp; preserved unchanged')
        if (s['state'] == 'active' and s['notes']) or (s['state'] != 'active' and (not s['notes'] or s['notes'][-1]['state'] != s['state'])):
            fail('Inconsistent saved state; preserved unchanged')
    return data


def locked(root, operation):
    folder = storage(root)
    lock = folder / 'session.lock'
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        fail('Session busy: session.lock exists. Verify no writer is running before manually removing the lock; unknown locks are never removed automatically.')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(str(os.getpid()))
        return operation(folder / 'session.json')
    finally:
        lock.unlink()


def start(root, proposal):
    context(proposal)
    if proposal.get('status') != 'suggested' or proposal['current_work']['agent_status'] not in ('running', 'unknown'):
        fail('Proposal does not authorize a side session')
    budget = proposal.get('budget_minutes')
    if not integer(budget) or proposal.get('return_reserve_minutes') != RESERVE:
        fail('Invalid proposal budget')
    why = reasons(root, proposal.get('chosen'), budget)
    if why:
        fail('Proposal no longer eligible: ' + ', '.join(why))
    def op(path):
        data = journal(path)
        if data and data['session']['state'] in ('active', 'paused'):
            if data['session']['proposal'] == proposal:
                return data['session']
            fail('Another session is active or paused; checkpoint it done first')
        history = [] if data is None else data['history'] + [data['session']]
        session = dict(id=str(uuid.uuid4()), state='active', created_at=now(), updated_at=now(), proposal=proposal, notes=[])
        atomic(path, dict(schema_version=1, session=session, history=history))
        return session
    return locked(root, op)


def checkpoint(root, state, note, next_step):
    def op(path):
        data = journal(path)
        if data is None:
            fail('No saved session')
        s = data['session']
        payload = dict(state=state, note=note, next=next_step)
        if s['notes'] and all(s['notes'][-1].get(k) == v for k, v in payload.items()):
            return s
        if s['state'] == 'done':
            fail('Session already done; preserved unchanged')
        s['notes'].append(dict(payload, recorded_at=now()))
        s['state'], s['updated_at'] = state, now()
        atomic(path, data)
        return s
    return locked(root, op)


def resume(root):
    def op(path):
        data = journal(path)
        if data is None:
            fail('No saved session')
        s = data['session']
        return dict(schema_version=1, session=s, warnings=source_reasons(root, s['proposal'].get('chosen', {})), limitations=LIMITS)
    return locked(root, op)


def main():
    parser = JSONParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('recommend', 'start', 'checkpoint', 'resume'):
        p = sub.add_parser(name)
        p.add_argument('--root', required=True)
        if name == 'recommend':
            p.add_argument('--input', required=True)
            p.add_argument('--minutes', required=True, type=int)
            p.add_argument('--intent', choices=['any', 'advance', 'resume', 'learn'], default='any')
            p.add_argument('--out')
        elif name == 'start':
            p.add_argument('--proposal', required=True)
        elif name == 'checkpoint':
            p.add_argument('--state', required=True, choices=['paused', 'done'])
            p.add_argument('--note', required=True)
            p.add_argument('--next', required=True)
    args = parser.parse_args()
    try:
        root = Path(args.root).expanduser().resolve(strict=True)
        if not root.is_dir():
            fail('Root must be an existing directory')
        if args.command == 'recommend':
            result = recommend(root, read(args.input), args.minutes, args.intent)
            if args.out:
                output = Path(args.out).absolute()
                if '.breakinggap' in output.parts:
                    fail('Recommendation output cannot use session storage')
                atomic(output, result, exclusive=True)
        elif args.command == 'start':
            result = start(root, read(args.proposal))
        elif args.command == 'checkpoint':
            result = checkpoint(root, args.state, args.note, args.next)
        else:
            result = resume(root)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (GapError, OSError, ValueError) as exc:
        print(json.dumps({'schema_version': 1, 'status': 'error', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
