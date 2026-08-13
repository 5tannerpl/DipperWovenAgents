# DipperWovenAgent — Development Plan

## 1. Project Goal

**DipperWovenAgent** is a compliance-first agentic AI system for debt collection.

The existing **RAG Service is already complete and is explicitly out of scope for this development plan**. DipperWovenAgent will consume the RAG Service as an external evidence-retrieval dependency.

The development focus is therefore:

```text
Before RAG
────────────────────────────────────────
Input Understanding
→ Event Detection
→ Compliance Question Decomposition
→ Fact Sufficiency
→ Context / Fact Resolution
→ Compliance Planning
→ Source Planning
→ Retrieval Query Generation

Existing RAG Service
────────────────────────────────────────
Hybrid Retrieval
→ Metadata Filters
→ Reranking
→ Evidence / Citation

After RAG
────────────────────────────────────────
Evidence Evaluation
→ Compliance Decision
→ SOP Resolution
→ Action Planning
→ Human Approval / Automation Gate
→ Business API Execution
→ Audit
```

---

## 2. Scope

### In Scope

1. Agent orchestration and state management
2. Input normalization and event understanding
3. Compliance question decomposition
4. Information sufficiency checking
5. Case context and verified-fact resolution
6. Compliance planning
7. Source planning
8. Retrieval query generation
9. Integration with the completed RAG Service
10. Evidence aggregation and sufficiency evaluation
11. Compliance decision service
12. SOP resolution
13. Action planning
14. Human approval / automation gate
15. Execution through business APIs
16. Execution audit
17. API layer for the existing collection platform
18. Unit, integration, workflow, regression and safety tests
19. Observability and production deployment

### Out of Scope

The following already-completed RAG capabilities will not be rebuilt:

- document ingestion
- chunking
- embeddings
- vector database
- BM25 / keyword index
- hybrid retrieval
- metadata filtering
- RAG-side reranking
- evidence citation generation
- RAG infrastructure

DipperWovenAgent only calls the existing RAG retrieval API.

---

## 3. Target Architecture

```text
Existing Debt Collection System
        │
        │ Collector Note / Proposed Action
        ▼
┌───────────────────────────────────────────────┐
│              DipperWovenAgent                │
│                                               │
│  1. Input / Event Understanding              │
│  2. Compliance Question Decomposer           │
│  3. Information Sufficiency Checker          │
│  4. Context / Fact Resolver                  │
│  5. Compliance Planner                       │
│  6. Source Planner                           │
│  7. Retrieval Query Generator                │
│                 │                             │
└─────────────────┼─────────────────────────────┘
                  │
                  ▼
          Existing RAG Service
                  │
                  ▼
┌───────────────────────────────────────────────┐
│              DipperWovenAgent                │
│                                               │
│  8. Evidence Aggregator                      │
│  9. Evidence Sufficiency Evaluator           │
│ 10. Compliance Service                       │
│ 11. SOP Resolver                             │
│ 12. Action Planner                           │
│ 13. Approval / Automation Gate               │
│ 14. Execution Agent                          │
│ 15. Audit                                    │
└─────────────────┬─────────────────────────────┘
                  │
                  ▼
             Business APIs
                  │
                  ▼
      Database / Messaging / Workflow
```

---

## 4. Recommended Repository Structure

