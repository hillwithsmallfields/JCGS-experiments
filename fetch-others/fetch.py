#!/usr/bin/env python3

import os
import subprocess

REPOS = ["https://github.com/scipy/scipy",
         "https://github.com/numpy/numpy",
         "https://github.com/scikit-learn/scikit-learn",
         "https://github.com/pandas-dev/pandas",
         "https://github.com/scikit-image/scikit-image",
         "https://github.com/cupy/cupy",
         "https://github.com/facebookresearch/fastText",
         "https://github.com/keras-team/keras",
         "https://github.com/explosion/spaCy",
         "https://github.com/tensorflow/tensorflow",
         "https://github.com/pytorch/pytorch",
         "https://github.com/Lightning-AI/pytorch-lightning",
         "https://github.com/langchain-ai/langchain",
         ]

for repo in REPOS:
    directory, name = repo.removeprefix("https://github.com/").split("/")
    holder = os.path.join(os.path.expanduser("~/open_projects/github.com"), directory)
    os.makedirs(holder, exist_ok=True)
    print("getting", repo)
    subprocess.run(["git", "clone", repo], cwd=holder)
