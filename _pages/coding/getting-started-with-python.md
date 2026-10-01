---
title: Getting Started with Python
seo_title: Getting Started with Python for Finance
excerpt: "Where to start with Python for finance: nailing down the basics so you understand how code works, and then handing more of the work to an AI assistant."
description: "Getting started with Python for finance: the basics on Kaggle, your first financial models and managing projects with Git and a code editor."
author_profile: true
permalink: /modelling/getting-started
classes: wide-sidebar
author_profile: false
sidebar:
  nav: "modelling"
---

If you are new to Python or want to get started, this page is for you. In the end, an AI assistant will write most of your code. But before you let it take over, it pays to nail down the basics yourself: how Python works, how data flows through Pandas and NumPy, and why code is written the way it is. Today's models are very capable and you can trust a lot of what they produce. Understanding the basics is what lets you follow the choices they make, steer them when you want something different and explain why your model gives the number it gives.

This page assumes you have little prior knowledge of Python or need a refresher. Once you get the hang of it, the other pages explain how to structure, test and maintain a model, and how to work with an assistant through each of those steps.

## Learning the Basics

Start with the fundamentals, and do these yourself rather than with an assistant: the point is to understand how code works, not just to get it working. If you are completely new to Python or need a refresher, I recommend going through:

- [Intro to Programming Course](https://www.kaggle.com/learn/intro-to-programming){: target="_blank"} to understand the basics of programming.
- [Python Course](https://www.kaggle.com/learn/python){: target="_blank"}, which is a concise course for Python.
- [Pandas Course](https://www.kaggle.com/learn/pandas){: target="_blank"} to understand Pandas, as it is fundamental to Python use in many industries.
- (Optional) [Machine Learning Course](https://www.kaggle.com/learn/intro-to-machine-learning){: target="_blank"}, but only if you plan on using Machine Learning in your projects.

I recommend Kaggle because it is an entirely free platform (no annoying paywalls). Familiarizing yourself with Kaggle can be a great way to start your own projects, as it offers plenty of datasets to experiment with.

{: .notice--info}
Once you have finished these courses, the most important advice I can offer is: **don't enroll in a "Python Certification" or read books solely about "How to Program in Python"**. What you need is the ability to turn a financial problem into a working model and to understand why it works. You learn that by building real projects, not from courses about syntax. Exceptions include higher-level content such as model architecture.

I recommend starting with a project that interests you. All the projects listed below originated from a personal need and taught me a lot, especially through building them in the open and receiving feedback from others.

<div class="row">
<div markdown="1" class="thirty-three-column mobile-max-column-width">

<a href="/projects/financetoolkit"><img src="https://user-images.githubusercontent.com/46355364/242269801-198d47bd-e1b3-492d-acc4-5d9f02d1d009.jpg" alt="Finance Toolkit project banner" width="400"></a>

With the **Finance Toolkit**, I wanted to see if I could improve my fundamental analysis using Python while also getting familiar with NumPy and Pandas.

</div>

<div markdown="1" class="thirty-three-column mobile-max-column-width">

<a href="/projects/financedatabase"><img src="https://user-images.githubusercontent.com/46355364/220746807-669cdbc1-ac67-404c-b0bb-4a3d67d9931f.jpg" alt="Finance Database project banner" width="400"></a>

With the **Finance Database**, I aimed to create a database to find products compatible with the Finance Toolkit functions.

</div>

<div markdown="1" class="thirty-three-column mobile-max-column-width" style="padding-right:0px">

<a href="/projects/personalfinance"><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/46355364/275324611-33a88b7d-f48f-42f0-83ae-d0950a3aed6e.jpg" alt="Personal Finance project banner" width="400"></a>

With **Personal Finance**, I wanted to understand my spending habits and determine how much money would be left at the end of the month for investing. This also allowed me to experiment with Excel and Power BI integrations.


</div>
</div>

## Installing and Working with Python

Today, most Python is written in a code editor with an AI assistant built in, and that is the setup I recommend starting with as well. The most common choice is **Visual Studio Code** with **GitHub Copilot** and/or **Claude Code**:

1. **Install Python.** Download the latest version from [python.org](https://www.python.org/downloads/){: target="_blank"}, or install [uv](https://docs.astral.sh/uv/){: target="_blank"}, which manages Python versions and packages for you and is used throughout this guide.
2. **Install [Visual Studio Code](https://code.visualstudio.com/){: target="_blank"}** and add the **Python** and **Jupyter** extensions from the Extensions view.
3. **Add an AI assistant.** Sign in to [GitHub Copilot](https://code.visualstudio.com/docs/copilot/setup){: target="_blank"}, which is built into VS Code and has a free tier, and/or install the [Claude Code](https://docs.anthropic.com/en/docs/claude-code/ide-integrations){: target="_blank"} extension. Both can explain code, answer questions about your project and, in agent mode, create and edit files and run commands for you.
4. **Open a folder and start.** Create a folder for your first project, open it in VS Code and create a file ending in `.ipynb` to start a notebook.

![VS Code with GitHub Copilot in agent mode, editing files and running tests](/assets/images/modelling/getting-started-with-python/vscode-copilot-agent.png)
<p class="image-credit">VS Code with GitHub Copilot in agent mode. Image: <a href="https://code.visualstudio.com/docs/copilot/overview" target="_blank">Visual Studio Code documentation</a>, <a href="https://creativecommons.org/licenses/by/3.0/us/" target="_blank">CC BY 3.0</a>.</p>

### Jupyter Notebooks as your Playground

While you learn the basics, a Jupyter Notebook is the best place to work. It runs code in small blocks (cells) and shows the result of each step immediately, so you can experiment with a dataset, try a calculation and see what happens. Notebooks run directly inside VS Code, so you don't need anything else. Write your first analyses here yourself, cell by cell, until reading and writing Pandas feels natural. See an example of how such a Notebook could look below.

![Jupyter Notebook](/assets/images/modelling/getting-started-with-python/notebook.png)

One of my first projects was simply a collection of Jupyter Notebooks (see [here](https://github.com/JerBouma/AlgorithmicTrading){: target="_blank"}). This was a university project where we used Python for Pairs Trading. It's by no means perfect, but it demonstrates how far you can get with notebooks alone. Once your analyses grow into something you want to reuse, you move them into `.py` files and a proper project, which is what the next pages are about.

Some tips to focus on while learning:

- **Stick to foundational packages like NumPy, Pandas, and SciPy.** These are used in almost every financial model. Hold off on Machine Learning packages like Scikit-learn until you have a solid grasp of the basics. Knowing these few packages well means you can follow almost any financial model, including the ones an assistant builds for you later.
- **Acquire (financial) datasets to experiment with**. Visit [Kaggle](https://www.kaggle.com/learn/python){: target="_blank"} or use the [Finance Toolkit](/projects/financetoolkit). Install it via `pip install financetoolkit` (or `uv add financetoolkit`), or run `%pip install financetoolkit` in a notebook cell. The examples found [here](/projects/financetoolkit) should help you get started. Since they rely on NumPy, Pandas, and SciPy, you should be able to work with the data quickly.
- **Look up anything you don't understand.** Someone has likely run into the same problem before, and the documentation of packages like Pandas is excellent.
- **Don't worry about dependency management, linters, pytest, styling, etc., initially.** Until you have a solid understanding of the basics, these tools will likely only confuse you. You will need them later to build models that last, but while you are still learning they only complicate things.

Looking for project ideas? An AI assistant can suggest plenty. Don't be discouraged if your idea has already been implemented. For example, while multiple applications similar to my Personal Finance tracker exist, I designed mine to provide the specific insights I needed.

### From the Basics to an AI Assistant

While you learn the basics, use an AI assistant as a tutor: ask it to explain an error, a Pandas function or why one approach is faster than another. Once the basics are in place, hand it more and more of the actual work. A good way to make that step:

1. **Describe the analysis, not the code.** "Calculate the 30-day rolling volatility of Apple and Microsoft and plot both" is a better request than asking for specific functions. Be clear about the finance: which prices, which period, annualised or not.
2. **Follow the choices it makes.** Read through what it built and ask why it chose a certain approach, for example a simple versus a logarithmic return, or how it handled missing days. The code itself will usually be right; the choices are where your own view matters.
3. **Change something and predict the outcome.** Change the window, a ticker or the period, predict what will happen and check. It's the fastest way to understand code you didn't type.
4. **Gradually give it more.** Start with single analyses, then whole notebooks, and eventually let it build complete models, as described in the rest of this guide.

{: .notice--info}
**Why understanding still matters**<br>An assistant can write a correct gross margin function in seconds. Whether it should use revenue or net sales, how missing quarters are treated and where the function belongs in your model are choices, and you want to understand and agree with them. That is what the rest of this guide is about.

## The Next Steps

Once you have the basics down, move from notebooks to real projects:

1. **Move from notebooks to `.py` files.** Real models consist of multiple files that interact with each other, the way packages like Pandas and NumPy are built. You already have the editor for it; the next pages explain how to organise those files. Your assistant becomes far more capable once your project has a clear structure, and from here on it does more and more of the hands-on work.
2. **Create a public or private project on a platform like [GitHub](https://github.com/){: target="_blank"}.** GitHub is a platform where over 100 million developers collaborate on open-source projects and manage Git repositories (e.g., my own [here](https://github.com/JerBouma/FinanceToolkit){: target="_blank"}). Platforms often used within companies include Azure DevOps or BitBucket, which share similar functionality. See a guide about GitHub [here](https://docs.github.com/en/get-started/using-github/hello-world){: target="_blank"}.
3. **Download [Git](https://git-scm.com/){: target="_blank"} to version control your project.** Using commands like `git add`, `git commit -m "Initial commit"`, and `git push`, you can create a version history. Your assistant will usually run these commands for you, but understand what they do: every commit is a checkpoint you can return to, which is exactly what you want when an assistant changes many files at once. The pages that follow assume you have Git set up.

Once you have completed these steps, it's time to start setting up your project. Visit [Setting up your Project](/modelling/setting-up-your-project) to continue!

[Setting up your Project](/modelling/setting-up-your-project){: .btn .btn--info .btn--large .align-center}