```text
dipper-woven-agent/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── agent.py
│   │   │   ├── compliance.py
│   │   │   ├── approvals.py
│   │   │   └── executions.py
│   │   └── schemas/
│   │
│   ├── orchestration/
│   │   ├── graph_builder.py
│   │   ├── state.py
│   │   └── routing.py
│   │
│   ├── understanding/
│   │   ├── input_normalizer.py
│   │   ├── event_detector.py
│   │   ├── question_decomposer.py
│   │   └── sufficiency_checker.py
│   │
│   ├── context/
│   │   ├── case_context_resolver.py
│   │   ├── representative_resolver.py
│   │   ├── authority_resolver.py
│   │   └── communication_resolver.py
│   │
│   ├── planning/
│   │   ├── compliance_planner.py
│   │   ├── source_planner.py
│   │   └── retrieval_query_generator.py
│   │
│   ├── rag/
│   │   └── rag_client.py
│   │
│   ├── evidence/
│   │   ├── evidence_aggregator.py
│   │   └── evidence_evaluator.py
│   │
│   ├── compliance/
│   │   ├── compliance_service.py
│   │   ├── decision_models.py
│   │   └── rule_reasoner.py
│   │
│   ├── sop/
│   │   ├── sop_resolver.py
│   │   └── sop_models.py
│   │
│   ├── action/
│   │   ├── action_planner.py
│   │   ├── approval_gate.py
│   │   ├── execution_agent.py
│   │   └── business_api_client.py
│   │
│   ├── audit/
│   │   ├── execution_audit.py
│   │   └── audit_models.py
│   │
│   └── common/
│       ├── config.py
│       ├── logging.py
│       ├── errors.py
│       └── llm_client.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── workflows/
│   ├── regression/
│   └── fixtures/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## 5. Core Agent State

Create a single workflow state shared across nodes.

```python
class DipperWovenAgentState(TypedDict, total=False):
    request_id: str
    case_id: str
    target_type: str
    raw_input: str

    normalized_input: dict

    detected_facts: list[dict]
    detected_events: list[str]
    intended_actions: list[dict]
    entities: list[dict]

    compliance_questions: list[dict]

    missing_facts: list[str]
    verified_facts: dict

    compliance_plan: dict
    source_plan: dict
    retrieval_requests: list[dict]

    rag_evidence: list[dict]

    evidence_evaluation: dict
    compliance_decision: dict

    applicable_sops: list[dict]
    action_plan: list[dict]

    approval_status: str
    execution_results: list[dict]

    errors: list[dict]
    audit_context: dict
```

A major design rule is to keep these concepts separate:

```text
Detected Fact
≠ Verified Fact

Compliance Question
≠ Retrieval Query

Retrieved Evidence
≠ Compliance Decision

Missing Rule Evidence
≠ Missing Case Fact
```

---

# 6. Development Phases

## Phase 0 — Foundation

### Goal

Create the deployable DipperWovenAgent service shell and orchestration infrastructure.

### Tasks

- create Python service
- FastAPI API layer
- configuration management
- structured logging
- request / correlation IDs
- agent state model
- graph/orchestrator
- exception handling
- health endpoint
- dependency injection / service factories
- LLM client abstraction
- RAG client abstraction
- business API client abstraction

### Initial API

```http
POST /api/agent/invoke
POST /api/agent/stream
GET  /health
```

### Deliverable

A minimal graph that accepts a request, builds state, runs one placeholder node and returns a structured response.

---

## Phase 1 — Input Understanding and Event Detection

### Goal

Convert a collector note or proposed action into structured facts, events and intended actions.

### Components

```text
input_normalizer
       ↓
