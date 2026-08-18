

<br />

<div align="center">


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://www.codium.ai/images/pr_agent/logo-dark.png" width="330">
  <source media="(prefers-color-scheme: light)" srcset="https://www.codium.ai/images/pr_agent/logo-light.png" width="330">
  <img src="https://www.codium.ai/images/pr_agent/logo-light.png" alt="logo" width="330">

</picture>
<br>
The Original Open-Source PR Reviewer
<br><br>
<a href="https://github.com/rajshree1854/pr-agent/commits/main">
<img alt="GitHub" src="https://img.shields.io/github/last-commit/rajshree1854/pr-agent/main?style=for-the-badge" height="20">
</a>
</div>

---

 This repository contains the open-source PR Agent Project. 
 It is not the Qodo offering for open-source projects.
 
PR-Agent is an open-source, AI-powered code review agent and a community-maintained legacy project of Qodo. It is distinct from Qodo's primary AI code review offering, which provides a feature-rich, context-aware experience. Qodo offers a free version for open-source projects and integrates seamlessly with GitHub, GitLab, Bitbucket, and Azure DevOps for high-quality automated reviews.


## Table of Contents

- [Getting Started](#getting-started)
- [Why Use PR-Agent?](#why-use-pr-agent)
- [Features](#features)
- [See It in Action](#see-it-in-action)
- [How It Works](#how-it-works)
- [Data Privacy](#data-privacy)
- [Contributing](#contributing)

## Getting Started

> [!NOTE]
> **Docker Hub namespace migration.** Releases `0.34.2` and later are published under [`pragent/pr-agent`](https://hub.docker.com/r/pragent/pr-agent). Older releases (up to and including `v0.31`) remain available at the legacy [`rajshree1854/pr-agent`](https://hub.docker.com/r/rajshree1854/pr-agent) namespace as a frozen archive — no new images are pushed there. Update any pinned `image:` / `docker pull` / `uses: docker://` references when upgrading to `0.34.2+`.

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
[Full GitHub Action setup guide](https://rajshree1854.github.io/Pr-Agent/installation/github/#run-as-a-github-action)

#### 2. CLI Usage (Local Development)

Run PR-Agent locally on your repository:

PyPI publishing is temporarily behind: `pip install pr-agent` currently installs `0.39.0`.
Until publishing resumes, install the current release (`v0.42.0`) reproducibly from its GitHub tag:

```bash
pip install "pr-agent @ git+https://github.com/rajshree1854/pr-agent.git@v0.42.0"
export OPENAI_KEY=your_key_here
pr-agent --pr_url https://github.com/owner/repo/pull/123 review
```
[Complete CLI setup guide](https://rajshree1854.github.io/Pr-Agent/usage-guide/automations_and_usage/#local-repo-cli)

#### 3. Other Platforms

- [GitLab webhook setup](https://rajshree1854.github.io/Pr-Agent/installation/gitlab/)
- [BitBucket app installation](https://rajshree1854.github.io/Pr-Agent/installation/bitbucket/)
- [Azure DevOps setup](https://rajshree1854.github.io/Pr-Agent/installation/azure/)

## Why Use PR-Agent?

### 🎯 Built for Real Development Teams

**Fast & Affordable**: Each tool (`/review`, `/improve`, `/ask`) uses a single LLM call (~30 seconds, low cost)

**Handles Any PR Size**: Our [PR Compression strategy](https://rajshree1854.github.io/Pr-Agent/core-abilities/#pr-compression-strategy) effectively processes both small and large PRs

**Highly Customizable**: JSON-based prompting allows easy customization of review categories and behavior via [configuration files](pr_agent/settings/configuration.toml)

**Platform Agnostic**: 
- **Git Providers**: GitHub, GitLab, BitBucket, Azure DevOps, Gitea
- **Deployment**: CLI, GitHub Actions, Docker, self-hosted, webhooks
- **AI Models**: OpenAI GPT, Anthropic Claude, Google Gemini, DeepSeek, Mistral, and any other model reachable through LiteLLM (Azure OpenAI, AWS Bedrock, Vertex AI, Databricks, OpenRouter, Ollama, and more) — see [Changing a model](https://rajshree1854.github.io/Pr-Agent/usage-guide/changing_a_model/)

**Open Source Benefits**:
- Full control over your data and infrastructure
- Customize prompts and behavior for your team's needs
- No vendor lock-in
- Community-driven development

## Features

<div style="text-align:left;">

PR-Agent offers comprehensive pull request functionalities integrated with various git providers:

|                                                         |                                                                                        | GitHub | GitLab | Bitbucket | Azure DevOps | Gitea |
|---------------------------------------------------------|----------------------------------------------------------------------------------------|:------:|:------:|:---------:|:------------:|:-----:|
| [TOOLS](https://rajshree1854.github.io/Pr-Agent/tools/)         | [Describe](https://rajshree1854.github.io/Pr-Agent/tools/describe/)                            |   ✅   |   ✅   |    ✅     |      ✅      |  ✅   |
|                                                         | [Review](https://rajshree1854.github.io/Pr-Agent/tools/review/)                                |   ✅   |   ✅   |    ✅     |      ✅      |  ✅   |
|                                                         | [Improve](https://rajshree1854.github.io/Pr-Agent/tools/improve/)                              |   ✅   |   ✅   |    ✅     |      ✅      |  ✅   |
|                                                         | [Ask](https://rajshree1854.github.io/Pr-Agent/tools/ask/)                                      |   ✅   |   ✅   |    ✅     |      ✅      |       |
|                                                         | ⮑ [Ask on code lines](https://rajshree1854.github.io/Pr-Agent/tools/ask/#ask-lines)            |   ✅   |   ✅   |           |              |       |
|                                                         | [Help Docs](https://rajshree1854.github.io/Pr-Agent/tools/help_docs/) ⚠️                       |   —    |   —    |    —      |              |       |
|                                                         | [Update CHANGELOG](https://rajshree1854.github.io/Pr-Agent/tools/update_changelog/)            |   ✅   |   ✅   |    ✅     |      ✅      |       |
|                                                         |                                                                                                                     |        |        |           |              |       |
| [USAGE](https://rajshree1854.github.io/Pr-Agent/usage-guide/)   | [CLI](https://rajshree1854.github.io/Pr-Agent/usage-guide/automations_and_usage/#local-repo-cli)                            |   ✅   |   ✅   |    ✅     |      ✅      |  ✅   |
|                                                         | [App / webhook](https://rajshree1854.github.io/Pr-Agent/usage-guide/automations_and_usage/#github-app)                      |   ✅   |   ✅   |    ✅     |      ✅      |  ✅   |
|                                                         | [Tagging bot](https://github.com/rajshree1854/pr-agent#try-it-now)                                                     |   ✅   |        |           |              |       |
|                                                         | [Actions](https://rajshree1854.github.io/Pr-Agent/installation/github/#run-as-a-github-action)                              |   ✅   |   ✅   |    ✅     |      ✅      |       |
|                                                         |                                                                                                                     |        |        |           |              |       |
| [CORE](https://rajshree1854.github.io/Pr-Agent/core-abilities/) | [Adaptive and token-aware file patch fitting](https://rajshree1854.github.io/Pr-Agent/core-abilities/compression_strategy/) |   ✅   |   ✅   |    ✅     |      ✅      |       |
|                                                         | [Agent skills (`SKILL.md`)](https://rajshree1854.github.io/Pr-Agent/core-abilities/agent_skills/)                           |   ✅   |   ✅   |    ✅     |      ✅      |  ✅   |
|                                                         | [Repo context files (`AGENTS.md`)](https://rajshree1854.github.io/Pr-Agent/usage-guide/additional_configurations/#bringing-per-repo-context-files-to-pr-agent) |   ✅   |   ✅   |    ✅     |      ✅      |  ✅   |
|                                                         | [Dynamic context](https://rajshree1854.github.io/Pr-Agent/core-abilities/dynamic_context/)                                  |   ✅   |   ✅   |    ✅     |      ✅      |       |
|                                                         | [Fetching ticket context](https://rajshree1854.github.io/Pr-Agent/core-abilities/fetching_ticket_context/)                  |   ✅    |  ✅    |     ✅     |              |       |
|                                                         | [Local and global metadata](https://rajshree1854.github.io/Pr-Agent/core-abilities/metadata/)                               |   ✅   |   ✅   |    ✅     |      ✅      |       |
|                                                         | [Multiple models support](https://rajshree1854.github.io/Pr-Agent/usage-guide/changing_a_model/)                            |   ✅   |   ✅   |    ✅     |      ✅      |       |
|                                                         | [PR compression](https://rajshree1854.github.io/Pr-Agent/core-abilities/compression_strategy/)                              |   ✅   |   ✅   |    ✅     |      ✅      |       |
|                                                         | [Self reflection](https://rajshree1854.github.io/Pr-Agent/core-abilities/self_reflection/)                                  |   ✅   |   ✅   |    ✅     |      ✅      |       |

⚠️ `/help_docs` is temporarily disabled since `v0.36.1` pending a fix for a credential-exposure issue ([#2445](https://github.com/rajshree1854/pr-agent/issues/2445)).

[//]: # (- Support for additional git providers is described in [here]&#40;./docs/Full_environments.md&#41;)
___

## See It in Action

</div>
<h4><a href="https://github.com/rajshree1854/pr-agent/pull/530">/describe</a></h4>
<div align="center">
<p float="center">
<img src="https://www.codium.ai/images/pr_agent/describe_new_short_main.png" width="512">
</p>
</div>
<hr>

<h4><a href="https://github.com/rajshree1854/pr-agent/pull/732#issuecomment-1975099151">/review</a></h4>
<div align="center">
<p float="center">
<kbd>
<img src="https://www.codium.ai/images/pr_agent/review_new_short_main.png" width="512">
</kbd>
</p>
</div>
<hr>

<h4><a href="https://github.com/rajshree1854/pr-agent/pull/732#issuecomment-1975099159">/improve</a></h4>
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

See the [Tools docs](https://rajshree1854.github.io/Pr-Agent/tools/#usage-examples) for the full list of tools with example commands, and each tool's page for screenshots and options.

<hr>

## How It Works

The following diagram illustrates PR-Agent tools and their flow:

![PR-Agent Tools](https://www.qodo.ai/images/pr_agent/diagram-v0.9.png)

## Data Privacy

### Self-hosted PR-Agent

- If you host PR-Agent with your OpenAI API key, it is between you and OpenAI. You can read their API data privacy policy here:
https://openai.com/enterprise-privacy

