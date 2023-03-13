# Contributors Guidelines

## Setting up the dev environment

1. Clone the repository to your local machine:
```bash
 git clone https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api.git
 cd orkg-nlp-api
```

2. Create a virtual environment with `python=3.8`, activate it, install the required
   dependencies and install the pre-commit configuration:

```bash
conda create -n orkg_nlp_api python=3.8
conda activate orkg_nlp_api
pip install -r requirements.txt
pre-commit install
```

3. Create a branch and commit your changes:
```bash
git switch -c <name-your-branch>
# do your changes
git add .
git commit -m "your commit msg"
git push
```
