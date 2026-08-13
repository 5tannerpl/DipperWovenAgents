# Debt Collection Agent: Compliance-first Agentic RAG Architecture (Revised Final Version)

## 1. Core Objective

Typical input:

> Client said he has a solicitor to deal with his debt. I am planning to
> call client tomorrow ask for pay the debt.

The system does not send the raw note directly to RAG to decide whether
contact is allowed. It follows the responsibility chain below:

``` text
UNDERSTAND
  ↓
DETECT EVENTS
  ↓
DECOMPOSE COMPLIANCE QUESTIONS
  ↓
VERIFY FACTS
  ↓
PLAN COMPLIANCE CHECKS
  ↓
PLAN SOURCES
  ↓
GENERATE MULTIPLE RETRIEVAL QUERIES
  ↓
RAG RETRIEVAL
  ↓
FUSE + RERANK
  ↓
EVALUATE EVIDENCE
  ↓
COMPLIANCE DECISION
  ↓
APPLY SOP
  ↓
PLAN ACTIONS
  ↓
HUMAN APPROVAL / AUTO GATE
  ↓
EXECUTE THROUGH BUSINESS APIs
  ↓
AUDIT RESULT
```

Core principles:

-   Detected Fact ≠ Verified Fact
-   Compliance Question ≠ Retrieval Query
-   Retrieved Rule ≠ Compliance Decision
-   Knowledge Missing ≠ Case Fact Missing
-   Legal / Policy primarily answer "Can we do it?"
-   SOP primarily answers "How should we do it?"
-   Agent / Workflow Execution performs the actual business action
-   High-risk actions support Human-in-the-loop approval

## 2. Complete Architecture

``` text
Collector Note / Proposed Action
        ↓
① Input / Event Understanding
   ├─ Facts
   ├─ Intended Actions
   ├─ Event Types
   └─ Entities
        ↓
② Compliance Question Decomposer
   └─ Q1 / Q2 / Q3 / ...
        ↓
③ Information Sufficiency Checker
        ↓
④ Context / Fact Resolver
   ├─ Case DB
   ├─ Notes
   ├─ Representative Records
   ├─ Authority Records
   └─ Communication History
        ↓
⑤ Compliance Planner
        ↓
⑥ Source Planner
   ├─ Legal / Regulatory
   ├─ Company Policy
   └─ SOP
        ↓
⑦ Retrieval Query Generator
   └─ Generate 2–4 short queries per question
        ↓
⑧ Multi-Query Hybrid Retriever
   ├─ Vector Search
   ├─ BM25 / Keyword Search
   └─ Metadata Filters
        ↓
⑨ Evidence Fusion & Reranker
   ├─ Merge
   ├─ Deduplicate
   └─ Final rerank using the original Compliance Question
        ↓
⑩ Evidence Sufficiency Evaluator
        ↓
⑪ Compliance Service
   ├─ ALLOW
   ├─ ALLOW_WITH_CONDITIONS
   ├─ HOLD_AND_VERIFY
   └─ BLOCK
        ↓
⑫ Next Best Action / Action Planner
        ↓
⑬ Human Approval / Automation Gate
        ↓
⑭ Agent / Workflow Execution
        ↓
⑮ Audit / Execution Result
```

## 3. Input / Event Understanding

The first LLM only understands and structures the input; it does not
make the final compliance decision.

``` json
{
  "facts": [{
    "type": "representative_claim",
    "value": "Customer stated a solicitor is dealing with the debt",
    "verification_status": "unverified"
  }],
  "intended_actions": [{
    "action": "call_customer",
    "when": "tomorrow",
    "purpose": "request_payment"
  }],
  "detected_events": [
    "POTENTIAL_REPRESENTATIVE",
    "PROPOSED_DIRECT_CONTACT"
  ]
}
```

Critical distinction:

``` text
Customer says a solicitor exists
            ≠
Verified authorised representative
```

## 4. Compliance Question Decomposer

Decompose the note from a debt-collection compliance perspective:

``` json
{
  "questions": [
    {"id":"Q1","topic":"representative_status","question":"Does the customer's statement establish or indicate that an authorised solicitor is representing the customer in relation to this debt?"},
    {"id":"Q2","topic":"authority","question":"What evidence or authority is required to treat the solicitor as an authorised representative?"},
    {"id":"Q3","topic":"direct_contact","question":"If the solicitor is an authorised representative, may the collector contact the customer directly?"},
    {"id":"Q4","topic":"contact_exception","question":"Do any exceptions permit direct contact with the customer despite representation?"},
    {"id":"Q5","topic":"payment_request","question":"If direct contact is permitted, may the collector call for the purpose of requesting payment?"},
    {"id":"Q6","topic":"privacy","question":"What information may be disclosed to the solicitor and what authority is required before disclosure?"}
  ]
}
```