event_detector
```

### Input

```json
{
  "case_id": "12345",
  "target_type": "note",
  "content": "Customer says his solicitor will manage the account. Collector plans to call the customer tomorrow for payment."
}
```

### Output

```json
{
  "facts": [
    {
      "type": "representative_claim",
      "value": "Customer stated a solicitor is dealing with the debt",
      "verification_status": "unverified"
    }
  ],
  "intended_actions": [
    {
      "action": "call_customer",
      "purpose": "request_payment",
      "when": "tomorrow"
    }
  ],
  "detected_events": [
    "POTENTIAL_REPRESENTATIVE",
    "PROPOSED_DIRECT_CONTACT"
  ]
}
```

### First supported events

Start with:

```text
REPRESENTATIVE
PROPOSED_DIRECT_CONTACT
BANKRUPTCY
DEBT_AGREEMENT
HARDSHIP
VULNERABILITY
DISPUTE
COMPLAINT
DECEASED
LEGAL_PROCEEDING
PAYMENT_ARRANGEMENT
```

### Acceptance Criteria

- raw text never becomes a verified fact automatically
- every detected fact carries verification status
- intended actions are separated from facts
- event detection supports multiple simultaneous events
- structured output passes schema validation

---

## Phase 2 — Compliance Question Decomposition

### Goal

Turn detected events into explicit compliance questions.

### Component

```text
question_decomposer
```

### Example

For:

```text
POTENTIAL_REPRESENTATIVE
+
PROPOSED_DIRECT_CONTACT
```

produce questions such as:

```text
Q1 representation_status
Q2 authority
Q3 direct_contact
Q4 contact_exception
Q5 payment_request
Q6 privacy
```

### Implementation

Use:

```text
Event
→ event-specific question template
→ LLM contextual expansion
→ schema validation
```

Do not let the LLM generate an unrestricted arbitrary set of topics.

### Acceptance Criteria

- every question has `id`
- every question has `topic`
- every question has original natural-language compliance question
- one event can produce multiple questions
- duplicate questions are removed

---

## Phase 3 — Information Sufficiency and Fact Resolution

### Goal

Determine whether the case has enough verified facts before a compliance decision.

### Components

```text
sufficiency_checker
        ↓
case_context_resolver
        ├─ representative_resolver
        ├─ authority_resolver
        └─ communication_resolver
```

### Integrations

DipperWovenAgent calls existing business APIs or read-only case APIs:

```http
GET /api/cases/{caseId}
GET /api/cases/{caseId}/notes
GET /api/cases/{caseId}/representatives
GET /api/cases/{caseId}/authorities
GET /api/cases/{caseId}/communications
```

### Output

```json
{
  "customer_claimed_solicitor": true,
  "representative_record_exists": false,
  "authority_verified": false,
  "no_direct_contact_instruction": null
}
```

### Important Rule

Do not immediately ask the collector for missing information.

Resolution order:

```text
Input
↓
Case database
↓
Historical notes
↓
Representative records
↓
Authority records
↓
Communication history
↓
still missing
↓
mark fact as unresolved
```

### Acceptance Criteria

Every important fact must include:

```text
value
source
verification status
timestamp if available
```

---

## Phase 4 — Compliance Planner and Source Planner

### Goal

Decide what needs to be checked before searching evidence.

### Components

```text
compliance_planner
source_planner
```

### Compliance Plan

```json
{
  "decision_target": "DIRECT_CONTACT",
  "checks": [
    {"id":"C1","check":"representation_status"},
    {"id":"C2","check":"authority_status"},
    {"id":"C3","check":"direct_contact_restriction"},
    {"id":"C4","check":"direct_contact_exception"},
    {"id":"C5","check":"contact_purpose"}
  ]
}
```

### Source Plan

Sources must remain logically separated:

```text
LEGAL / REGULATORY
→ Can the action legally occur?

COMPANY POLICY
→ Does the organisation permit / require it?

SOP
→ If permitted, how should the work be performed?
```

### Acceptance Criteria

The planner must not treat SOP as the primary authority for the legal compliance decision.

---

## Phase 5 — Retrieval Query Generation and RAG Integration

### Goal

Translate compliance questions into efficient retrieval requests for the already-completed RAG Service.

### Components

```text
retrieval_query_generator
rag_client
```

### Key Pattern

```text
1 Compliance Question
       ↓
2–4 short retrieval queries
       ↓
Existing RAG Service
```

### Example

```json
{
  "question_id": "Q3",
  "original_question": "If the solicitor is an authorised representative, may the collector contact the customer directly?",
  "queries": [
    "represented debtor authorised representative direct contact",
    "debtor solicitor direct contact restriction",
    "represented debtor direct contact exceptions",
    "solicitor representative direct communication exceptions"
  ],
  "source_scope": [
    "regulatory_guidance",
    "company_policy"
  ],
  "filters": {
    "jurisdiction": "AU",
    "effective_only": true
  }
}
```

### RAG Adapter

```python
class RagClient:
    async def retrieve(
        self,
        *,
        target_type: str,
        content: str,
        jurisdiction: str,
        region: str,
        top_k: int
    ) -> list[dict]:
        ...
