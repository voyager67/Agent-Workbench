# Sources, attribution, and skill mapping

Agent Workbench is an independently authored collection of workflows informed by public skill libraries and agent projects. **No third-party `SKILL.md`, script, template, or agent configuration file is copied into this release.** Source relationships below describe workflow inspiration and selection, not copied source files or endorsement.

The `sources.json` file is the machine-readable mapping from each shipped skill to its upstream influences. Every shipped skill is mapped to one or more source IDs or explicitly marked original. A mapped skill's text is newly written for Agent Workbench; it may combine multiple workflow ideas and intentionally changes their boundaries to avoid duplicate skills.

## Source-to-skill map

| Upstream project | License/status checked | Upstream examples or patterns reviewed | Agent Workbench mapping |
|---|---|---|---|
| [t3dotgg/tstack](https://github.com/t3dotgg/tstack) | MIT | `full-send`, `full-stop`, `council`, `sol-loop`, `file-pr`, `takeover`, `babysit-pr`, `modernize`, `leaving-pr-comments` | `pr-lifecycle` combines the overlapping full-send/full-stop paths; `multi-model-review` consolidates council/sol-loop; `file-pr`, `take-over`, `babysit-pr`, `modernize-pr`, `pr-comment-writing` |
| [obra/superpowers](https://github.com/obra/superpowers) | MIT | `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `requesting-code-review`, `receiving-code-review`, `using-git-worktrees`, `subagent-driven-development`, `writing-skills`, branch completion | `design-interview`, `implementation-planning`, `test-driven-development`, `systematic-debugging`, `code-review`, `receiving-code-review`, `refactor-safely`, `verification-before-completion`, `using-git-worktrees`, `subagent-driven-development`, `skill-authoring`, plus Git lifecycle patterns |
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | `grill-me`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `improve-codebase-architecture`, `triage`, `handoff`, `teach` | `design-interview`, `spec-writing`, `implementation-planning`, `ticket-breakdown`, `issue-triage`, `architecture-review`, `handoff`, `decision-brief`, `meeting-to-actions` |
| [anthropics/skills](https://github.com/anthropics/skills) | Mixed repository; many example skills are Apache-2.0, while document-skill folders have separate terms. Check each skill/folder before reuse. | `mcp-builder`, `webapp-testing`, `skill-creator`, Agent Skills metadata, progressive disclosure | `mcp-server-development`, `web-app-testing`, `skill-authoring`; all independently written, no Anthropic skill file or script redistributed |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | MIT | Four themes: think before coding, simplicity first, surgical changes, goal-driven execution | `engineering-principles`; consolidated into one repository-wide engineering bar |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | MIT | `react-best-practices`, `web-design-guidelines`, `writing-guidelines` | `frontend-performance-review`, `ui-accessibility-review`, `documentation-sync`, `technical-writing` |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | MIT | Supabase/Postgres best-practice guidance, especially schema, query, security, and performance review | `database-review` (generalized into portable relational-database review; no Supabase-specific code copied) |
| [wshobson/agents](https://github.com/wshobson/agents) | MIT | Specialist agent/skill patterns for Python, backend, testing, security, API design, LLM systems, and agent teams | `architecture-review`, `python-engineering`, `api-design-review`, `subagent-driven-development`, `multi-model-review`, and the portable role-card layout |
| [ai4s-research/ai4s-skills](https://github.com/ai4s-research/ai4s-skills) | MIT at repository level; check individual skill metadata before copying files | Research exploration, literature survey, experiment suite, paper writing, integrity audit | `research-question-framing`, `literature-search`, `literature-synthesis`, `experiment-design`, `reproducible-ml-experiments`, `dataset-audit`, `research-integrity-audit`, `research-writing` |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | MIT at repository level; individual skill licenses may differ | Scientific databases, packages, computational biology/chemistry/medicine and ML workflows | Research and scientific-computing discovery informing `paper-reading`, `data-analysis`, and research workflows |
| [NVIDIA SkillEvaluator](https://docs.nvidia.com/skills/skillevaluator) | Evaluator docs describe an experimental product; check implementation license before reuse | Deterministic checks, overlap detection, evaluation-case generation, live agent evaluation | `skill-evaluation` and the validation approach; no NVIDIA code is included |

## Independently authored workflow

| Skill | Provenance |
|---|---|
| `web-research` | Written specifically for Agent Workbench as a general current-information workflow. It uses standard source-verification practices and is not adapted from a third-party skill file. |

## Reviewed as discovery sources, not reused in shipped instructions

| Project | License / reuse note | Why it is useful |
|---|---|---|
| [Trail of Bits skills](https://github.com/trailofbits/skills) | CC BY-SA 4.0. No content copied; assess share-alike and attribution requirements before adapting any skill. | Strong specialist security research, vulnerability detection, and audit workflows. |
| [Microsoft skills](https://github.com/microsoft/skills) | MIT repository license; currently marked work in progress and focused on Azure SDKs / Foundry. | Examples of specialist agent roles, SDK guidance, and skill evaluation. |
| [GitHub awesome-copilot](https://github.com/github/awesome-copilot) | Check repository and each item before reuse. This is a community catalog with varied contributions. | Broad collection of agent skills, prompts, custom instructions, and reusable workflows. |
| [research-paper-lifecycle-skills](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills) | Apache-2.0; if redistributing substantial portions, retain upstream LICENSE and NOTICE. No files copied. | Focused lifecycle coverage from literature search through submission, rebuttal, and presentation. |
| [Jason-Mar1/awesome-academic-research-skills](https://github.com/Jason-Mar1/awesome-academic-research-skills) | Discovery index; linked projects retain individual licenses. | Workflow-first map of academic research tools, skills, and discipline packs. |
| [O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills) | CC0-1.0 for the index; linked repositories retain their own terms. | Research lifecycle index that records license and capability disclosures. |
| [openai/skills](https://github.com/openai/skills) | Individual skills have `LICENSE.txt`; the repository README currently marks the catalog deprecated. | Historical Codex catalog only; not treated as the current source of Codex guidance. |

## Licensing and attribution policy

- The root MIT license applies to original Agent Workbench material in this release.
- Upstream license labels describe the upstream repository as reviewed on 2026-11-07; repository-level terms do not automatically apply to every file in a mixed-license collection.
- No upstream files are redistributed here, so upstream license texts are not bundled as if they governed our files.
- Before adding any copied or substantially modified upstream file, inspect its exact path, author, license metadata, root license, notices, and any third-party assets. Preserve all required copyright, attribution, Apache NOTICE, and share-alike terms.
- Workflow inspiration is not a claim that the upstream project endorses Agent Workbench. The machine-readable mapping is intended to make provenance auditable, not to imply official partnership.
