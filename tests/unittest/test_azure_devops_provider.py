from types import SimpleNamespace
from unittest.mock import MagicMock

from pr_agent.git_providers.azuredevops_provider import AzureDevopsProvider


class TestAzureDevopsProviderRepoContext:
    def test_get_repo_file_content_reads_from_target_commit(self):
        # Repo-context files must be read from the PR target (base) commit, matching
        # the other providers.
        provider = AzureDevopsProvider.__new__(AzureDevopsProvider)
        provider.repo_slug = "my-repo"
        provider.workspace_slug = "my-project"
        provider.pr = MagicMock()
        provider.pr.last_merge_target_commit.commit_id = "base-sha"
        provider.azure_devops_client = MagicMock()
        provider.azure_devops_client.get_item.return_value = MagicMock(content="repo context")

        content = provider.get_repo_file_content("AGENTS.md")

        assert content == "repo context"
        _, kwargs = provider.azure_devops_client.get_item.call_args
        assert kwargs["path"] == "AGENTS.md"
        assert kwargs["repository_id"] == "my-repo"
        assert kwargs["project"] == "my-project"
        assert kwargs["version_descriptor"].version == "base-sha"
        assert kwargs["version_descriptor"].version_type == "commit"

    def test_get_repo_file_content_from_default_branch_omits_version(self):
        provider = AzureDevopsProvider.__new__(AzureDevopsProvider)
        provider.repo_slug = "my-repo"
        provider.workspace_slug = "my-project"
        provider.pr = MagicMock()
        provider.azure_devops_client = MagicMock()
        provider.azure_devops_client.get_item.return_value = MagicMock(content="repo context")

        content = provider.get_repo_file_content("AGENTS.md", from_default_branch=True)

        assert content == "repo context"
        _, kwargs = provider.azure_devops_client.get_item.call_args
        assert kwargs["version_descriptor"] is None  # no version -> default branch

    def test_get_repo_file_content_treats_failure_as_empty(self):
        provider = AzureDevopsProvider.__new__(AzureDevopsProvider)
        provider.repo_slug = "my-repo"
        provider.workspace_slug = "my-project"
        provider.pr = MagicMock()
        provider.pr.last_merge_target_commit.commit_id = "base-sha"
        provider.azure_devops_client = MagicMock()
        provider.azure_devops_client.get_item.side_effect = Exception("not found")

        assert provider.get_repo_file_content("MISSING.md") == ""


class TestAzureDevopsProviderInlineComments:
    @staticmethod
    def _provider(threads):
        provider = AzureDevopsProvider.__new__(AzureDevopsProvider)
        provider.repo_slug = "my-repo"
        provider.workspace_slug = "my-project"
        provider.pr_num = 42
        provider.azure_devops_client = MagicMock()
        provider.azure_devops_client.get_threads.return_value = threads
        return provider

    def test_get_inline_comment_bodies_only_returns_line_threads(self):
        line_thread = SimpleNamespace(
            thread_context=SimpleNamespace(file_path="/app.py", right_file_start=SimpleNamespace(line=3)),
            comments=[SimpleNamespace(content="line finding")],
        )
        file_thread = SimpleNamespace(
            thread_context=SimpleNamespace(file_path="/app.py", right_file_start=None),
            comments=[SimpleNamespace(content="file finding")],
        )
        pr_thread = SimpleNamespace(
            thread_context=None,
            comments=[SimpleNamespace(content="PR finding")],
        )
        provider = self._provider([line_thread, file_thread, pr_thread])

        assert provider.get_inline_comment_bodies() == ["line finding"]
        provider.azure_devops_client.get_threads.assert_called_once_with(
            repository_id="my-repo",
            pull_request_id=42,
            project="my-project",
        )

    def test_get_inline_comment_bodies_supports_serialized_context(self):
        thread = SimpleNamespace(
            thread_context={"filePath": "/app.py", "rightFileStart": {"line": 3, "offset": 1}},
            comments=[SimpleNamespace(content="line finding"), SimpleNamespace(content="")],
        )

        assert self._provider([thread]).get_inline_comment_bodies() == ["line finding"]

    def test_get_inline_comment_bodies_includes_recent_successful_posts(self):
        provider = self._provider([])
        provider.publish_code_suggestions([{
            "body": "line finding",
            "relevant_file": "/app.py",
            "relevant_lines_start": 3,
            "relevant_lines_end": 3,
        }])

        assert provider.get_inline_comment_bodies() == ["line finding"]

    def test_set_pr_clears_inline_comment_state(self):
        provider = self._provider([])
        provider._published_inline_comment_bodies = ["old finding"]
        provider._inline_comment_store = MagicMock()
        provider._parse_pr_url = MagicMock(return_value=("new-project", "new-repo", 43))
        provider._get_pr = MagicMock(return_value=MagicMock())

        provider.set_pr("https://dev.azure.com/example/new-project/_git/new-repo/pullrequest/43")

        assert provider._published_inline_comment_bodies == []
        assert provider._inline_comment_store is None

    def test_recent_inline_comment_bodies_returns_a_copy(self):
        provider = self._provider([])
        provider._published_inline_comment_bodies = ["line finding"]

        bodies = provider.get_recent_inline_comment_bodies()
        bodies.append("other finding")

        assert provider.get_recent_inline_comment_bodies() == ["line finding"]