```

Example external call:

```text
POST /rag/evidence/retrieve
```

### Important

No implementation work should duplicate retrieval functionality already provided by RAG.

DipperWovenAgent owns:

```text
What should we search?
Why should we search it?
Which evidence belongs to which compliance question?
```

RAG owns:

```text
How is evidence retrieved?
```

---

## Phase 6 — Evidence Aggregation and Sufficiency Evaluation

### Goal

Transform retrieved material into evidence usable for a decision.

### Components

```text
evidence_aggregator
evidence_evaluator
```

### Evaluation

Evidence must be split into:

```text
Rule Evidence
+
Case Fact Evidence
```

### Output

```json
{
  "sufficient_for_final_decision": false,
  "rule_evidence_sufficient": true,
  "case_fact_evidence_sufficient": false,
  "missing": [
    "solicitor authority / representation status",
    "whether debtor requested no direct contact"
  ]
}
```

### Routing

```text
Evidence sufficient
        ↓
Compliance Service

Rule evidence insufficient
        ↓
HOLD / MANUAL REVIEW

Case fact insufficient
        ↓
HOLD_AND_VERIFY
```

### Acceptance Criteria

A retrieved rule must never automatically produce a compliance decision.

---

## Phase 7 — Compliance Service

### Goal

Make the compliance decision using verified case facts and evidence.

### Input

```text
Proposed Action
+
Verified Facts
+
Legal Evidence
+
Policy Evidence
```

### Decision Contract

```python
class ComplianceDecision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_CONDITIONS = "ALLOW_WITH_CONDITIONS"
    HOLD_AND_VERIFY = "HOLD_AND_VERIFY"
    BLOCK = "BLOCK"
```

### Example

```json
{
  "decision": "HOLD_AND_VERIFY",
  "risk_level": "HIGH",
  "reasoning_summary": "Representation is indicated but authority has not been verified.",
  "required_checks": [
    "Verify solicitor details",
    "Check authority",
    "Check whether customer requested no direct contact"
  ],
  "evidence_refs": [
    "evidence-001",
    "evidence-004"
  ]
}
```

### Design Rule

The Compliance Service answers:

```text
Can this proposed action proceed?
```

It does not execute the action.

### Acceptance Criteria

Every decision must be:

- explainable
- evidence-linked
- deterministic in output schema
- auditable
- incapable of directly changing case data

---

## Phase 8 — SOP Resolver and Action Planner

### Goal

Convert an approved or conditional compliance outcome into operational steps.

### Components

```text
sop_resolver
      ↓
action_planner
```

### Example Representative SOP

```text
1. Create representative record
2. Set Representative Type = Solicitor
3. Record solicitor details
4. Set Authority Status = Pending
5. Apply temporary Contact Hold
6. Create Verify Representative task
7. Send authority request where required
8. Review after response
```

### Action Plan

```json
{
  "recommended_actions": [
    {
      "action": "create_representative",
      "requires_confirmation": true
    },
    {
      "action": "apply_contact_hold",
      "requires_confirmation": true
    },
    {
      "action": "create_task",
      "task_type": "VERIFY_REPRESENTATIVE",
      "requires_confirmation": false
    }
  ]
}
```

### Design Rule

```text
Legal + Policy
→ Compliance Service
→ CAN WE DO IT?

