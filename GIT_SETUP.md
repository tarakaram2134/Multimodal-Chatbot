# Git Setup and Commit Instructions

Follow these steps to initialize git, commit your code, and push it to GitHub.

## 1. Initialize Git

Open a terminal in the root directory of your project (`c:/Users/tarak/Desktop/Multimodal-ChatBot`) and run:

```bash
git init
```

## 2. Verify .gitignore

Ensure you have a `.gitignore` file (I have created one for you) so you don't commit unnecessary files like virtual environments or API keys.

## 3. Stage and Commit Your Code

Add all files to the staging area:

```bash
git add .
```

Commit the files with a message:

```bash
git commit -m "Initial commit: Add backend, frontend, and documentation"
```

## 4. Create a Repository on GitHub

1.  Go to [github.com/new](https://github.com/new).
2.  Enter a repository name (e.g., `Multimodal-ChatBot`).
3.  Choose **Public** or **Private**.
4.  **Do not** check "Initialize this repository with a README" (since we already have one).
5.  Click **Create repository**.

## 5. Connect and Push

Copy the commands shown on GitHub under "…or push an existing repository from the command line". They will look like this:

```bash
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/Multimodal-ChatBot.git
git push -u origin main
```

Run these commands in your terminal. You may be asked to sign in to GitHub.

## 6. Future Commits

When you make changes in the future, just run:

```bash
git add .
git commit -m "Description of your changes"
git push
```
