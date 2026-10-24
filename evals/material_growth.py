"""Initial job-queue fixture for material-growth-handoff; not a registered case.

Only fixture bytes live here. Evaluation framework conventions and requirements
remain in META-EVALUATIONS.md; no prompts, grading, or review rubric are defined.
"""


FIXTURE_FILES = {
    "job_queue.py": b'''"""Job state and leases; canonical contract: docs/job-queue.md."""

from copy import deepcopy
from pathlib import Path
import time


LEASE_SECONDS = 30
MAX_ATTEMPTS = 3


class JobQueue:
    def __init__(self, database_path, clock=time.time):
        self.database_path = Path(database_path)
        self._clock = clock
        # The path is retained, but authoritative state is currently instance-local.
        self._jobs = {}

    def submit(self, job_id, payload):
        if job_id in self._jobs:
            raise ValueError("duplicate job ID")
        self._jobs[job_id] = {
            "payload": deepcopy(payload), "state": "pending", "attempts": 0,
            "worker_id": None, "expires_at": None,
        }

    def claim(self, worker_id):
        now = self._clock()
        for job_id, job in self._jobs.items():
            self._expire(job, now)
            if job["state"] != "pending":
                continue
            payload = deepcopy(job["payload"])
            job.update(state="leased", attempts=job["attempts"] + 1,
                       worker_id=worker_id, expires_at=now + LEASE_SECONDS)
            return {"job_id": job_id, "payload": payload,
                    "token": job["attempts"], "expires_at": job["expires_at"]}
        return None

    def ack(self, job_id, token):
        job = self._jobs.get(job_id)
        if not self._valid_lease(job, token):
            return False
        job.update(state="completed", worker_id=None, expires_at=None)
        return True

    def fail(self, job_id, token):
        job = self._jobs.get(job_id)
        if not self._valid_lease(job, token):
            return False
        job.update(state=self._retry_state(job), worker_id=None, expires_at=None)
        return True

    def status(self, job_id):
        job = self._jobs.get(job_id)
        if job is None:
            return None
        self._expire(job, self._clock())
        return {"state": job["state"], "attempts": job["attempts"]}

    def _valid_lease(self, job, token):
        return (job is not None and job["state"] == "leased"
                and type(token) is int and token == job["attempts"]
                and self._clock() < job["expires_at"])

    def _retry_state(self, job):
        return "pending" if job["attempts"] < MAX_ATTEMPTS else "exhausted"

    def _expire(self, job, now):
        if job["state"] == "leased" and now >= job["expires_at"]:
            job.update(state=self._retry_state(job), worker_id=None, expires_at=None)
''',
    "test_job_queue.py": b'''from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from job_queue import JobQueue


class JobQueueTests(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(TemporaryDirectory())
        self.now = 1000.0
        self.queue = JobQueue(Path(directory) / "jobs.sqlite3", clock=lambda: self.now)

    def test_submit_claim_and_ack_complete_a_job(self):
        self.assertIsNone(self.queue.submit("job", {"message": "hello"}))
        self.assertEqual(self.queue.status("job"), {"state": "pending", "attempts": 0})

        lease = self.queue.claim("worker")

        self.assertEqual(lease, {"job_id": "job", "payload": {"message": "hello"},
                                 "token": 1, "expires_at": 1030.0})
        self.assertEqual(self.queue.status("job"), {"state": "leased", "attempts": 1})
        self.assertIsNone(self.queue.claim("another-worker"))
        self.assertIs(self.queue.ack("job", lease["token"]), True)
        self.assertEqual(self.queue.status("job"), {"state": "completed", "attempts": 1})
        self.now = 2000.0
        self.assertIsNone(self.queue.claim("another-worker"))
        self.assertIs(self.queue.ack("job", lease["token"]), False)
        self.assertIs(self.queue.fail("job", lease["token"]), False)

    def test_failure_allows_immediate_retry_until_exhaustion(self):
        self.queue.submit("job", None)
        for attempt in (1, 2, 3):
            lease = self.queue.claim("worker")
            self.assertEqual(lease["token"], attempt)
            self.assertIs(self.queue.fail("job", lease["token"]), True)
            expected_state = "pending" if attempt < 3 else "exhausted"
            self.assertEqual(self.queue.status("job"),
                             {"state": expected_state, "attempts": attempt})
        self.assertIsNone(self.queue.claim("worker"))

    def test_expiry_at_deadline_allows_reclaim_and_fences_old_token(self):
        self.queue.submit("job", ["work"])
        old = self.queue.claim("crashed-worker")
        self.now = 1029.999
        self.assertIsNone(self.queue.claim("replacement"))

        self.now = old["expires_at"]
        self.assertIs(self.queue.ack("job", old["token"]), False)
        self.assertIs(self.queue.fail("job", old["token"]), False)
        self.assertEqual(self.queue.status("job"), {"state": "pending", "attempts": 1})
        new = self.queue.claim("replacement")

        self.assertEqual(new["token"], 2)
        self.assertEqual(new["expires_at"], 1060.0)
        self.assertIs(self.queue.ack("job", old["token"]), False)
        self.assertIs(self.queue.fail("job", old["token"]), False)
        self.assertEqual(self.queue.status("job"), {"state": "leased", "attempts": 2})
        self.assertIs(self.queue.ack("job", new["token"]), True)

    def test_expiration_of_final_attempt_is_terminal(self):
        self.queue.submit("job", "work")
        for attempt in (1, 2, 3):
            lease = self.queue.claim("worker")
            self.assertEqual(lease["token"], attempt)
            self.now = lease["expires_at"]
        self.assertIsNone(self.queue.claim("worker"))
        self.assertEqual(self.queue.status("job"), {"state": "exhausted", "attempts": 3})
        self.assertIs(self.queue.ack("job", 3), False)
        self.assertIs(self.queue.fail("job", 3), False)

    def test_duplicate_id_is_rejected_without_replacing_payload(self):
        self.queue.submit("job", "original")
        with self.assertRaises(ValueError):
            self.queue.submit("job", "replacement")
        lease = self.queue.claim("worker")
        self.assertEqual(lease["payload"], "original")
        self.queue.ack("job", lease["token"])
        with self.assertRaises(ValueError):
            self.queue.submit("job", "replacement")

    def test_empty_queue_unknown_ids_and_invalid_tokens(self):
        self.assertIsNone(self.queue.claim("worker"))
        self.assertIsNone(self.queue.status("missing"))
        self.assertIs(self.queue.ack("missing", 1), False)
        self.assertIs(self.queue.fail("missing", 1), False)
        self.queue.submit("job", {})
        self.assertIs(self.queue.ack("job", 1), False)
        self.assertIs(self.queue.fail("job", 1), False)
        lease = self.queue.claim("worker")
        for token in (None, "1", True, 1.0, 0, -1, 2):
            with self.subTest(token=token):
                self.assertIs(self.queue.ack("job", token), False)
                self.assertIs(self.queue.fail("job", token), False)
                self.assertEqual(self.queue.status("job"), {"state": "leased", "attempts": 1})
        self.assertIs(self.queue.ack("job", lease["token"]), True)

    def test_payloads_and_status_results_are_detached_snapshots(self):
        payload = {"items": [1, {"ready": True}]}
        self.queue.submit("job", payload)
        payload["items"].append(2)
        lease = self.queue.claim("worker")
        self.assertEqual(lease["payload"], {"items": [1, {"ready": True}]})
        lease["payload"]["items"][1]["ready"] = False
        self.queue.fail("job", lease["token"])
        snapshot = self.queue.status("job")
        snapshot["state"] = "completed"

        retry = self.queue.claim("worker")

        self.assertEqual(retry["payload"], {"items": [1, {"ready": True}]})
        self.assertEqual(retry["token"], 2)

    def test_job_ids_are_case_sensitive_and_jobs_complete_independently(self):
        self.queue.submit("Job", "upper")
        self.queue.submit("job", "lower")
        first = self.queue.claim("one")
        second = self.queue.claim("two")
        self.assertEqual({first["job_id"], second["job_id"]}, {"Job", "job"})
        self.assertIs(self.queue.ack(first["job_id"], first["token"]), True)
        self.assertEqual(self.queue.status(second["job_id"]), {"state": "leased", "attempts": 1})
        self.assertIs(self.queue.ack(second["job_id"], second["token"]), True)


if __name__ == "__main__":
    unittest.main()
''',
    "README.md": b'''# Background job queue

A small queue module that coordinates job state for background workers.
Use Python 3.11 or newer; only the standard library is needed.

```python
from job_queue import JobQueue

queue = JobQueue("jobs.sqlite3")
queue.submit("welcome-42", {"recipient": "customer-42"})
lease = queue.claim("worker-1")
if lease is not None:
    print(lease["payload"])
    queue.ack(lease["job_id"], lease["token"])
```

The [application contract](docs/job-queue.md) owns the supported API, required
reliability guarantees, accepted storage decision, and current implementation
gaps. The current module keeps state only in memory and loses jobs on reopening.

Run the existing sequential API tests from this directory:

```sh
python -B -m unittest -v
```

Those tests exercise one queue instance at a time; passing them does not
establish persistence, crash recovery, or concurrent worker safety.
''',
    "docs/job-queue.md": b'''# Job queue contract

This is the canonical application API and requirements document. Requirements
describe established obligations, including guarantees the current implementation
does not meet. The implementation assessment below describes present behavior.

## Supported API (required behavior)

`from job_queue import JobQueue` exposes `JobQueue(database_path, clock=time.time)`.
The path is a string or pathlib.Path naming a local file, with an existing parent
directory. An absent database is created on first use; an existing database is
reopened without resetting state. In-memory SQLite databases are unsupported.
The clock is a zero-argument callable returning finite Unix epoch seconds;
production defaults to time.time. Tests can control it without sleeping.
Clocks must be comparable across processes and restarts and must progress;
backward clock jumps are outside the recovery guarantee.

Job and worker IDs are nonempty, case-sensitive strings. A payload is a finite
JSON value: null/None, boolean, string, integer, finite float, list of JSON values,
or dictionary with string keys and JSON values. Other input shapes are outside
the supported interface, except invalid lease tokens as specified below.

| Operation | Supported result and behavior |
| --- | --- |
| `submit(job_id, payload)` | Returns None. Creates a pending job with zero attempts. Rejects any existing ID with ValueError, including IDs of completed or exhausted jobs, without modifying it. Exception wording is unspecified. |
| `claim(worker_id)` | Returns None if no job is eligible; otherwise returns a dictionary with exactly job_id, payload, token, and expires_at. Records the worker as lease owner. expires_at uses the injected clock's units. Selection order among eligible jobs is unspecified. |
| `ack(job_id, token)` | Returns True only when a valid current lease is completed; otherwise False. |
| `fail(job_id, token)` | Returns True only when a valid current lease is relinquished; otherwise False. |
| `status(job_id)` | Returns None for an unknown ID; otherwise a dictionary with exactly state and attempts, reflecting expiry at the observation time. |

States are pending, leased, completed, and exhausted. Only pending jobs are
eligible for a claim. A lease is current only while state is leased, its token
matches, and the clock is strictly before expires_at. Tokens are positive Python
integers; booleans, floats, strings, and other types are invalid. Unknown IDs,
wrong tokens, and jobs without a valid lease make ack/fail return False without
modifying state. No worker ID is needed for ack/fail: the job ID and token identify
the lease. Repeating a successful acknowledgment or failure returns False.

Inputs and returned payloads are detached value snapshots. Mutating a submitted
payload after submission, a returned payload, or a status result does not mutate
stored state. Public calls are synchronous; successful returns mean their state
changes have committed. Storage/transaction failures raise exceptions rather
than return a success or a no-work result; exception classes and text for such
failures are unspecified. Database schema and connection lifetimes are private.
Each process constructs its own queue; sharing one instance across threads is
outside the supported interface. No explicit close call is required of callers.

## Established requirements

These requirements apply to all supported calls, across queue instances and
process restarts, not only to the sequential examples in the existing tests.

| ID | Requirement |
| --- | --- |
| JQ-1 | When a process restarts and reopens the database, the queue shall retain every committed job, payload, status, lease owner, lease token, lease deadline, and attempt count. |
| JQ-2 | The queue shall use file-backed SQLite at database_path as its authoritative job store, shared by all instances using that file. |
| JQ-3 | When independent worker processes claim using separate database connections, the queue shall grant at most one valid lease per job at a time and atomically increment its attempt count with the claim, using that per-job count as the monotonically increasing lease token. |
| JQ-4 | The queue shall grant leases lasting 30 seconds. When the clock is greater than or equal to a lease deadline, the queue shall treat that lease as invalid and make the job immediately eligible for retry if attempts remain. |
| JQ-5 | If an acknowledgment or failure supplies an invalid, expired, or superseded token, then the queue shall return False without changing job state. |
| JQ-6 | The queue shall persist attempt counts and retry eligibility across restarts, allow at most 3 attempts per job, and make a job immediately eligible again after a valid failure while attempts remain. |
| JQ-7 | When the final attempt fails or expires, the queue shall mark the job exhausted and prevent every subsequent claim of that job. |
| JQ-8 | When a valid lease is acknowledged, the queue shall mark the job completed, retain that terminal status across restarts, and prevent every subsequent claim of that job. |
| JQ-9 | If an operation fails or its process crashes before commit, then the queue shall expose none of that operation's partial state changes to subsequent calls or other connections. |
| JQ-10 | The queue shall preserve the supported API's signatures, return shapes, duplicate rejection, value snapshots, state transitions, and injectable clock behavior described above. |

Claiming the third attempt is allowed; it remains leased until acknowledged,
failed, or expired. A successful third attempt completes normally. Expiration
can be evaluated lazily during claim/status, without a background cleanup service.
An invalid ack/fail does not perform even lazy state updates; a later claim/status
can materialize expiry. Clearing a lease removes its owner and deadline; attempts
are never reset, including after completion or exhaustion. There is no deletion
or ID-reuse API.

## Recovery boundary

The promise is at-least-once processing eligibility while retry capacity remains,
not exactly-once external side effects. Recovery assumes a usable SQLite file
on local storage, a progressing shared clock, and workers that resume polling.
A worker that crashes after an external effect but before acknowledgment may
leave work eligible for a repeat attempt. The queue coordinates state, not the
execution or deduplication of arbitrary external effects. No networking,
distributed service, message broker, or third-party dependency is required.
Storage media loss/corruption and external-effect transactions are outside scope.

## Accepted storage decision

Status: accepted. File-backed SQLite is the established authoritative storage
technology for this local, standard-library-only application (JQ-2). Independent
worker connections need shared durable state and atomic transitions (JQ-1,
JQ-3, JQ-9). The accepted choice uses Python's sqlite3 module and local-file
transactions; it entails database locking and recovery work. Schema and SQL
details remain implementation choices. This is an existing decision, not a
proposal to select another storage architecture.

## Current implementation and known gaps

In [job_queue.py](../job_queue.py), JobQueue.__init__ creates an empty _jobs
dictionary for every instance. database_path is retained but never opened.
submit, claim, ack, fail, and status operate only on that dictionary. Sequential
calls implement the local lease, fencing, retry, and terminal-state transitions;
[test_job_queue.py](../test_job_queue.py) exercises that limited behavior.

Reopening loses all jobs, payloads, leases, attempts, and terminal states (JQ-1,
JQ-6, JQ-8). Separate instances do not share pending work or coordinate leases;
the same ID can be independently submitted and leased twice (JQ-2, JQ-3).
Tokens and budgets can start over after reopening, so fencing and exhaustion
are not guaranteed across recovery (JQ-5, JQ-7). There are no SQLite connections
or transactions providing commit/rollback and crash integrity (JQ-9). Local
expiry handling (JQ-4) cannot recover work whose entire state has been lost.
These are defects relative to established requirements, not supported limits
on persistence or concurrent independent workers.
''',
}
