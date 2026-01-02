---
id: 01KDZAVXFFWC39D6NGA5M7WC6Q
type: drill
status: untried
created: 2026-01-02T13:28:08.559575
source_id: 01KDZAPA83GFZ67M7YFZAKMNYM
next_review: 2026-01-02
review_count: 0
timebox_min: 10
topics: ['Commits', 'Pushing', 'Version Control']
prereqs: []
---

# Commit and Push a Code Update

## Pattern
- Modify an existing file in your local repository.
- Stage the changes using `git add .`.
- Create a descriptive commit message using `git commit -m`.
- Push the committed changes to the remote GitHub repository using `git push`.

## Drill
**Goal:** Successfully update a file in your local repository and push the changes to GitHub.

**Steps:**
1. Open the local repository you created in the previous drill (e.g., 'my-new-project').
2. Modify the `index.html` file by adding another line of text (e.g., 'This is an update.'). Save the file (See 22:53-23:02).
3. In your terminal, execute `git add .` to stage the changes (See 23:04).
4. Commit the changes with a descriptive message like 'Updated index.html' using `git commit -m` (See 23:07-23:18).
5. Push the changes to your GitHub repository using `git push origin main` (See 23:19-23:33).

## Snippet
```commands
git add .
git commit -m "Updated index.html"
git push origin main
```

## Validation
- [ ] Your GitHub repository's `index.html` file now reflects the changes you made locally.
- [ ] A new commit message (e.g., 'Updated index.html') appears in the commit history of your GitHub repository (See 23:48-23:51).
- [ ] The 'files changed' view on GitHub shows the specific lines added/removed (See 23:56-23:57).

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
