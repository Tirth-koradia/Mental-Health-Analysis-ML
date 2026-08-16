# GitHub Repository Import Rule

When pulling or copying code from an external/third-party GitHub repository for the user:
1. **Never preserve original `.git` history or commits**.
2. **Download/Clone project files** into the working directory.
3. **Remove `.git` directory entirely** (`rm -rf .git`).
4. **Configure user identity**: Ensure `git config user.name "Tirth-koradia"` and `git config user.email "tirthkoradia4@gmail.com"` are set.
5. **Initialize fresh repository**: Run `git init`, `git add -A`, and `git commit -m "Initial commit"`.
6. **Push freshly**: Create/link the target repository on GitHub and push the single initial commit.

This ensures zero historic metadata, zero external commit authors, and 100% clean contributor history under the user's account.
