# Publishing this repository safely

Create the repository as **private**, check it on GitHub, and make it public only when everything is right. Nobody else can see a private repository.

## 0. Fill in your details

- `LICENSE`: replace `YOUR FULL NAME`.
- `CITATION.cff`: replace `YOUR FAMILY NAME` and `YOUR GIVEN NAME`; optionally add your ORCID and affiliation.

## 1. Use only the clean notebooks

The notebooks in `notebooks/` have **no outputs**: no paintings, no printed tokens. Do not replace them with the copies you ran in Colab or Kaggle, which contain painting images in their outputs. If you edit a notebook and run it, clear its outputs before committing:

- in Jupyter or Colab: *Edit → Clear all outputs*, then save; or
- from the command line: `pip install nbstripout`, then `nbstripout notebooks/*.ipynb notebooks/supplementary/*.ipynb`.

To make Git strip outputs automatically on every commit, run `nbstripout --install` once inside the repository.

## 2. Check for secrets and images

From the repository root:

```bash
python scripts/check_before_publish.py
```

It must print `No secrets, notebook outputs, images or large files found.` before you continue.

For a second, independent check you can use [gitleaks](https://github.com/gitleaks/gitleaks):

```bash
gitleaks detect --source . --no-git -v
```

## 3. Create the local repository and first commit

```bash
cd art-training-vision-models
git init -b main
git add .
git status                      # read the list: only code, notebooks and text files should appear
git commit -m "Pilot code: labels vs exposure in DINOv2 and DINOv3"
```

## 4. Check the history before the first push

Secrets in *any* commit stay in the history even if you delete them later. Before pushing:

```bash
git log -p | grep -nE "hf_[A-Za-z0-9]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9_-]{20,}" || echo "No tokens in history"
git ls-files | grep -iE "\.(png|jpe?g|gif|webp|npz|npy|pt|pth)$" || echo "No images or data files tracked"
gitleaks detect --source . -v   # optional: scans the full Git history
```

If anything turns up, the simplest fix before the first push is to delete the `.git` folder, fix the files, and start again from step 3.

**If a token was ever pushed anywhere,** revoke it immediately on Hugging Face (Settings → Access Tokens) and create a new one. Removing it from the code is not enough.

## 5. Create the repository on GitHub as private and push

**On the website:** go to github.com/new, set the name to `art-training-vision-models`, choose **Private**, and do **not** add a README, licence or .gitignore (they already exist). Then:

```bash
git remote add origin https://github.com/Divya1205/art-training-vision-models.git
git push -u origin main
```

**Or with the GitHub CLI** (`gh auth login` first):

```bash
gh repo create Divya1205/art-training-vision-models --private --source=. --remote=origin --push
```

## 6. Check it on GitHub

While it's private, open the repository on GitHub and check:

- the README renders correctly and the results table is right;
- each notebook preview shows code and text only, no images;
- the file list contains no images, `.npz` files or anything from `results/` except its README.

## 7. Make it public

When you're satisfied: **Settings → General → Danger Zone → Change repository visibility → Public.**

Or with the CLI:

```bash
gh repo edit Divya1205/art-training-vision-models --visibility public --accept-visibility-change-consequences
```

## Pin exact versions

`requirements.txt` gives minimum versions. To record the exact versions you used, run this in the Colab or Kaggle session where the notebook worked, and save the output as `requirements-lock.txt`:

```python
!pip freeze | grep -iE "^(torch|torchvision|transformers|datasets|huggingface.hub|umap.learn|scikit.learn|scipy|numpy|pandas|matplotlib|pillow)=="
```

Mention in the README that `requirements-lock.txt` lists the exact versions used for the paper.

## Later: a citable version

When the manuscript is posted, you can connect the repository to [Zenodo](https://zenodo.org) to get a DOI for a release, and update `CITATION.cff` with it.
