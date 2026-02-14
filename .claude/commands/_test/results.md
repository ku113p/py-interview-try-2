# Test Results

## Summary

| Metric | Value |
|--------|-------|
| Total Cases | 10 |
| Passed | 10 |
| Failed | 0 |
| Pass Rate | 100% |

## Results by Case

| # | Case Name | Status | Areas | Sub-Areas | Summaries | Knowledge | Last Run |
|---|-----------|--------|-------|-----------|-----------|-----------|----------|
| 1 | CRUD Operations | PASS | 3/3 | 2/2-2 | 1/true | 4/true | 2026-02-13 03:09 |
| 5 | Quick Interaction | PASS | 1/1 | 0/0-0 | 0/false | 0/false | 2026-02-13 03:09 |
| 13 | Knowledge - Skill Extraction | PASS | 3/3 | 2/2-2 | 1/true | 5/true | 2026-02-13 03:09 |
| 18 | Multi-Area - Creation | PASS | 3/3 | 0/0-0 | 0/false | 0/false | 2026-02-13 03:09 |
| 21 | Tree Sub-Areas Full Flow | PASS | 4/4 | 3/3-3 | 1/true | 7/true | 2026-02-13 03:09 |
| 22 | Subtree - Bulk Create | PASS | 7/7 | 6/6-6 | 0/false | 0/false | 2026-02-13 03:09 |
| 23 | Subtree - Deep Nesting | PASS | 5/5 | 4/4-4 | 0/false | 0/false | 2026-02-13 03:09 |
| 24 | Small Talk Flow | PASS | 3/3 | 2/2-2 | 0/false | 0/false | 2026-02-13 03:09 |
| 25 | Completed Area Message | PASS | 3/3 | 2/2-2 | 1/true | 5/true | 2026-02-13 03:09 |
| 26 | Reset Area Command | PASS | 3/3 | 2/2-2 | 1/true | 4/true | 2026-02-13 03:09 |

## Test Case Descriptions

| # | Name | Focus |
|---|------|-------|
| 1 | CRUD Operations | Basic area + sub-area creation, leaf-by-leaf interview flow |
| 5 | Quick Interaction | Minimal conversation, no extraction expected |
| 13 | Knowledge - Skill Extraction | Technical skill extraction from leaf-by-leaf interview |
| 18 | Multi-Area - Creation | Creating multiple root areas in one session |
| 21 | Tree Sub-Areas Full Flow | Hierarchical sub-areas with nested parent-child relationships |
| 22 | Subtree - Bulk Create | Bulk nested sub-area creation via create_subtree |
| 23 | Subtree - Deep Nesting | Deep nesting (3+ levels) with create_subtree |
| 24 | Small Talk Flow | Greeting/app questions before transitioning to area creation |
| 25 | Completed Area Message | Messaging a completed area shows completion notice |
| 26 | Reset Area Command | Completed area notification with reset command suggestion |

## Expected Format

Test cases use the following expected fields:

```json
{
  "expected": {
    "life_areas": 3,
    "sub_areas_min": 2,
    "sub_areas_max": 2,
    "summaries": true,
    "knowledge": true
  }
}
```

- `life_areas` - Exact count of life_areas table rows
- `sub_areas_min/max` - Range for life_areas with parent_id (sub-areas)
- `summaries` - Boolean: expect area_summaries > 0
- `knowledge` - Boolean: expect user_knowledge_areas > 0

## Recent Changes

### 2026-02-13: Fixed Leaf Interview Flow Issues

**Issue 1 - Small talk routing override:**
- Short confirmations like "yes" were being routed to `small_talk` instead of `conduct_interview`
- Fix: `extract_target` now checks for active interview context and overrides to `conduct_interview`

**Issue 2 - Leaf order predictability:**
- Changed `get_descendants` from `ORDER BY title` to `ORDER BY id` (UUID7)
- Leaves are now asked in creation order (predictable, intuitive)

**Issue 3 - Evaluation too lenient:**
- `PROMPT_QUICK_EVALUATE` now explicitly requires content to match the specific topic being asked
- Answers about wrong topics are marked as "partial" not "complete"

**Test cases updated:**
- All 5 extraction test cases (1, 13, 21, 25, 26) updated for leaf-by-leaf interview flow
- Answers now provided in creation order with topic-specific content

### 2026-02-11: Fixed Three Failing Tests (1, 22, 24)

**Test 1 - CRUD Operations:**
- Fixed UUID normalization bug in `_validate_uuid` function
- Now returns `str(parsed)` instead of original input to ensure consistent UUIDs

**Test 22 - Subtree Bulk Create:**
- Updated expectations to correct counts: 7 areas, 6 sub-areas
- Structure: 1 root + 2 companies + 4 children (Responsibilities/Achievements each)

**Test 24 - Small Talk Flow:**
- Updated test inputs to use explicit sub-area creation syntax
- Changed from conversational auto-extraction to: "Create area Hobbies with sub-areas Reading, Hiking"

### 2026-02-11: Completed Area Prevention Feature

- Added test cases 25 and 26 for completed area handling
- New `extracted_at` column tracks when knowledge extraction completed
- Messaging a completed area shows notification with `/reset-area` command
- Test 25 now passing - completed area response working correctly

### 2026-02-11: Small Talk Feature

- Added test case 24 for small talk flow (greetings, app questions)
- New routing target `small_talk` handles casual conversation before interview/area modes

### 2026-02-10: Test Suite Cleanup

- Reduced from 20 to 5 focused test cases
- Replaced `criteria` with `sub_areas` (hierarchical structure)
- Replaced `summaries_min/max` and `knowledge_min/max` with boolean flags
- Added test 21 for hierarchical sub-area validation
- Fixed token limit for knowledge extraction (1024 -> 4096)

## Resolved Issues

### Leaf Interview Flow Issues (Fixed 2026-02-13)

Three issues were identified and fixed:
1. `extract_target` routing confirmations to `small_talk` during active interviews
2. Leaf order was alphabetical (unpredictable) instead of creation order
3. Evaluation accepted answers about wrong topics as "complete"

### Test 1 - UUID Normalization (Fixed 2026-02-11)
The `_validate_uuid` function was validating UUIDs but returning the original string unchanged. When UUIDs passed through LLM extraction, minor corruption could occur. Fixed by returning the normalized UUID via `str(uuid.UUID(value))`.

### Test 22 - Expectations (Fixed 2026-02-11)
Test expected 5 areas / 4 sub-areas but actual correct count is 7 areas / 6 sub-areas for the nested structure.

### Test 24 - Test Inputs (Fixed 2026-02-11)
Test expected auto-extraction of sub-areas from conversational input, but this feature doesn't exist. Fixed by using explicit creation syntax.

### Azure Provider Error (Fixed 2026-02-11)
Fixed `BadRequestError: Error code: 400 - No tool call found for function call output` in `small_talk_response` and `completed_area_response` nodes by filtering out tool-related messages before invoking LLM without tools bound.
