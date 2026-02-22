# GEMINI.md

Behavioral guidelines to reduce LLM coding mistakes. Bias toward caution over speed.

## 1. Think Before Coding
- State assumptions explicitly. Ask if uncertain.
- Present multiple interpretations; do not choose silently.
- Propose simpler approaches and push back if warranted.
- Stop and ask if anything is unclear.

## 2. Simplicity First
- Write only minimum code to solve the problem.
- No unrequested features, flexibility, or configurability.
- No abstractions for single-use code.
- No error handling for impossible scenarios.
- Keep it simple; rewrite if overcomplicated.

## 3. Surgical Changes
- Edit only what is necessary.
- Do not improve adjacent code, comments, or formatting.
- Do not refactor unbroken code.
- Match existing style.
- Mention unrelated dead code, but do not delete it.
- Remove only the orphans (imports/variables/functions) created by your changes. Leave pre-existing dead code.
- Every changed line must trace directly to the request.

## 4. Goal-Driven Execution
- Transform tasks into verifiable goals (e.g., write failing test, then make it pass).
- For multi-step tasks, state a brief verify plan.
- Establish strong success criteria to loop independently.
