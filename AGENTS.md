# AGENTS.md - fwordlesolver Developer & Agent Guidelines

## 1. Project Overview & Multi-Repo Structure
`fwordlesolver` is a full-stack Wordle solver application split into separate components:

- **`fwordlesolver-api`**: Python backend exposing the solving algorithms, endpoints, and dictionary validations.
- **`fwordlesolver-web`**: TypeScript / Frontend web interface.
- **`fwordlesolver-ops`**: CDK8s operations repository generating Kubernetes manifests.
- **Routing & Ingress**:
  - Non-prod (Devo): `https://games-devo.codeuni.net/wordle-solver` (API: `/wordle-solver/api`)
  - Prod: `https://games.codeuni.net/wordle-solver` (API: `/wordle-solver/api`)

---

## 2. Component Workflows

### Backend (`fwordlesolver-api`)
- Python environment managed with `uv`.
- Run tests: `uv run pytest`.
- Linting: `ruff`.
- GitHub Actions: `.github/workflows/publish.yml` builds and pushes `fmakdemir/fwordlesolver-api:<tag>`.

### Frontend (`fwordlesolver-web`)
- Node.js & `pnpm`.
- Build & Test: `pnpm install`, `pnpm test`, `pnpm build`.
- GitHub Actions: `.github/workflows/publish.yml` builds and pushes `fmakdemir/fwordlesolver-web:<tag>`.

### Infrastructure (`fwordlesolver-ops`)
- CDK8s Chart in `fwordlesolver-ops/main.ts`.
- Workloads are standard Kubernetes `Deployment` resources (`fws-api`, `fws-web`).
- Manifest synthesis: `stage=devo npx cdk8s-cli synth` or `stage=prod npx cdk8s-cli synth`.
- Local devo update script: [`fwordlesolver-ops/update-devo.sh`](file:///home/fma/fwordlesolver/fwordlesolver-ops/update-devo.sh).

---

## 3. CI/CD & Release Pipeline

The pipeline triggers automatically on code change:
1. **GitHub Actions**:
   - `publish.yml` builds and publishes Docker image to DockerHub (`fmakdemir/fwordlesolver-api` or `fmakdemir/fwordlesolver-web`).
   - Calls the cluster release webhook via `curl` to `https://events.codeuni.net/release` using `ARGO_EVENTS_WEBHOOK_TOKEN`.
2. **Argo Events & Workflows**:
   - Ingests event in `argo-events` and starts `ClusterWorkflowTemplate/application-release`.
   - Automatically detects standard `Deployment`, updates container image using `kubectl set image`, and monitors rollout readiness.

---

## 4. Agent Guidelines & Invariants
- **No GitOps Reconcile Loops**: Deployments are imperatively updated via Argo Events & Workflows. Do not enable automated sync on ArgoCD Applications for this project.
- **Cluster Ingress**: Ingress routes use `cloudflare-tunnel` class.
- **Tools**: Use `write_to_file` and `replace_file_content` for editing code. Refer to [`/home/fma/cluster-ops/runbook-k8s.md`](file:///home/fma/cluster-ops/runbook-k8s.md) for cluster diagnostics.