SOP
→ Action Planner
→ HOW DO WE DO IT?
```

---

## Phase 9 — Human Approval / Automation Gate

### Goal

Prevent unsafe or unauthorised autonomous execution.

### Component

```text
approval_gate
```

### Initial Permission Model

Start conservatively:

| Action | Initial mode |
|---|---|
| Create internal verification task | Auto |
| Read case data | Auto |
| Generate recommendation | Auto |
| Add low-risk internal workflow item | Configurable |
| Create representative record | Human approval |
| Apply account/contact hold | Human approval |
| Send SMS/email | Human approval |
| Direct customer contact | Human approval + compliance gate |
| Legal / enforcement action | Human approval only |

Move actions from manual to automatic only after policy, audit and operational validation.

### Approval API

```http
POST /api/approvals/{approvalId}/approve
POST /api/approvals/{approvalId}/reject
```

---

## Phase 10 — Execution Agent and Business API Integration

### Goal

Execute approved actions safely through existing application services.

### Component

```text
execution_agent
       ↓
business_api_client
```

### Example APIs

```http
POST /api/representatives
POST /api/accounts/{id}/holds
POST /api/tasks
POST /api/messages
POST /api/workflows
```

### Critical Architecture Rule

```text
LLM
→ proposes structured action

Execution Agent
→ validates action

Business API
→ validates permissions + domain rules
→ performs transaction
→ returns result
```

The LLM never:

```text
writes directly to SQL
updates business tables directly
sends messages directly
bypasses application authorization
```

### Required Controls

- idempotency key
- action allow-list
- request validation
- business permission validation
- retry policy
- timeout
- failure handling
- partial execution tracking

---

## Phase 11 — Audit and Traceability

### Goal

Make every important decision reproducible and reviewable.

### Audit Record

Store:

```text
request ID
case ID
user ID
raw input
normalized input
detected events
detected facts
verified facts and sources
compliance questions
retrieval queries
RAG evidence IDs / citations
evidence sufficiency result
compliance decision
SOP selected
action plan
approval decision
execution requests
execution results
LLM/model version
prompt/version identifiers
timestamps
errors
```

### Suggested Audit Events

```text
AGENT_REQUEST_RECEIVED
EVENT_DETECTED
FACT_RESOLVED
COMPLIANCE_PLAN_CREATED
RAG_REQUESTED
EVIDENCE_EVALUATED
COMPLIANCE_DECIDED
ACTION_PLANNED
APPROVAL_REQUESTED
ACTION_APPROVED
ACTION_REJECTED
ACTION_EXECUTED
ACTION_FAILED
WORKFLOW_COMPLETED
```

---

# 7. Orchestration Graph

Recommended graph:

```text
START
  ↓
normalize_input
  ↓
detect_events
  ↓
decompose_questions
  ↓
check_information_sufficiency
  ↓
resolve_context
  ↓
plan_compliance_checks
  ↓
plan_sources
  ↓
generate_retrieval_queries
  ↓
retrieve_from_existing_rag
  ↓
aggregate_evidence
  ↓
evaluate_evidence
  ├────────────── missing evidence ──────────────┐
  │                                             │
  ▼                                             │
compliance_decision                             │
  │                                             │
  ├─ BLOCK ───────────────→ audit → END          │
  │                                             │
  ├─ HOLD_AND_VERIFY ─────→ action_plan ────────┤
  │                                             │
  └─ ALLOW / CONDITIONS                         │
          ↓                                     │
      resolve_sop                               │
          ↓                                     │
      action_plan                               │
          ↓                                     │
      approval_gate                             │
       /       \                                 │
   approved    rejected                         │
      ↓           ↓                             │
 execution      audit                           │
      ↓           ↓                             │
 execution_audit END                            │
      ↓                                         │
     END                                        │
