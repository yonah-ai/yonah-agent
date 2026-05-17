# yonah-agent

**Yonah** is a dual-audience autonomous AI agent with verifiable per-decision provenance for regulated domains. This repository is the **framework upstream** of the Yonah family: the vertical-agnostic backend that the per-vertical forks derive from and pull updates from.

The framework defines the architectural pattern — the seven-tool API contract, the three-crew internal structure, the PAC-AI substrate integration, the role-gated refusal contract, the identity-blind PII detacher, the multi-provider LLM adapter, and the AWS Chalice + CrewAI deployment scaffolding. Each vertical fork supplies the domain content: concrete artefact schema, concrete tool implementations, vertical-specific crews, and the regulatory-anchor mapping for the domain's compliance regime.

The org-level profile + brand spec + per-vertical proposals live in the [.github](https://github.com/yonah-ai/.github) repo.

## Status

**Early scaffold.** The directory layout and architectural skeletons are in place; the framework base classes are defined; the business logic is being filled in. Every file that is currently a stub carries a `TODO` marker. Pin `jhcontext-sdk` and `jhcontext-protocol` from PyPI when first running `pip install -e .`.

## The seven-tool surface (API contract)

A single named conversational agent (**Yonah**) serves two audiences with role-aware refusals enforced by `agent/yonah/role_guard.py`:

| Tool | Audience | Purpose |
|---|---|---|
| `build_artefact` | authority | Co-design a shared-contract artefact (the vertical's domain object) |
| `publish_artefact` | authority | Bind an artefact at a fixed version to a second-audience cohort |
| `commit_decision` | authority | Review the evaluator's per-criterion output and commit a final decision |
| `tutor_me` | second_audience | Be tutored against the active artefact (formative loop) |
| `submit_draft` | second_audience | Submit work for identity-blind evaluation against the artefact |
| `query_my_provenance` | second_audience | Retrieve the PROV-O subgraph for one of one's own decisions |
| `delete_my_data` | universal | Scrub the caller's PII reattachment mapping |

Each tool ships in this repository as an **abstract base class** with the input-schema, output-schema, and regulatory-anchor override hooks named explicitly. Vertical forks subclass these and provide the domain-specific implementation. See `agent/yonah/tools/`.

## The three-crew internal structure

The seven tools dispatch internally to three CrewAI crews:

| Crew | Invoked by | Framework lifecycle stages |
|---|---|---|
| `ArtefactBuilderCrew` | `build_artefact` | TypeAdvisor -> CriteriaElicitor -> Validator |
| `TutorCrew` | `tutor_me` | ArtefactSummariser -> FormativeGuide -> ReflectionPrompter |
| `EvaluatorCrew` | `submit_draft` (via SQS) | IdentityBlindReader -> ArtefactApplier -> EvidenceFinder -> Calibrator -> Auditor |

Each crew is an abstract base class. The framework owns the lifecycle stages and the structural-verifier hooks; each vertical fork supplies the concrete CrewAI Agents + Tasks, the vertical voice, and the regulatory-anchor mapping. See `agent/crews/`.

## The PAC-AI substrate dependency

Every tool invocation, every crew handoff, and every model call produces a content-hashed signed envelope persisted to an append-only Provenance-Aware Context for AI (PAC-AI) graph in DynamoDB. The PAC-AI substrate is imported from PyPI (`jhcontext-sdk`, `jhcontext-protocol`) rather than vendored; the framework's role is to ensure every action emits an envelope and that the chain re-derives.

## Layout

```
yonah-agent/
  app.py                     # Chalice REST + WebSocket entry point
  chalicelib/
    blueprints/              # one Blueprint per API surface
    pii/                     # PII detacher middleware + reattacher (KMS-wrapped)
    llm/                     # multi-provider adapter (Anthropic / OpenAI / Gemini)
  models/
    dao/                     # PynamoDB DAOs (User, ApiKey, Cohort,
                             # Artefact, Decision, Envelope, PiiToken)
    dtos/                    # Pydantic v2 DTOs
  agent/
    yonah/                   # the conversational agent itself
      personality.md         # the published identity contract (framework default)
      role_guard.py          # the asymmetric refusal contract
      yonah_agent.py         # agent + tool registry
      tools/                 # one base-class stub per tool
    crews/                   # the three internal crews (abstract base classes)
      artefact_builder/
      tutor/
      evaluator/
    flows/                   # CrewAI Flow classes
    ontologies/              # generic structural validators (framework) +
                             # domain-validator override hook
    libs/llms.py             # lazy LLM wrapper
  worker/
    worker_main.py           # Lambda handler dispatching to crews from SQS
  Dockerfile                 # Lambda container image for the worker
  buildspec.yml              # AWS CodeBuild spec
  deploy.sh                  # one-command deploy
  DEPLOY.md                  # AWS install guide
  pyproject.toml
  requirements.txt
  tests/                     # pytest + moto
```

## Quick start (local development)

```bash
# Python 3.12 recommended
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Local Chalice (REST only; WSS needs deployed API Gateway)
chalice local

# Worker run against LocalStack SQS (separate terminal)
LOCALSTACK_ENDPOINT=http://localhost:4566 \
  python -m worker.worker_main --local
```

## Deployment

See [DEPLOY.md](DEPLOY.md) for the full AWS install guide (IAM, DynamoDB tables, SQS, KMS CMK, Chalice deploy, CodeBuild for the worker, smoke test).

## Vertical forks (the family)

The framework upstream is the source from which the per-vertical reference implementations derive. Each vertical fork tracks the upstream framework and inherits framework-level improvements via `git pull upstream main`; only files inside the vertical-override surface are vertical-specific.

| Vertical | Backend repo | Status |
|---|---|---|
| Education | [yonah-edu-agent](https://github.com/yonah-ai/yonah-edu-agent) | reference implementation (companion to the IJAIED paper) |
| Health | `yonah-agent-health` | forthcoming — will fork this framework |
| Hire | `yonah-agent-hire` | forthcoming — will fork this framework |

The frontend lives at [yonah-page](https://github.com/yonah-ai/yonah-page) (framework upstream) with symmetric vertical forks.

## License

Apache-2.0 — see [LICENSE](LICENSE).
