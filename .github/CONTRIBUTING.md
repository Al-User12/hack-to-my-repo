# Contributing Guide

Welcome, and thank you for your interest in contributing! 🎉

This repository is a **safe practice ground** for making your first open source contribution. There is no way to "break" anything here, so relax and learn the workflow at your own pace.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Your First Contribution (Step by Step)](#your-first-contribution-step-by-step)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Adding a Translation](#adding-a-translation)
- [Need Help?](#need-help)

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold it. Be kind, be patient, and assume good intent.

## Ways to Contribute

You don't need to be an expert. Here are beginner-friendly ways to help:

- **Add your name** to `Contributors.md` (the classic first PR).
- **Fix a typo** or broken link in the README or any doc.
- **Improve a translation**, or add a new one under `translations/`.
- **Improve documentation** in the `gui-tool-tutorials/` or `additional-material/` folders.
- **Report a bug** via the issue tracker.

Look for issues labeled [`good first issue`](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) to get started.

## Your First Contribution (Step by Step)

1. **Fork** this repository (click the Fork button at the top right).
2. **Clone** your fork to your machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/hack-to-my-repo.git
   cd hack-to-my-repo
   ```
3. **Create a branch** for your change:
   ```bash
   git checkout -b add-my-name
   ```
4. **Make your change** (for example, add your name to `Contributors.md`).
5. **Commit** with a clear message:
   ```bash
   git add Contributors.md
   git commit -m "docs: add <your-name> to contributors list"
   ```
6. **Push** your branch:
   ```bash
   git push origin add-my-name
   ```
7. **Open a Pull Request** from your fork back to this repository.

That's it! A maintainer will review your PR and merge it. 🚀

## Pull Request Guidelines

To help us review your PR quickly:

- Keep each PR focused on **one** change.
- Use a descriptive title (e.g. `docs: fix broken link in README`).
- Fill out the PR template checklist.
- If your PR addresses an issue, mention it in the description: `Closes #123`.
- Make sure existing links and formatting still work.

We use [Conventional Commits](https://www.conventionalcommits.org/) prefixes where possible: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.

## Adding a Translation

1. Copy `README.md` into `translations/README.<language-code>.md`.
2. Translate the content (keep the links and image paths intact).
3. Add a link to your translation in `translations/Translations.md`.
4. Open a PR.

## Need Help?

If you get stuck:
- Open an issue with the `question` label.
- Describe what you tried and what happened.

No question is too small here. Happy contributing! 💙