```

---

# 8. API Contract for MVP

## Invoke Agent

```http
POST /api/agent/invoke
```

```json
{
  "case_id": "12345",
  "target_type": "note",
  "content": "Customer says his solicitor will manage the account. Collector plans to call the customer tomorrow for payment.",
  "jurisdiction": "AU",
  "region": "AU",
  "metadata": {}
}
```

### Response

```json
{
  "request_id": "req-123",
  "status": "AWAITING_APPROVAL",
  "events": [
    "POTENTIAL_REPRESENTATIVE",
    "PROPOSED_DIRECT_CONTACT"
  ],
  "verified_facts": {
    "representative_record_exists": false,
    "authority_verified": false
  },
  "compliance": {
    "decision": "HOLD_AND_VERIFY",
    "risk_level": "HIGH"
  },
  "recommended_actions": [
    {
      "action_id": "a1",
      "type": "CREATE_VERIFY_REPRESENTATIVE_TASK",
      "requires_confirmation": false
    },
    {
      "action_id": "a2",
      "type": "APPLY_CONTACT_HOLD",
      "requires_confirmation": true
    }
  ],
  "evidence": []
}
```

---

# 9. MVP Boundary

The first production-capable MVP should support one end-to-end domain extremely well instead of implementing every event immediately.

## MVP Event

```text
REPRESENTATIVE
+
PROPOSED_DIRECT_CONTACT
```

## MVP Workflow

```text
Collector Note
↓
Detect representative claim
↓
Detect proposed direct contact
↓
Resolve representative / authority records
↓
Generate representative compliance questions
↓
Generate short retrieval queries
↓
Call existing RAG
↓
Evaluate legal + policy evidence
↓
ALLOW / CONDITIONS / HOLD / BLOCK
↓
Resolve Representative SOP
↓
Recommend contact hold / verification task
↓
Human approval where required
↓
Call business APIs
↓
Audit
```

This validates the complete architecture before adding further event routes.

---

# 10. Expansion Order

After the Representative workflow is stable, add event packs in this order:

```text
1. REPRESENTATIVE / DIRECT CONTACT
2. HARDSHIP
3. VULNERABILITY
4. DISPUTE
5. COMPLAINT
6. BANKRUPTCY
7. DEBT_AGREEMENT
8. DECEASED
9. LEGAL_PROCEEDING
10. PAYMENT_ARRANGEMENT
```

Each event pack should contain:

```text
event definition
required facts
compliance questions
compliance checks
source requirements
query-generation examples
decision tests
SOP mapping
allowed actions
approval rules
workflow tests
```

---

# 11. Testing Plan

## Unit Tests

Test every node independently:

```text
event detector
question decomposer
sufficiency checker
fact resolvers
compliance planner
source planner
query generator
evidence evaluator
compliance service
SOP resolver
action planner
approval gate
execution mapper
```

## Contract Tests

Validate integration contracts with:

```text
RAG Service
Case APIs
Representative APIs
Authority APIs
Task API
Hold API
Messaging API
```

## Golden Workflow Tests

Maintain curated scenarios with expected outputs.

Example:

```text
Scenario:
Customer mentions solicitor.
No representative record exists.
Collector proposes payment call.

Expected:
POTENTIAL_REPRESENTATIVE detected
authority_verified = false
compliance decision = HOLD_AND_VERIFY
direct payment call must not be auto-executed
verification workflow recommended
```

## Safety Regression Tests

Must test:

- hallucinated facts are not marked verified
- missing facts do not become assumptions
- missing evidence does not become ALLOW
- RAG result is not copied directly into decision
- BLOCK never reaches execution
- rejected approval never reaches execution
- execution cannot call an unapproved API/action
- high-risk action cannot bypass gate

---

# 12. Observability

Track at least:

```text
request latency
LLM latency by node
RAG latency
number of retrieval queries
evidence count
evidence sufficiency rate
decision distribution
HOLD_AND_VERIFY rate
human approval rate
human rejection rate
execution success rate
workflow failure rate
token usage
LLM cost
```

Structured logs should use `request_id`, `case_id`, `workflow_id` and `action_id`.

---

# 13. Deployment Plan

Recommended initial deployment:

```text
Existing Application
       │
       ▼
