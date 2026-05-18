# Phase 01: Preparation (15 minutes)

## Goal

Set up a clean Python development workspace for the capstone activity.

## What is a fork?

A fork is your own copy of someone else's GitHub repository. We use a fork so you can safely make changes, commit your work, and push to your own GitHub account without changing the instructor repository.

>  [!TIP]
>
> You should work in your own fork because you will not have permission to push changes directly to the instructor repository.

## Steps

1. Make sure Python is installed on your computer and your GitHub account is ready in your browser.

2. Fork the [capstone repository](https://github.com/warestack/bda-capstone-1) to your own GitHub account.

Click **Fork** on the instructor repository.

![Fork the repository on GitHub](assets/how-to-fork.png)
*Figure 1: Click **Fork** on the instructor repository.*

On the next screen, choose your GitHub account as the owner and click **Create fork**.

![Create a new fork on GitHub](assets/create-fork.png)
*Figure 2: Create the fork under your own GitHub account.*

3. On your computer, open a new, fresh VS Code window.

4. Clone your fork to your computer.

After GitHub creates your fork, copy the HTTPS clone URL from your own repository. Make sure the URL contains your GitHub username.

![Clone your forked repository](assets/clone-your-repo.png)
*Figure 3: Copy the clone URL from your fork, not the instructor repository.*

Then run:

```bash
git clone https://github.com/YOUR-USERNAME/bda-capstone-1.git
cd bda-capstone-1
```

5. Open the cloned folder in VS Code.

6. Create and activate a virtual environment.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

7. Install the dependencies in the `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Checkpoint

Before moving to Phase 02, confirm that:

- **You cloned your own fork, not the instructor repository.**

  Check your Git remote (you should see your own GitHub username in the remote URL).

  ```bash
  git remote -v
  ```

- The project folder is open in VS Code.
- You are in the correct folder (`bda-capstone-1`)
- Your virtual environment is activated.
- The dependencies were installed without errors.
