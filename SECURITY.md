# Security Policy

## Supported Versions

Knowledge-Dojo is currently in active development. The following versions receive security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| 0.9.x   | :white_check_mark: |
| < 0.9   | :x:                |

**Note:** As this project is in early stages, we recommend always using the latest version from the `main` branch.

## Reporting a Vulnerability

We take security seriously. Knowledge-Dojo handles sensitive data including:
- API keys (Gemini API)
- Local file system access (Obsidian vaults)
- User-generated content and learning data

### How to Report

**Please DO NOT open public GitHub issues for security vulnerabilities.**

Instead, report security issues via:

1. **GitHub Security Advisories** (preferred): Navigate to the [Security tab](https://github.com/freubreu88-byte/Knowledge-Dojo/security/advisories) and click "Report a vulnerability"
2. **Email**: Send details to the repository maintainer (check GitHub profile for contact info)

### What to Include

Please provide:
- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Potential impact
- Suggested fix (if available)

### Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Every 7 days until resolved
- **Fix timeline**: Critical issues within 14 days, moderate issues within 30 days

### What to Expect

**If accepted:**
- We'll work with you to understand and verify the issue
- A fix will be developed and tested
- Credit will be given in release notes (unless you prefer anonymity)
- CVE will be requested for critical vulnerabilities

**If declined:**
- We'll explain why the report doesn't constitute a security vulnerability
- Alternative solutions or mitigations may be suggested

## Security Best Practices for Users

When using Knowledge-Dojo:

1. **Protect your API keys**: Never commit `.env` files to version control
2. **Vault permissions**: Ensure your Obsidian vault has appropriate file system permissions
3. **Keep dependencies updated**: Run `pip install --upgrade knowledge-dojo` regularly
4. **Review generated content**: AI-generated drills may contain sensitive information from source material
5. **Backup your vault**: Regular backups protect against data corruption

## Known Security Considerations

- **API Key Storage**: Keys are stored in `.env` files - ensure proper file permissions (chmod 600 on Unix)
- **Network requests**: The tool makes requests to YouTube API and Gemini API - review your network policies
- **Local file access**: The CLI requires read/write access to your Obsidian vault directory

## Security Updates

Security patches will be announced via:
- GitHub Security Advisories
- Release notes with `[SECURITY]` prefix
- Repository README updates

---

For general questions about security practices, open a [GitHub Discussion](https://github.com/freubreu88-byte/Knowledge-Dojo/discussions).