These are reasoning-oriented Compliance Questions, not direct
search-engine queries.

## 5. Information Sufficiency + Context Resolver

Determine whether the current case facts are sufficient:

``` json
{
  "sufficient": false,
  "missing_facts": [
    "Solicitor identity and contact details",
    "Whether the solicitor acts for this debt",
    "Whether the customer requested no direct contact",
    "Whether authority has been received or recorded",
    "Scope and currency of authority"
  ]
}
```

Do not immediately ask the collector; first resolve missing facts from
internal systems:

``` python
get_case(case_id)
get_recent_notes(case_id)
get_representatives(case_id)
get_authorities(case_id)
get_communications(case_id)
```

Produce Verified Facts:

``` json
{
  "customer_claimed_solicitor": true,
  "representative_record_exists": false,
  "authority_verified": false,
  "no_direct_contact_instruction": null
}
```

## 6. Compliance Planner

Generate a Compliance Plan rather than a simple Search Plan:

``` json
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

## 7. Source Planner: Legal / Policy / SOP

``` text
Legal / Regulatory
→ What do law and regulatory rules allow or prohibit?

Company Policy
→ What does the company require internally?

SOP (Standard Operating Procedure)
→ What exactly should the employee or system do?
```

例如 Representative SOP：

``` text
1. Create representative record
2. Set Representative Type = Solicitor
3. Record solicitor details
4. Set Authority Status = Pending
5. Apply temporary Contact Hold
6. Create Verify Representative task
7. Send authority request where required
8. Review after response
```

Responsibility boundary:

``` text
Legal + Policy
      ↓
Compliance Service
      ↓
"Can we do it?"

SOP
      ↓
Action Planner / Workflow
      ↓
