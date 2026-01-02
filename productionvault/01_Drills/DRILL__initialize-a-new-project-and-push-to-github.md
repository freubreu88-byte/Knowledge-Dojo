---
id: 01KDZAVXFEW1DTN5Z98Z8YYF8Y
type: drill
status: untried
created: 2026-01-02T13:28:08.558903
source_id: 01KDZAPA83GFZ67M7YFZAKMNYM
next_review: 2026-01-02
review_count: 0
timebox_min: 15
topics: ['Repositories', 'Commits', 'Pushing']
prereqs: []
---

# Initialize a New Project and Push to GitHub

## Pattern
- Create a new, empty repository on GitHub.
- Initialize a local directory as a Git repository.
- Add existing local files to the Git staging area.
- Commit the staged files.
- Connect the local Git repository to the remote GitHub repository.
- Push the initial commit to GitHub.

## Drill
**Goal:** Successfully create a new GitHub repository and push your first set of local code to it.

**Steps:**
1. Create a new, empty repository on GitHub (e.g., 'my-new-project') (See 20:04-20:16). Do not initialize with a README.
2. Copy the SSH link for your newly created empty repository (See 20:23-20:25).
3. On your local machine, create a new folder for your project and add a simple file (e.g., `index.html` with 'Hello, GitHub!').
4. Open your terminal in this new local project folder and execute the `git init`, `git add .`, `git commit -m "Initial commit"`, `git remote add origin <SSH_URL>`, and `git push -u origin main` commands (See 20:57-21:25).

## Snippet
```commands
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:<YOUR_USERNAME>/my-new-project.git
git push -u origin main
```

## Validation
- [ ] Your new GitHub repository now displays the `index.html` file and the 'Initial commit' message.
- [ ] The `main` branch is visible in your GitHub repository.
- [ ] No errors occurred during the push operation.

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
