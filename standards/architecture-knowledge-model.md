# Architecture Knowledge Model

## Document Status
Draft

## Purpose
Define how architecture research is transformed into usable project guidance without copying source material directly into project architecture documents.

## Owner
Architecture Team

## Last Updated
2026-07-03

---

See [Glossary](../glossary.md) for definitions of key terms used in this document.

---

## 1. Intent

Architecture research should inform the repository, but it should not be pasted into the active client architecture workspace.

The repository should convert research into reusable judgment aids:

1. **Principles** — stable rules of architectural judgment.
2. **Practices** — repeatable behaviors used while creating or reviewing architecture.
3. **How-to Guides** — step-by-step guidance for common architecture tasks.
4. **Reference Frameworks** — named models, lenses, and decision structures used to reason about architecture.
5. **Selection Guidance** — decision support for choosing which architecture documents are needed for a given project.
6. **Project-Specific Documents** — actual source-truth architecture for the target system.

## 2. Knowledge Flow

```text
research sources
  ↓
distilled principles
  ↓
practices and how-to guidance
  ↓
reference frameworks
  ↓
architecture selection guidance
  ↓
project-specific architecture documents
```

The active architecture documents should contain project-specific facts, decisions, constraints, and diagrams. They should not contain generic book summaries or copied framework explanations.

## 3. Layer Definitions

| Layer | Purpose | Belongs In | Does Not Belong In |
|---|---|---|---|
| Research Sources | Raw or external source material used for learning and reference. | External Drive folders, citations, research notes. | Active architecture source-truth documents. |
| Principles | Durable rules that guide architecture judgment. | `standards/architecture-principles.md`. | Project-specific decision records unless the principle is being applied to a decision. |
| Practices | Repeatable activities used to create, review, or maintain architecture. | `standards/architecture-practices.md`. | Raw research summaries. |
| How-to Guides | Step-by-step instructions for executing architecture work. | `standards/how-to/`. | Final project architecture documents. |
| Reference Frameworks | Decision models and conceptual tools used to reason about architecture. | `standards/reference-frameworks.md`. | Directly copied framework chapters or vendor documentation. |
| Selection Guidance | Rules for deciding which architecture artifacts are needed. | `standards/architecture-document-selection.md`. | One-off project documents. |
| Project-Specific Documents | Source-truth architecture for the target system. | `architecture/`, `decisions/`, `governance/`, `glossary.md`. | Generic best-practice content. |

## 4. Research Distillation Rule

When using research, convert it into one of the following forms:

| Output Type | Use When | Expected Shape |
|---|---|---|
| Principle | The research identifies a durable architecture judgment. | A short rule with rationale and implications. |
| Practice | The research identifies a repeatable behavior. | A checklist, review activity, or operating habit. |
| How-to | The research supports a repeatable task. | Steps, inputs, outputs, and completion criteria. |
| Framework | The research provides a decision lens. | Model description, when to use, limits, and related project docs. |
| Selection Rule | The research helps decide which documents are needed. | Trigger conditions and required architecture artifacts. |
| Project Fact | The research is specific to the target system. | Must be sourced from project evidence, not generic reference material. |

## 5. Anti-Patterns

Avoid these patterns:

- copying book or article sections into active architecture documents;
- using generic architecture language where a project-specific decision is required;
- treating a framework as a required deliverable for every project;
- creating every possible architecture document regardless of project risk;
- filling project documents with best-practice explanations instead of source facts;
- allowing AI to turn reference material into invented project architecture.

## 6. Architecture Document Creation Rule

Architecture documents should be created or expanded because the project needs the clarity, not because a framework contains a matching diagram type.

Use the architecture clarity checklist to decide whether a document is needed:

- Does this artifact answer a question needed for implementation?
- Does it preserve a boundary that developers might otherwise break?
- Does it clarify ownership, data, integration, quality, security, deployment, or operational expectations?
- Does it record a material decision or unresolved risk?

If the answer is no, keep the concept in principles, practices, how-to guidance, or reference frameworks instead of creating a project-specific document.

## 7. Review Rule

Before adding research-derived content to the repository, identify its layer:

```text
source → principle / practice / how-to / framework / selection rule / project fact
```

If the layer is unclear, do not add it to active architecture documents. Capture it as a research note or open question until its use is clear.
