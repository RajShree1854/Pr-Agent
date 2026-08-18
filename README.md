# PR-Agent

<div align="center">

An open-source, AI-powered code review agent.

<a href="https://github.com/rajshree1854/pr-agent/commits/main">
<img alt="GitHub" src="https://img.shields.io/github/last-commit/rajshree1854/pr-agent/main?style=for-the-badge" height="20">
</a>
</div>

---

PR-Agent is an open-source, AI-powered code review agent. It integrates seamlessly with GitHub, GitLab, Bitbucket, and Azure DevOps to provide high-quality automated reviews, code suggestions, and PR descriptions.

## Table of Contents

- [Getting Started](#getting-started)
- [Why Use PR-Agent?](#why-use-pr-agent)
- [Features](#features)
- [How It Works](#how-it-works)

## Getting Started

### 🚀 Quick Start for PR-Agent

#### 1. GitHub Action (Recommended)

Add automated PR reviews to your repository with a simple workflow file:

```yaml
# .github/workflows/pr-agent.yml
name: PR Agent
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  pr_agent_job:
    runs-on: ubuntu-latest
    steps:
    - name: PR Agent action step
      uses: rajshree1854/pr-agent@main
      env:
        OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### 2. CLI Usage (Local Development)

Run PR-Agent locally on your repository:

```bash
pip install "pr-agent @ git+https://github.com/rajshree1854/pr-agent.git@main"
export OPENAI_KEY=your_key_here
pr-agent --pr_url https://github.com/owner/repo/pull/123 review
```

## Why Use PR-Agent?

### 🎯 Built for Real Development Teams

**Fast & Affordable**: Each tool (`/review`, `/improve`, `/ask`) uses a single LLM call (~30 seconds, low cost)

**Handles Any PR Size**: Effectively processes both small and large PRs through intelligent compression strategies.

**Highly Customizable**: JSON-based prompting allows easy customization of review categories and behavior via configuration files.

**Platform Agnostic**: 
- **Git Providers**: GitHub, GitLab, BitBucket, Azure DevOps, Gitea
- **Deployment**: CLI, GitHub Actions, Docker, self-hosted, webhooks
- **AI Models**: OpenAI GPT, Anthropic Claude, Google Gemini, and any other model reachable through LiteLLM.

## Features

PR-Agent offers comprehensive pull request functionalities integrated with various git providers:

| TOOLS |
|-------|
| Describe |
| Review |
| Improve |
| Ask |
| Update CHANGELOG |

## See It in Action

<h4>/describe</h4>
<div align="center">
<p float="center">
<img src="https://www.codium.ai/images/pr_agent/describe_new_short_main.png" width="512">
</p>
</div>
<hr>

<h4>/review</h4>
<div align="center">
<p float="center">
<kbd>
<img src="https://www.codium.ai/images/pr_agent/review_new_short_main.png" width="512">
</kbd>
</p>
</div>
<hr>

<h4>/improve</h4>
<div align="center">
<p float="center">
<kbd>
<img src="https://www.codium.ai/images/pr_agent/improve_new_short_main.png" width="512">
</kbd>
</p>
</div>
<hr>

### Usage Examples

PR-Agent tools run as a comment on a PR or from the CLI. A few common ones:

```bash
# Comment on a PR (GitHub/GitLab/Bitbucket/…):
/describe                        # generate title, summary, walkthrough and labels
/review                          # findings, security, review effort and tests
/improve                         # actionable code-improvement suggestions
/ask "What does this PR change?" # free-text Q&A about the PR

# Or locally via the CLI:
pr-agent --pr_url <PR_URL> review
```

## How It Works

PR-Agent processes pull requests by parsing the repository context, fetching the diff, intelligently compressing it if necessary to fit within AI token limits, and querying the specified AI model to generate actionable feedback and reviews.
