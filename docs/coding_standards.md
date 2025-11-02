# Mandatory Coding Standards

## 1. Directive

This document defines the mandatory coding standards for this project. All code, without exception, must adhere to these rules. This is the definitive guide on how to write code for this repository.

---

## 2. Core Principles (Non-Negotiable)

- **Principle 1: Simplicity is Mandatory (KISS)**

  - **Rule:** All solutions must be simple and avoid unnecessary complexity. If a simpler solution exists, it must be chosen.

- **Principle 2: Design Before Code**

  - **Rule:** A structured design process must be followed before any implementation. The required sequence is:
    1.  **Words:** Define the objective and constraints.
    2.  **Diagrams:** Visualize the architecture and data flow.
    3.  **Code:** Implement the solution based on the approved design.

- **Principle 3: Pragmatism Over Trends**

  - **Rule:** Use proven, stable technologies appropriate for the task. Do not introduce new or complex technologies unless explicitly required and justified.

- **Principle 4: Understand Your Tools**
  - **Rule:** You must understand the underlying mechanisms of the tools you use, not just their surface-level APIs. This is critical for creating robust solutions.

---

## 3. The Development Workflow

All development must follow this five-step process:

1.  **Purpose:** Define the "why" with absolute clarity.
2.  **Structure:** Define the required outcomes and components.
3.  **Technology:** Select the correct tools based on the principles above.
4.  **Implementation:** Build a minimal, functional version that meets the purpose.
5.  **Refinement:** Test, verify, and then improve the implementation.

---

## 4. Strict Coding Rules

These rules are absolute and must be followed in all code contributions.

### 4.1. Naming Conventions

- **File Naming:** Files must be descriptively named to declare their exact purpose (e.g., `user_authentication_service.py`, not `auth.py`).
- **Variable & Function Naming:** Names must clearly state their purpose. Abbreviations are forbidden.

### 4.2. Modularity Rules

- **Single Responsibility Principle (SRP):** One file must have one, and only one, purpose. One function must perform one, and only one, action.
- **Function Length:** Functions must be concise and focused. The strict maximum length for any function is 50 lines.
- **File Length:** Files must not exceed a strict maximum of 200 lines. This is to ensure readability and maintain a single, clear focus.

### 4.3. Code Clarity Rules

- **Self-Documenting Code:** Code must be written to be immediately understandable without requiring comments.
- **"Boring" Code is a Requirement:** Clever, complex, or obscure code is forbidden. All code must be straightforward, predictable, and easy to follow.
- **Meaningful Comments:** Comments are to be used only to explain the "why" (the strategic reason for a design choice), never the "what" (what the code is doing).
- **Fail Loudly:** Errors must be handled explicitly. Never silence or ignore exceptions.
