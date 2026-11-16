# Requirements Analysis & Prioritization Models Reference

## 1. Prioritization Frameworks (SE Curriculum Chapter 4)

### MoSCoW Prioritization
- **Must Have**: Critical system functionality. Omission renders the system non-viable.
- **Should Have**: Important capabilities, but temporary manual or operational workarounds exist.
- **Could Have**: Desirable features with low business risk if deferred to subsequent releases.
- **Won't Have**: Explicitly out-of-scope for the current cycle to protect the appetite boundary.

### Kano Customer Satisfaction Model
- **Must-Be Qualities (Basic Needs)**: Expected by default (e.g. login security, database persistence). Their absence creates severe dissatisfaction, but their presence does not delight.
- **One-Dimensional (Performance Needs)**: Satisfaction is linear with performance (e.g. query speed, search throughput).
- **Attractive Qualities (Delighters)**: Unexpected innovations that create high satisfaction without causing dissatisfaction if missing.

---

## 2. Attack Tree Modeling for Security Requirements (SE Curriculum Chapter 3 & 11)

An **Attack Tree** decomposes an attacker's overarching objective into component sub-attacks via AND / OR branch logic:

```
                      [Exfiltrate User DB] (Root Goal)
                                  |
               +------------------+------------------+
               | (OR)                                | (OR)
     [SQL Injection]                      [Stolen Cloud Credential]
           |                                         |
     +-----+-----+                             +-----+-----+
     | (AND)     | (AND)                       | (OR)      | (OR)
[Bypass WAF] [Blind SQL Payload]         [Phish Admin] [GitHub Leak]
```

Each leaf node maps directly to a proactive mitigation requirement in the product backlog.
