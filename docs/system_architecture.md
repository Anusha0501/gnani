                    ┌─────────────────────────┐
                    │        Streamlit UI      │
                    │  (User Claim Submission) │
                    └────────────┬────────────┘
                                 │
                                 ▼
                     ┌─────────────────────┐
                     │   CrewAI Orchestrator│
                     │(Multi-Agent Workflow)│
                     └─────────┬───────────┘
                               │
        ┌──────────────────────┼────────────────────────┐
        │                      │                        │
        ▼                      ▼                        ▼
┌────────────────┐   ┌─────────────────────┐   ┌──────────────────────────┐
│ ClaimIntakeAgent│   │DamageAssessmentAgent│   │ DecisionAgent            │
│ Validate Input  │   │ Severity + Cost     │   │ Final Approval Logic     │
└───────┬─────────┘   └──────────┬─────────┘   └────────┬────────────────┘
        │                        │                       │
        │                        │                       │
        │                        ▼                       │
        │           ┌──────────────────────┐             │
        │           │ MCP Tool Layer       │             │
        │           │  - Damage Scoring    │             │
        │           │  - Policy Lookup     │             │
        │           │  - Notifications     │             │
        │           └──────────┬───────────┘             │
        │                      │                         │
        │                      ▼                         │
        │         ┌─────────────────────────┐            │
        │         │ FraudDetectionADKAgent  │            │
        │         │ (ADK Risk Intelligence) │            │
        │         └──────────┬──────────────┘            │
        │                     │                           │
        └─────────────────────┴───────────────────────────┘
                              │
                              ▼
                      ┌────────────────┐
                      │ Decision Output│
                      │ JSON + UI View │
                      └────────────────┘
