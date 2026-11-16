# OWASP Top 10 for LLM Applications Reference

1. **LLM01: Prompt Injection**: Manipulating behavior via untrusted direct prompts or indirect document embeddings.
2. **LLM02: Sensitive Information Disclosure**: Leaking proprietary data, credentials, or PII.
3. **LLM03: Excessive Agency**: Over-permissioned agents executing destructive actions without approval.
4. **LLM04: Supply Chain Vulnerabilities**: Poisoned datasets, malicious third-party plugins, or compromised weights.
5. **LLM05: Data and Model Poisoning**: Manipulated training data or fine-tuning sets leading to backdoors.
6. **LLM06: Insecure Output Handling**: Blindly trusting LLM output in downstream HTML rendering or SQL execution.
7. **LLM07: System Prompt Leakage**: Exposing hidden system instructions.
8. **LLM08: Vector and Embedding Weaknesses**: Inversion attacks reconstructing source texts from vectors.
9. **LLM09: Misinformation & Hallucination**: Ungrounded generations damaging business trust.
10. **LLM10: Unbounded Consumption**: Denial of Service (DoS) through heavy token or tool loop consumption.
