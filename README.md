# DevSecOps Security Pipeline

An interview-ready DevSecOps demonstration: secure a Python Flask app through automated testing and security checks in GitHub Actions.

## Security controls

| Area | Tool | Purpose |
|---|---|---|
| SAST | Semgrep | Find insecure source patterns |
| SCA | pip-audit | Detect vulnerable Python dependencies |
| Secrets | Gitleaks | Detect committed credentials |
| Container | Trivy | Scan image OS and application packages |
| DAST | OWASP ZAP Baseline | Passive checks against the running demo |
| Tests | pytest | Validate application behavior |

## Pipeline

```text
Pull request / push
  -> pytest
  -> Semgrep (SAST)
  -> pip-audit (SCA)
  -> Gitleaks (secrets)
  -> Docker build -> Trivy (container scan)
  -> separate DAST workflow -> OWASP ZAP against local demo
  -> review findings -> fix -> rerun -> merge
```

## Run locally

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
python app.py
```

Open http://127.0.0.1:5000/health.

## Local security scans

Install the scanners from their official documentation:

```bash
semgrep scan --config semgrep.yml .
pip-audit -r requirements.txt
gitleaks detect --source . --redact
docker build -t devsecops-demo:local .
trivy image --severity HIGH,CRITICAL --exit-code 1 devsecops-demo:local
```

## GitHub configuration

- Workflows use read-only repository permissions.
- Configure successful CI jobs as required status checks in **Settings → Branches** to enforce merge gates.
- Enable CodeQL default setup under **Settings → Code security and analysis → Code scanning** if desired.
- Dependabot proposes weekly updates for Python packages, Docker and GitHub Actions.
- Never use `pull_request_target` to execute untrusted PR code.

## Security design choices

1. No credentials are stored in source code.
2. Do not expose secrets to forked pull requests.
3. DAST targets only this isolated demo. Scan other systems only with explicit authorization.
4. Review and triage findings; a clean scan is not proof of security.
5. Pin third-party actions to reviewed full commit SHAs before production use.
6. Keep dependencies and actions updated.

## Interview talking points

**Why multiple scanners?** SAST inspects source, SCA checks third-party packages, secret scanning detects exposed credentials, container scanning checks image packages, and DAST observes the running app.

**How do you gate merges?** Require successful checks, code review and protected branches; restrict bypass permissions.

**Production improvements:** SBOM publication, signed image provenance, IaC scanning, policy-as-code, centralized findings, protected deployment environments and runtime monitoring.

## License

MIT