DipperWovenAgent API
       │
       ├── Existing RAG Service
       ├── Existing Business APIs
       └── LLM Provider
```

Containerise DipperWovenAgent independently.

Required configuration:

```text
RAG_SERVICE_URL
BUSINESS_API_BASE_URL
LLM_PROVIDER
LLM_MODEL
DATABASE / AUDIT STORE
AUTH SETTINGS
LOG LEVEL
TIMEOUTS
FEATURE FLAGS
```

Do not couple the RAG deployment lifecycle to the DipperWovenAgent deployment lifecycle.

---

# 14. Suggested Delivery Milestones

## Milestone 1 — Agent Foundation

Deliver:

```text
service shell
state
graph
API
logging
RAG adapter
mock business API adapter
```

## Milestone 2 — Understanding Pipeline

Deliver:

```text
input normalization
event detection
question decomposition
schemas
tests
```

## Milestone 3 — Verified Fact Pipeline

Deliver:

```text
sufficiency checker
case context resolver
representative resolver
authority resolver
```

## Milestone 4 — Compliance Retrieval Planning

Deliver:

```text
compliance planner
source planner
multi-query generator
existing RAG integration
```

## Milestone 5 — Decision Engine

Deliver:

```text
evidence evaluator
compliance service
decision model
evidence-linked explanations
```

## Milestone 6 — Operational Workflow

Deliver:

```text
SOP resolver
action planner
approval gate
```

## Milestone 7 — Controlled Execution

Deliver:

```text
business API integration
execution agent
idempotency
audit
```

## Milestone 8 — Representative MVP Production Hardening

Deliver:

```text
golden test set
regression tests
security controls
observability
CI/CD
container deployment
production configuration
```

Only after Milestone 8 should additional event packs be added.

---

# 15. Recommended Implementation Priority

```text
P0
├─ Agent State
├─ Orchestration Graph
├─ Event Detector
├─ Question Decomposer
├─ Context Resolver
├─ RAG Client
├─ Evidence Evaluator
└─ Compliance Service

P1
├─ Compliance Planner
├─ Source Planner
├─ Retrieval Query Generator
├─ SOP Resolver
├─ Action Planner
└─ Approval Gate

P2
├─ Execution Agent
├─ Business API integrations
├─ Audit
├─ Observability
└─ workflow persistence / resume

P3
├─ additional event packs
├─ increased safe automation
└─ optimisation / model routing
```

---

# 16. Definition of Done for the First End-to-End Release

The first release of **DipperWovenAgent** is complete when the system can:

```text
1. Receive a collector note and proposed action.
2. Detect representative-related events.
3. Keep detected and verified facts separate.
4. Resolve representative and authority data from the case system.
5. Generate compliance questions.
6. Generate multiple retrieval queries for each relevant question.
7. Call the existing RAG Service.
8. Evaluate both rule evidence and case-fact evidence.
9. Return ALLOW / ALLOW_WITH_CONDITIONS / HOLD_AND_VERIFY / BLOCK.
10. Resolve the applicable SOP.
11. Produce a structured action plan.
12. Require approval for configured high-risk actions.
13. Execute approved actions only through Business APIs.
14. Persist a complete evidence-to-decision-to-action audit trail.
15. Pass representative/direct-contact golden workflow and safety regression tests.
```

---

# 17. Final Responsibility Boundary

```text
DipperWovenAgent — Before RAG
    Understand
    Detect
    Verify
    Plan
    Generate retrieval intent

Existing RAG Service
    Retrieve
    Filter
    Rank
    Return evidence + citations

DipperWovenAgent — After RAG
    Evaluate
    Decide
    Apply SOP
    Plan action
    Request approval
    Execute
    Audit

Business APIs
    Enforce permissions
    Enforce domain rules
    Perform transactions
```

This boundary allows the completed RAG Service to remain stable while **DipperWovenAgent** supplies the agentic reasoning, compliance control and business execution layers around it.
