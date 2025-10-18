                         ┌───────────────────────────────┐
                         │     Policyholder/User         │
                         │  (Submits claim request)      │
                         └──────────────┬────────────────┘
                                        │
                                        ▼
                      ┌────────────────────────────────────────┐
                      │ Claim Intake Agent (Agentic AI #1)     │
                      │ • Extracts user data (OCR, NLP)        │
                      │ • Captures images, documents, voice    │
                      │ • Verifies completeness of claim        │
                      └─────────────────┬──────────────────────┘
                                        │
                                        ▼
                  ┌────────────────────────────────────────────┐
                  │ Validation & Risk Assessment Agent (#2)    │
                  │ • Cross-verifies with policy DB/API        │
                  │ • Uses ML model for risk & fraud scoring   │
                  │ • Flags anomalies for human review         │
                  └──────────────────┬─────────────────────────┘
                                     │
                                     ▼
               ┌──────────────────────────────────────────────┐
               │ Damage Estimation Agent (#3)                 │
               │ • Uses Vision AI (YOLO/Mask R-CNN) on photos │
               │ • Predicts damage cost estimate              │
               │ • Matches parts/labor rates from database    │
               └───────────────────┬──────────────────────────┘
                                   │
                                   ▼
           ┌──────────────────────────────────────────────────────┐
           │ Claim Decision Agent (#4)                            │
           │ • Aggregates previous agent outputs                  │
           │ • Applies insurer rules / policy coverage logic      │
           │ • Generates claim summary & recommended decision     │
           └─────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
      ┌────────────────────────────────────────────────────────────┐
      │ Human-in-the-loop Reviewer (Insurance Officer)             │
      │ • Reviews flagged or high-value claims                     │
      │ • Confirms or edits decision output                        │
      │ • Sends feedback to model (continuous improvement)         │
      └────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
         ┌─────────────────────────────────────────────────────┐
         │ Settlement & Notification Agent (#5)                │
         │ • Initiates approved settlements via payment API    │
         │ • Sends user confirmation, report & analytics        │
         │ • Updates claim history dashboard                   │
         └─────────────────────────────────────────────────────┘
