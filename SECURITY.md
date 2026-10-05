# Security Policy

This project takes security issues seriously, especially because the code may parse user-generated lyric files, load local resources, and execute CLI workflows from untrusted content.

## Supported versions

We support and review security reports for:

- the latest release on the main branch
- the most recent published package release

Older versions may receive fixes only when they are still in active use and the issue is still reproducible without a significant compatibility burden.

## Reporting a vulnerability

Please do not open a public GitHub issue for a security vulnerability.

Use one of the following:

1. Preferred: GitHub Security Advisories for this repository
2. If that is not available: contact the maintainer privately through GitHub and request a secure reporting channel

When reporting, include:

- a clear description of the issue
- the affected version or commit
- reproduction steps
- affected file or module, if known
- any proof of concept or exploit details
- the impact and severity you believe it has

## What we ask you not to do

- do not disclose the issue publicly before a fix is available
- do not create a public issue containing exploit details
- do not test against third-party systems or users without permission
- do not attempt to access, modify, or exfiltrate unrelated data

## Response expectations

We will do our best to:

- acknowledge receipt within a reasonable timeframe
- assess the report and determine severity
- work toward a fix or mitigation
- communicate the status privately during remediation
- coordinate disclosure once the fix is ready

## Security-sensitive areas in this project

Given the project’s nature, the most relevant concerns are:

- unsafe parsing of lyric files or user-provided text
- command execution through CLI options or scripts
- local file access beyond intended project boundaries
- dependency or package supply-chain issues
- crashes or denial-of-service caused by malformed input

## Disclosure policy

We prefer coordinated disclosure. Once a fix is validated and released, we may publish a brief summary in the changelog or release notes without exposing sensitive exploit details.

Thank you for helping keep the project safe.
