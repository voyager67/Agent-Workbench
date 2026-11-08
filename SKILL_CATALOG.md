# Additional agent-skill and agent collections

This catalog records useful public projects discovered while curating Agent Workbench. It is a starting point for further exploration, **not a quality ranking or blanket recommendation to install everything**. Skill repositories can execute scripts, access networks, read local files, or use hooks; inspect each selected skill and its permissions before use.

## Everyday coding and engineering

| Project | Best starting point | Why explore it | Important caveat |
|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | Brainstorming, planning, TDD, debugging, review, worktrees, branch completion | A coherent software-development methodology with complementary skills and a skill-authoring guide. | Workflow methodology is more prescriptive than a loose skill library; select components intentionally. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `grill-me`, `to-spec`, `to-tickets`, `implement`, `improve-codebase-architecture`, `handoff`, `triage` | Small, composable skills spanning engineering and productivity. | Some skills are user-invoked orchestration and may assume a configured issue tracker or project conventions. |
| [t3dotgg/tstack](https://github.com/t3dotgg/tstack) | PR lifecycle, independent model review, takeover, PR monitoring | Focused everyday PR operations for Claude Code and Codex. | Some workflows expect authenticated GitHub CLI or multi-provider/subagent support; inspect integration requirements. |
| [anthropics/skills](https://github.com/anthropics/skills) | Development/technical examples including MCP builder and web-app testing, plus skill templates | Official public examples of portable skills, bundled resources, and richer workflows. | Mixed repository; many skills are Apache-2.0, but check each folder. Some document skills have separate implementation and runtime considerations. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | React best practices, web design guidelines, writing guidelines, Vercel deploy | Strong frontend-specific review and implementation guidance. | Framework and platform-specific; use only when the stack matches. |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | Supabase and Postgres best practices | Current product guidance for Supabase database, auth, RLS, and related products. | Specialized to Supabase; the documentation/changelog lookup is an advantage but depends on current docs/network access. |
| [wshobson/agents](https://github.com/wshobson/agents) | Python/JS development, testing, security, architecture, LLM apps, agent teams | Large MIT-licensed multi-harness library with skills, agents, and plugins. | Very broad. Install narrow components; not every feature maps equally across every host. |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | Agent skills, custom agents, repository onboarding | Large community collection of Copilot-ready instructions and skills. | Community contributions vary; verify license, maintenance, scripts, and host-specific assumptions per item. |
| [microsoft/skills](https://github.com/microsoft/skills) | Azure SDK, Microsoft Foundry, backend/frontend/planner agents | Examples of specialist roles and SDK-grounded workflows. | Marked work in progress and concentrated on Microsoft/Azure technology. |

## Security and systems

| Project | Best starting point | Why explore it | Important caveat |
|---|---|---|---|
| [trailofbits/skills](https://github.com/trailofbits/skills) | Vulnerability discovery, smart-contract/security analysis, audit workflows | Specialist security research workflows from a security engineering firm. | CC BY-SA 4.0; not copied here. Read the license and inspect each tool/script before adapting. |

## Research, science, and ML experimentation

| Project | Best starting point | Why explore it | Important caveat |
|---|---|---|---|
| [ai4s-research/ai4s-skills](https://github.com/ai4s-research/ai4s-skills) | Research exploration, literature survey, experiment suite, paper writing, integrity audit | Compact research lifecycle pipeline with emphasis on citation and result provenance. | Its example outputs and citation counts are project-specific goals, not guaranteed outcomes. Validate all evidence and methods independently. |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Scientific databases, Python packages, biology/chemistry/medicine workflows | Large computational science library across many scientific packages and databases. | Very broad; repository-level MIT does not mean every skill is MIT. Check each skill's license metadata and data/API terms. |
| [ShaishavMaisuria/research-paper-lifecycle-skills](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills) | Citation checking, paper writing, submission, rebuttal, presentation | 42 skills covering a full paper lifecycle, Apache-2.0. | Preserve LICENSE and NOTICE if redistributing substantial content; venue rules change, so check official current instructions. |
| [Jason-Mar1/awesome-academic-research-skills](https://github.com/Jason-Mar1/awesome-academic-research-skills) | Research workflow discovery by stage and discipline | Useful map of literature, experiments, figures, writing, and peer review collections. | It is a discovery index, not an endorsement or benchmark; linked skills have different licenses. |
| [O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills) | Literature search, paper reading, data analysis, figures, writing, peer review | Another focused research index that records license and disclosed capabilities. | Index license does not override upstream skill licenses; check network, hooks, and scripts per project. |
| [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills) | Biology, genomics, scientific databases and tools | Specialist science workflows from Google DeepMind. | Skills/data may have mixed terms and domain-specific prerequisites; check per-item licensing and suitability. |

## Skill quality and evaluation

| Project | Best starting point | Why explore it | Important caveat |
|---|---|---|---|
| [NVIDIA SkillEvaluator](https://docs.nvidia.com/skills/skillevaluator) | Deterministic quality gates, overlap checks, generated eval cases, live agent evaluation | Useful model for testing skills as behavioral artifacts, not just Markdown files. | Documentation marks support as experimental; inspect the implementation and license before adopting it. |

## Codex note

The older [openai/skills](https://github.com/openai/skills) catalog is marked deprecated in its README, and its individual skill licenses are listed in per-skill `LICENSE.txt` files. For current Codex skill locations and usage, consult the [Codex skill documentation](https://developers.openai.com/codex/skills/) and the [Agent Skills standard](https://agentskills.io/).

## Selection checklist

Before adding an external skill, check: (1) exact source file and license, (2) last meaningful maintenance and supported host, (3) trigger specificity and overlap with an existing skill, (4) scripts/network/hooks/permissions, (5) source and data privacy, (6) positive and negative behavior examples, and (7) a realistic evaluation case. Popularity alone is not a quality or safety measure.
