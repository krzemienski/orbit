# Orbit Skill Compliance

Status: **PASS**

## Frontmatter Validator

Evidence: `.orbit-sdk-harness/static-frontmatter.json`

```json

{
  "skills_dir": "/Users/nick/Desktop/orbit/skills",
  "skills": [
    {
      "name": "gap-analysis",
      "skill_md": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md",
      "status": "PASS",
      "checks": [
        {
          "check_name": "frontmatter_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md",
          "observed_value": "parsed",
          "expected_value": "--- ... --- block at top of file"
        },
        {
          "check_name": "frontmatter_name_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md",
          "observed_value": "gap-analysis",
          "expected_value": "present"
        },
        {
          "check_name": "frontmatter_name_format",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md",
          "observed_value": "gap-analysis",
          "expected_value": "^[a-z0-9-]+$ and <=64 chars"
        },
        {
          "check_name": "frontmatter_description_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md",
          "observed_value": "len=343",
          "expected_value": "non-empty string"
        },
        {
          "check_name": "frontmatter_description_no_xml",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md",
          "observed_value": "no XML tags",
          "expected_value": "no XML tags"
        },
        {
          "check_name": "frontmatter_description_length",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md",
          "observed_value": "len=343",
          "expected_value": "<= 1024"
        },
        {
          "check_name": "body_non_empty",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md",
          "observed_value": "body_chars=1975",
          "expected_value": "non-empty body"
        }
      ]
    },
    {
      "name": "instruction-ledger",
      "skill_md": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md",
      "status": "PASS",
      "checks": [
        {
          "check_name": "frontmatter_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md",
          "observed_value": "parsed",
          "expected_value": "--- ... --- block at top of file"
        },
        {
          "check_name": "frontmatter_name_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md",
          "observed_value": "instruction-ledger",
          "expected_value": "present"
        },
        {
          "check_name": "frontmatter_name_format",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md",
          "observed_value": "instruction-ledger",
          "expected_value": "^[a-z0-9-]+$ and <=64 chars"
        },
        {
          "check_name": "frontmatter_description_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md",
          "observed_value": "len=234",
          "expected_value": "non-empty string"
        },
        {
          "check_name": "frontmatter_description_no_xml",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md",
          "observed_value": "no XML tags",
          "expected_value": "no XML tags"
        },
        {
          "check_name": "frontmatter_description_length",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md",
          "observed_value": "len=234",
          "expected_value": "<= 1024"
        },
        {
          "check_name": "body_non_empty",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md",
          "observed_value": "body_chars=655",
          "expected_value": "non-empty body"
        }
      ]
    },
    {
      "name": "plan-execution-audit",
      "skill_md": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md",
      "status": "PASS",
      "checks": [
        {
          "check_name": "frontmatter_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md",
          "observed_value": "parsed",
          "expected_value": "--- ... --- block at top of file"
        },
        {
          "check_name": "frontmatter_name_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md",
          "observed_value": "plan-execution-audit",
          "expected_value": "present"
        },
        {
          "check_name": "frontmatter_name_format",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md",
          "observed_value": "plan-execution-audit",
          "expected_value": "^[a-z0-9-]+$ and <=64 chars"
        },
        {
          "check_name": "frontmatter_description_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md",
          "observed_value": "len=234",
          "expected_value": "non-empty string"
        },
        {
          "check_name": "frontmatter_description_no_xml",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md",
          "observed_value": "no XML tags",
          "expected_value": "no XML tags"
        },
        {
          "check_name": "frontmatter_description_length",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md",
          "observed_value": "len=234",
          "expected_value": "<= 1024"
        },
        {
          "check_name": "body_non_empty",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md",
          "observed_value": "body_chars=570",
          "expected_value": "non-empty body"
        }
      ]
    },
    {
      "name": "validation-pairing",
      "skill_md": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md",
      "status": "PASS",
      "checks": [
        {
          "check_name": "frontmatter_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md",
          "observed_value": "parsed",
          "expected_value": "--- ... --- block at top of file"
        },
        {
          "check_name": "frontmatter_name_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md",
          "observed_value": "validation-pairing",
          "expected_value": "present"
        },
        {
          "check_name": "frontmatter_name_format",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md",
          "observed_value": "validation-pairing",
          "expected_value": "^[a-z0-9-]+$ and <=64 chars"
        },
        {
          "check_name": "frontmatter_description_present",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md",
          "observed_value": "len=224",
          "expected_value": "non-empty string"
        },
        {
          "check_name": "frontmatter_description_no_xml",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md",
          "observed_value": "no XML tags",
          "expected_value": "no XML tags"
        },
        {
          "check_name": "frontmatter_description_length",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md",
          "observed_value": "len=224",
          "expected_value": "<= 1024"
        },
        {
          "check_name": "body_non_empty",
          "status": "PASS",
          "evidence_path": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md",
          "observed_value": "body_chars=618",
          "expected_value": "non-empty body"
        }
      ]
    }
  ],
  "status": "PASS",
  "_returncode": 0
}

```
