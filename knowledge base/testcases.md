
### **Test Cases for ClaimSwift**

| #  | Prompt                                                                                                                                                    | Expected Outcome                                                          |
| -- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| 1  | I want to submit a claim for policy PB12345678, amount ₹20,000, incident date 2025-05-01, documents complete.                                             | Approved. Reference ID generated.                                         |
| 2  | I want to submit a claim for policy PB23456789, amount ₹60,000, incident date 2025-06-01, all documents submitted.                                        | Escalated (claim exceeds coverage). Reference ID generated.               |
| 3  | I want to submit a claim for policy PB34567890, amount ₹10,000, incident date 2024-05-01.                                                                 | Rejected (policy expired). Reference ID generated.                        |
| 4  | I want to submit a claim for policy PB12345678, amount ₹20,000, incident date 2025-05-01, missing FIR.                                                    | Escalated (missing documents, transfer to human). Reference ID generated. |
| 5  | I want to submit a claim for policy PB99999999, amount ₹10,000.                                                                                           | Rejected (policy not found). Reference ID generated.                      |
| 6  | I want to submit a claim for policy PB12345678, amount ₹45,000, incident date 2025-05-01, documents complete.                                             | Escalated (high claim amount). Reference ID generated.                    |
| 7  | I want to submit a claim for policy PB12345678, amount ₹20,000, incident date 2025-02-01, documents complete, but claim filed after 40 days.              | Escalated (late claim submission). Reference ID generated.                |
| 8  | I want to submit a claim for policy PB23456789, amount ₹70,000, incident date 2025-03-01, missing photos.                                                 | Escalated (missing documents). Reference ID generated.                    |
| 9  | I want to submit a claim for policy PB34567890, amount ₹90,000, incident date 2025-04-15, all documents, but invoice seems edited.                        | Escalated or Rejected (fraud risk detected). Reference ID generated.      |
| 10 | I want to submit a claim for policy PB12345678, amount ₹15,000, incident date 2025-05-01, duplicate photo from previous claim.                            | Escalated (suspicious duplicate image). Reference ID generated.           |
| 11 | I want to submit a claim for policy PB23456789, amount ₹10,000, incident date 2025-05-01, all documents, driver was drunk.                                | Rejected (exclusion: drunk driving). Reference ID generated.              |
| 12 | I want to submit a claim for policy PB12345678, amount ₹20,000, incident date 2025-05-01, vehicle used commercially but insured for private use.          | Rejected (policy exclusion). Reference ID generated.                      |
| 13 | I want to submit a claim for policy PB34567890, amount ₹25,000, incident date 2025-05-01, all documents complete, first claim.                            | Approved (low risk, documents valid). Reference ID generated.             |
| 14 | I want to submit a claim for policy PB12345678, amount ₹50,000, incident date 2025-05-01, all documents submitted.                                        | Escalated (claim > 80% sum insured). Reference ID generated.              |
| 15 | I want to submit a claim for policy PB23456789, amount ₹5,000, incident date 2025-05-01, documents incomplete, user asks questions about policy coverage. | Escalated (missing documents, human guidance). Reference ID generated.    |

---

These **15 cases cover all scenarios**:

* Valid claims → Approved
* High-risk or incomplete claims → Escalated
* Invalid/violating policies → Rejected
* Fraud detection triggers → Escalated/Rejected

