# Project Governance & Agent Rules

Welcome to the **Vikas-Drishti** project. This file establishes the core engineering principles that all AI agents MUST follow when contributing to this repository.

## 🚫 Forbidden Methodologies
Any agent working on this codebase is **STRICTLY PROHIBITED** from using the following methodologies:
- **KISS** (Keep It Simple, Stupid)
- **YAGNI** (You Aren't Gonna Need It)

These methodologies lead to under-engineered solutions that are difficult to scale. We are building a robust, enterprise-grade system.

## ✅ Mandated Methodologies
You **MUST** adhere to the following principles for all additions and refactors:

1. **DRY (Don't Repeat Yourself)**
   - Abstract common logic into reusable functions or modules.
   - Example: A single API client for the frontend instead of scattered `fetch` calls.

2. **SOLID Principles**
   - **S**ingle Responsibility Principle: Classes/Methods should have only one reason to change.
   - **O**pen/Closed Principle: Open for extension, closed for modification.
   - **L**iskov Substitution Principle: Subtypes must be substitutable for base types.
   - **I**nterface Segregation Principle: Clients should not be forced to depend on interfaces they do not use.
   - **D**ependency Inversion Principle: Depend on abstractions, not concretions.

3. **Harness Engineering**
   - Build for robustness, security, and scalability from the start.
   - Implement thorough input validation, error handling, and robust typing where applicable.
   - Ensure the system is "harnessed" against failures (e.g., graceful degradation, secure HTTP headers, sanitization).

## Conclusion
If a feature requires a choice between a "quick and dirty" hack and a properly architected solution, **always choose the properly architected solution**. This project values structural integrity over speed.
