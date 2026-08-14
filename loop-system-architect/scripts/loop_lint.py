#!/usr/bin/env python3
"""Deterministic completeness linter for loop.contract.json.

Profiles:
- Full contract: every section required (default).
- learning.enabled == false: learning.promotion_authority / monitoring_window /
  rollback / protected_fields are not required.
- capabilities.discovery == "none" with a non-empty capabilities.reason:
  candidate_creation and sandbox_required are not required.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PLACEHOLDER = re.compile(r"^(replace-me|todo|tbd|unknown)$", re.IGNORECASE)
REQUIRED_TOP = (
    "schema_version", "loop_id", "mode", "status", "objective", "source_policy",
    "control", "triggers", "state", "roles", "capabilities", "authority",
    "verification", "failure_policy", "budgets", "runtime_safety", "observability",
    "replacement", "learning", "retirement",
)
PROTECTED = {
    "objective", "source_policy", "authority", "tenant_scope", "privacy",
    "verification.acceptance_checks",
}
TRIGGER_TYPES = {"continuous", "schedule", "event", "hybrid", "manual"}
REQUIRED_VALUES = (
    "schema_version", "loop_id", "mode", "status", "objective.statement",
    "objective.owner", "source_policy.authoritative_sources", "control.sensor.name",
    "control.sensor.signal", "control.sensor.collection", "control.comparator.rule",
    "control.comparator.window", "control.controller.decision_space",
    "control.actuator.actions", "control.actuator.feedback_path", "state.path",
    "state.cursor_fields", "state.event_log", "state.evidence_store", "state.atomic_write",
    "state.recovery", "verification.acceptance_checks", "verification.failure_path_checks",
    "verification.evidence_required", "verification.pass_rule",
    "failure_policy.classification", "failure_policy.rollback", "failure_policy.kill",
    "runtime_safety.idempotency_key", "runtime_safety.dedupe_store",
    "runtime_safety.concurrency_lock", "runtime_safety.side_effect_choke_point",
    "runtime_safety.tenant_scope", "observability.status_view", "observability.alerts",
    "replacement.atomic_promotion", "retirement.conditions",
)
LEARNING_REQUIRED_VALUES = (
    "learning.promotion_authority", "learning.monitoring_window", "learning.rollback",
)


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip() or bool(PLACEHOLDER.match(value.strip()))
    if isinstance(value, (list, dict)):
        return not value
    return False


def get(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print("ERROR: contract root must be an object", file=sys.stderr)
        return 2

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level section: {key}")

    for path in REQUIRED_VALUES:
        if is_blank(get(data, path)):
            errors.append(f"missing or placeholder value: {path}")

    mode = data.get("mode")
    if mode not in {"terminal", "recurring"}:
        errors.append("mode must be terminal or recurring")
    if mode == "terminal" and is_blank(get(data, "objective.completion_condition")):
        errors.append("terminal loop requires objective.completion_condition")
    if mode == "recurring" and is_blank(get(data, "objective.per_run_success")):
        errors.append("recurring loop requires objective.per_run_success")

    triggers = data.get("triggers")
    if not isinstance(triggers, list) or not triggers:
        errors.append("at least one trigger is required")
    else:
        for index, trigger in enumerate(triggers):
            if not isinstance(trigger, dict):
                errors.append(f"triggers[{index}] must be an object")
                continue
            if trigger.get("type") not in TRIGGER_TYPES:
                errors.append(f"triggers[{index}].type is invalid")
            for key in ("condition", "preflight", "dedupe_key"):
                if is_blank(trigger.get(key)):
                    errors.append(f"triggers[{index}].{key} is missing or placeholder")

    role_names = {
        role.get("name") for role in data.get("roles", []) if isinstance(role, dict)
    }
    for required in ("orchestrator", "executor", "verifier"):
        if required not in role_names:
            errors.append(f"required role missing: {required}")

    if get(data, "verification.independent") is not True:
        errors.append("verification.independent must be true")
    if get(data, "verification.verifier_cannot_write_work_product") is not True:
        errors.append("verifier must be prevented from writing the work product")
    if get(data, "runtime_safety.fail_closed") is not True:
        errors.append("runtime_safety.fail_closed must be true")

    max_attempts = get(data, "failure_policy.max_attempts")
    same_limit = get(data, "failure_policy.same_failure_limit")
    timeout = get(data, "failure_policy.timeout_seconds")
    if not isinstance(max_attempts, int) or max_attempts < 1:
        errors.append("failure_policy.max_attempts must be a positive integer")
    if not isinstance(same_limit, int) or same_limit < 1:
        errors.append("failure_policy.same_failure_limit must be a positive integer")
    if not isinstance(timeout, int) or timeout < 1:
        errors.append("failure_policy.timeout_seconds must be a positive integer")

    for key in ("max_turns", "max_tokens", "max_wall_time_seconds"):
        value = get(data, f"budgets.{key}")
        if not isinstance(value, int) or value < 1:
            errors.append(f"budgets.{key} must be a positive integer")
    cost = get(data, "budgets.max_cost")
    if not isinstance(cost, (int, float)) or cost < 0:
        errors.append("budgets.max_cost must be a non-negative number")
    elif cost == 0:
        warnings.append("budgets.max_cost is 0; confirm this means local/unmetered, not unlimited")

    protected = set(get(data, "authority.protected_fields") or [])
    missing_protected = sorted(PROTECTED - protected)
    if missing_protected:
        errors.append("authority.protected_fields missing: " + ", ".join(missing_protected))

    learning_enabled = get(data, "learning.enabled")
    if learning_enabled is False:
        # Minimal profile: the loop declares it does not self-improve, so the
        # learning pipeline fields are not required.
        pass
    else:
        for path in LEARNING_REQUIRED_VALUES:
            if is_blank(get(data, path)):
                errors.append(f"missing or placeholder value: {path}")
        learning_protected = set(get(data, "learning.protected_fields") or [])
        missing_learning = sorted(PROTECTED - learning_protected)
        if missing_learning:
            errors.append("learning.protected_fields missing: " + ", ".join(missing_learning))

    if get(data, "replacement.single_active_version") is not True:
        errors.append("replacement.single_active_version must be true")
    for key in ("impact_scan", "contradiction_scan", "zero_context_probe"):
        if get(data, f"replacement.{key}") is not True:
            errors.append(f"replacement.{key} must be true")

    discovery = get(data, "capabilities.discovery")
    if discovery == "none":
        # Minimal profile: no capability lifecycle, but the omission must be justified.
        if is_blank(get(data, "capabilities.reason")):
            errors.append('capabilities.discovery "none" requires a non-empty capabilities.reason')
    else:
        if discovery != "open":
            warnings.append("capabilities.discovery is not open; document why a static restriction is required")
        for key in ("sandbox_required", "candidate_creation"):
            if get(data, f"capabilities.{key}") is not True:
                errors.append(f"capabilities.{key} must be true for autonomous skill lifecycle")

    result = {
        "contract": str(args.contract),
        "verdict": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
    }
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"VERDICT: {result['verdict']}")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARNING: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
