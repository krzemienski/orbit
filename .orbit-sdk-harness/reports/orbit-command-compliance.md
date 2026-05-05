# Orbit Command Compliance

Status: **PASS**

## Command Validator

```json

{
  "plugin_root": "/Users/nick/Desktop/orbit",
  "commands_dir": "/Users/nick/Desktop/orbit/commands",
  "checks": [
    {
      "check_name": "commands_dir_present",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_present_audit-gaps",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/audit-gaps.md",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_body_non_empty_audit-gaps",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/audit-gaps.md",
      "observed_value": "chars=307",
      "expected_value": "non-empty",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_purpose_heading_audit-gaps",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/audit-gaps.md",
      "observed_value": "heading present",
      "expected_value": "markdown heading present",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_example_audit-gaps",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/audit-gaps.md",
      "observed_value": "fenced_blocks=1",
      "expected_value": ">=1 fenced example block",
      "failure_reason": ""
    },
    {
      "check_name": "command_maps_to_workflow_audit-gaps",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/audit-gaps.md",
      "observed_value": "mentions orbit-audit or skill",
      "expected_value": "mentions orbit-audit or skill",
      "failure_reason": ""
    },
    {
      "check_name": "command_present_mine-intent",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/mine-intent.md",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_body_non_empty_mine-intent",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/mine-intent.md",
      "observed_value": "chars=186",
      "expected_value": "non-empty",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_purpose_heading_mine-intent",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/mine-intent.md",
      "observed_value": "heading present",
      "expected_value": "markdown heading present",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_example_mine-intent",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/mine-intent.md",
      "observed_value": "fenced_blocks=1",
      "expected_value": ">=1 fenced example block",
      "failure_reason": ""
    },
    {
      "check_name": "command_maps_to_workflow_mine-intent",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/mine-intent.md",
      "observed_value": "mentions orbit-audit or skill",
      "expected_value": "mentions orbit-audit or skill",
      "failure_reason": ""
    },
    {
      "check_name": "command_present_validate-claims",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/validate-claims.md",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_body_non_empty_validate-claims",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/validate-claims.md",
      "observed_value": "chars=220",
      "expected_value": "non-empty",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_purpose_heading_validate-claims",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/validate-claims.md",
      "observed_value": "heading present",
      "expected_value": "markdown heading present",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_example_validate-claims",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/validate-claims.md",
      "observed_value": "fenced_blocks=1",
      "expected_value": ">=1 fenced example block",
      "failure_reason": ""
    },
    {
      "check_name": "command_maps_to_workflow_validate-claims",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/validate-claims.md",
      "observed_value": "mentions orbit-audit or skill",
      "expected_value": "mentions orbit-audit or skill",
      "failure_reason": ""
    },
    {
      "check_name": "command_present_render-dashboard",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/render-dashboard.md",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_body_non_empty_render-dashboard",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/render-dashboard.md",
      "observed_value": "chars=187",
      "expected_value": "non-empty",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_purpose_heading_render-dashboard",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/render-dashboard.md",
      "observed_value": "heading present",
      "expected_value": "markdown heading present",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_example_render-dashboard",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/render-dashboard.md",
      "observed_value": "fenced_blocks=1",
      "expected_value": ">=1 fenced example block",
      "failure_reason": ""
    },
    {
      "check_name": "command_maps_to_workflow_render-dashboard",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/render-dashboard.md",
      "observed_value": "mentions orbit-audit or skill",
      "expected_value": "mentions orbit-audit or skill",
      "failure_reason": ""
    },
    {
      "check_name": "command_present_compare-plan",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/compare-plan.md",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_body_non_empty_compare-plan",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/compare-plan.md",
      "observed_value": "chars=218",
      "expected_value": "non-empty",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_purpose_heading_compare-plan",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/compare-plan.md",
      "observed_value": "heading present",
      "expected_value": "markdown heading present",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_example_compare-plan",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/compare-plan.md",
      "observed_value": "fenced_blocks=1",
      "expected_value": ">=1 fenced example block",
      "failure_reason": ""
    },
    {
      "check_name": "command_maps_to_workflow_compare-plan",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/compare-plan.md",
      "observed_value": "mentions orbit-audit or skill",
      "expected_value": "mentions orbit-audit or skill",
      "failure_reason": ""
    },
    {
      "check_name": "command_present_review-window",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_body_non_empty_review-window",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "chars=437",
      "expected_value": "non-empty",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_purpose_heading_review-window",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "heading present",
      "expected_value": "markdown heading present",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_example_review-window",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "fenced_blocks=2",
      "expected_value": ">=1 fenced example block",
      "failure_reason": ""
    },
    {
      "check_name": "command_maps_to_workflow_review-window",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "mentions orbit-audit or skill",
      "expected_value": "mentions orbit-audit or skill",
      "failure_reason": ""
    },
    {
      "check_name": "review_window_documents_days",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "present",
      "expected_value": "--days documented",
      "failure_reason": ""
    },
    {
      "check_name": "review_window_documents_since",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "present",
      "expected_value": "--since documented",
      "failure_reason": ""
    },
    {
      "check_name": "review_window_documents_from",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "present",
      "expected_value": "--from documented",
      "failure_reason": ""
    },
    {
      "check_name": "review_window_documents_to",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-window.md",
      "observed_value": "present",
      "expected_value": "--to documented",
      "failure_reason": ""
    },
    {
      "check_name": "command_present_review-last-3-days",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-last-3-days.md",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_body_non_empty_review-last-3-days",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-last-3-days.md",
      "observed_value": "chars=185",
      "expected_value": "non-empty",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_purpose_heading_review-last-3-days",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-last-3-days.md",
      "observed_value": "heading present",
      "expected_value": "markdown heading present",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_example_review-last-3-days",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-last-3-days.md",
      "observed_value": "fenced_blocks=2",
      "expected_value": ">=1 fenced example block",
      "failure_reason": ""
    },
    {
      "check_name": "command_maps_to_workflow_review-last-3-days",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-last-3-days.md",
      "observed_value": "mentions orbit-audit or skill",
      "expected_value": "mentions orbit-audit or skill",
      "failure_reason": ""
    },
    {
      "check_name": "review_last_3_days_alias",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/review-last-3-days.md",
      "observed_value": "alias documented",
      "expected_value": "documents alias for --days 3",
      "failure_reason": ""
    },
    {
      "check_name": "command_present_rebuild-ledger",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/rebuild-ledger.md",
      "observed_value": "present",
      "expected_value": "present"
    },
    {
      "check_name": "command_body_non_empty_rebuild-ledger",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/rebuild-ledger.md",
      "observed_value": "chars=181",
      "expected_value": "non-empty",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_purpose_heading_rebuild-ledger",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/rebuild-ledger.md",
      "observed_value": "heading present",
      "expected_value": "markdown heading present",
      "failure_reason": ""
    },
    {
      "check_name": "command_has_example_rebuild-ledger",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/rebuild-ledger.md",
      "observed_value": "fenced_blocks=1",
      "expected_value": ">=1 fenced example block",
      "failure_reason": ""
    },
    {
      "check_name": "command_maps_to_workflow_rebuild-ledger",
      "status": "PASS",
      "evidence_path": "/Users/nick/Desktop/orbit/commands/rebuild-ledger.md",
      "observed_value": "mentions orbit-audit or skill",
      "expected_value": "mentions orbit-audit or skill",
      "failure_reason": ""
    }
  ],
  "status": "PASS",
  "_returncode": 0
}

```