"How should we do it?"
```

## 8. Retrieval Query Generator: Key Revision

Do not use:

``` text
一个 Compliance Question
→ 一个长自然语言 Query
→ 一次 Search
```

Use instead:

``` text
一个 Compliance Question
→ 2–4 个短 Retrieval Queries
→ 多次 Search
→ Candidate Fusion
→ Final rerank using the original Compliance Question
```

Q3 example:

``` json
{
  "question_id": "Q3",
  "original_question": "If the solicitor is an authorised representative, may the collector contact the customer directly?",
  "topic": "represented_debtor_direct_contact",
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

Principle:

``` text
Short Retrieval Query → improve recall
Full Compliance Question → final rerank to improve precision
```

## 9. Multi-Query Retrieval + Evidence Fusion

``` text
Q3-A → Existing RAG → Top N ─┐
Q3-B → Existing RAG → Top N ─┤
Q3-C → Existing RAG → Top N ─┤
Q3-D → Existing RAG → Top N ─┘
                              ↓
                       Candidate Pool
                              ↓
                         Deduplicate
                              ↓
                       Final Reranker
                              ↑
                    Original Q3 Question
                              ↓
                       Final Top K
```

Pseudocode:

``` python
all_candidates = []

for query in retrieval_request.queries:
    candidates = await rag.retrieve(
        content=query,
        jurisdiction="AU",
        top_k=10
    )
    all_candidates.extend(candidates)

candidates = deduplicate(all_candidates)

results = await reranker.rerank(
    question=retrieval_request.original_question,
    candidates=candidates,
    top_k=5
)
```

The existing RAG Service can retain its Hybrid Search, metadata filters,
reranking, evidence, and citation core.

## 10. Evidence Sufficiency Evaluator

Evaluate separately:

``` text
Rule Evidence
+
Case Fact Evidence
```

Example:

``` json
{
  "sufficient_for_final_decision": false,
  "rule_evidence_sufficient": true,
  "case_fact_evidence_sufficient": false,
  "missing": [
    "whether debtor requested no direct contact",
    "solicitor authority / representation status"
  ]
}
```

Core principle:

``` text
Rule Found ≠ Decision Can Be Made
```

## 11. Compliance Service

Inputs:

``` text
Verified Facts
+
Legal Evidence
+
Policy Evidence
+
Proposed Action
```

示例：

``` python
await compliance_service.evaluate(
    target_type="proposed_action",
    content={
        "action": "call_customer",
        "purpose": "request_payment",
        "when": "tomorrow"
    },
    verified_facts=state["verified_facts"],
    legal_evidence=state["legal_evidence"],
    policy_evidence=state["policy_evidence"],
    topics=["representative", "direct_contact", "authority"]
)
```

Decision Model：

``` text
ALLOW
ALLOW_WITH_CONDITIONS
HOLD_AND_VERIFY
BLOCK
```

This example may produce:

``` json
{
  "decision": "HOLD_AND_VERIFY",
  "risk_level": "HIGH",
  "required_checks": [
    "Verify solicitor details",
    "Check authority",
    "Check whether customer requested no direct contact"
  ]
}
```

## 12. SOP → Action Planner → Execution

This is the other important revision.

SOP is not merely reference material for the collector; it can drive
downstream automation:

``` text
Compliance Decision
      ↓
Applicable SOP
      ↓
Action Planner
      ↓
Recommended Actions
      ↓
Approval / Automation Gate
      ↓
Execution Agent
      ↓
Business APIs
```

Example:

``` json
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

## 13. Human-in-the-loop / Auto Execution

``` text
Action Plan
    ↓
Risk / Permission Gate
   /                 Human Approval       Safe Auto Action
   ↓                     ↓
Confirm               Execute
   └──────────┬──────────┘
              ↓
         Business API
```

Example:

-   Create internal task → may be automated
-   Update non-sensitive internal status → may be automated under policy
-   Send SMS / Email → may require confirmation
-   Contact customer → high risk; pass through Compliance Gate
-   Legal / enforcement action → Human Approval

Exact permissions are determined by Company Policy, risk controls, and
system authorisation.

## 14. Execution Layer

The LLM does not directly modify the database.

``` text
Action Planner
      ↓
Execution Agent
      ↓
Business APIs
      ├─ POST /api/representatives
      ├─ POST /api/accounts/{id}/holds
      ├─ POST /api/tasks
      ├─ POST /api/messages
      └─ POST /api/workflows
      ↓
Database / External Services
```

Responsibilities:

``` text
LLM
→ 决定需要哪些业务动作

Business Service / API
→ 验证参数、权限、业务规则并执行
```

## 15. Event Sub-routing

Possible detected events:

``` text
REPRESENTATIVE
BANKRUPTCY
DEBT_AGREEMENT
HARDSHIP
VULNERABILITY
DISPUTE
COMPLAINT
DECEASED
LEGAL_PROCEEDING
PAYMENT_ARRANGEMENT
PROPOSED_DIRECT_CONTACT
```

Complete pattern:

``` text
Event
  ↓
Required Questions / Checks
  ↓
Required Facts
  ↓
Required Sources
  ↓
Multi-Query RAG
  ↓
Evidence
  ↓
Compliance Decision
  ↓
SOP
  ↓
Action Plan
  ↓
Execution
```

## 16. Recommended Service Boundaries

``` text
collection-agent/
├── understanding/
│   ├── event_detector.py
│   ├── query_decomposer.py
│   └── sufficiency_checker.py
├── context/
│   ├── case_context_resolver.py
│   ├── representative_resolver.py
│   └── authority_resolver.py
├── planning/
│   ├── compliance_planner.py
│   ├── source_planner.py
│   └── retrieval_query_generator.py
├── evidence/
│   ├── multi_query_retriever.py
│   ├── evidence_fusion.py
│   ├── final_reranker.py
│   └── evidence_evaluator.py
├── compliance/
│   └── compliance_service.py
├── action/
│   ├── action_planner.py
│   ├── approval_gate.py
│   └── execution_agent.py
└── audit/
    └── execution_audit.py
```

With an existing independent RAG Service:

``` text
Collection Agent / Orchestrator
   ├─ Event Detection
   ├─ Compliance Questions
   ├─ Fact Resolution
   ├─ Compliance Planning
   └─ Retrieval Query Generation
             ↓
       Existing RAG Service
   ├─ Hybrid Retrieval
   ├─ Metadata Filters
   ├─ Reranking
   └─ Evidence / Citation
             ↓
     Evidence Fusion / Evaluator
             ↓
       Compliance Service
             ↓
        Action Planner
             ↓
         SOP Execution
             ↓
    Business APIs / Workflow
```

The existing RAG Service therefore does not need to be rewritten for the
agentic architecture. Most agentic capability is added before RAG
through planning and after RAG through evaluation, decision, and
execution.

## 17. Final Responsibilities of the Three Evidence Types

  -----------------------------------------------------------------------
  Evidence                Primary question        Primary consumer
  ----------------------- ----------------------- -----------------------
  Legal / Regulatory      What does               Compliance Service
                          law/regulation allow or 
                          prohibit?               

  Company Policy          What does the company   Compliance Service
                          allow, require, or      
                          restrict?               

  SOP                     How should the          Action Planner /
                          employee/system perform Workflow
                          the work?               
  -----------------------------------------------------------------------

Finally:

``` text
Legal + Policy
      ↓
Compliance Decision
      ↓
Can / Cannot / Conditions

SOP
      ↓
Action Plan
      ↓
How to Execute
```

This creates an auditable, testable, extensible enterprise
debt-collection Compliance-first Agentic RAG system that can evolve from
Copilot assistance into controlled agentic automation.
