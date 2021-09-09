# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from buildbot.www.hooks.github import GitHubEventHandler

class CustomGitHubHandler(GitHubEventHandler):

    def handle_push(self, payload, event):
        # This field is unused:

        payload['repository']['html_url'] = payload['repository']['ssh_url']
        return super().handle_push(payload, event)


    def handle_pull_request(self, payload, event):

        payload['repository']['html_url'] = payload['repository']['ssh_url']
        return super().handle_pull_request(payload, event)
