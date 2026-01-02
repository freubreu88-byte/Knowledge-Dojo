---
id: 01KDZAVXFCAJXC87N98VDKMXQC
type: drill
status: untried
created: 2026-01-02T13:28:08.556081
source_id: 01KDZAPA83GFZ67M7YFZAKMNYM
next_review: 2026-01-02
review_count: 0
timebox_min: 20
topics: ['Setup', 'Security', 'Authentication']
prereqs: []
---

# Set Up Your GitHub Environment with SSH Key and Git

## Pattern
- Securely connect your local machine to GitHub using an SSH key.
- Ensure Git is installed and recognized by your development environment.
- Understand why SSH keys are preferred over access tokens for long-term authentication.

## Drill
**Goal:** Successfully configure your development environment to securely interact with GitHub repositories.

**Steps:**
1. Navigate to your GitHub profile settings and locate the SSH GPGs section (See 12:49).
2. Follow the provided Google Doc guide and video (linked in the video description) to generate and add an SSH key to your GitHub account (See 13:03, 13:08).
3. Verify your SSH connection by attempting a test connection (e.g., `ssh -T git@github.com`).
4. Ensure Git is installed on your local machine. If not, follow the installation guide referenced in the video description for your operating system (Mac, Windows, Linux) (See 16:41, 17:00).
5. Confirm Git is recognized by your terminal by typing `git --version`.

## Snippet
```commands
ssh -T git@github.com
git --version
```

## Validation
- [ ] You have successfully added an SSH key to your GitHub profile.
- [ ] The `ssh -T git@github.com` command outputs a success message (e.g., 'Hi <username>! You've successfully authenticated...').
- [ ] The `git --version` command outputs the installed Git version.
- [ ] You understand why SSH keys are used for secure GitHub access.

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
