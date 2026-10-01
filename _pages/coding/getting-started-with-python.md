---
title: Getting Started with Python
seo_title: Getting Started with Python for Finance
excerpt: "Where to start with Python: the basics on Kaggle, first project ideas for financial models, using AI assistants as a tutor, and tips on Git and code editors."
description: "Getting started with Python for finance: the basics on Kaggle, your first financial models and managing projects with Git and a code editor."
author_profile: true
permalink: /modelling/getting-started
classes: wide-sidebar
author_profile: false
sidebar:
  nav: "modelling"
---

If you are new to Python or want to get started, this page is for you. I will cover the basics of Python, how to begin using it and how to make good use of AI assistants while you learn. I will also share some tips I have picked up over the years.

This page assumes you have little prior knowledge of Python or need a refresher. Perhaps you have become accustomed to working with Jupyter Notebooks and are looking for the next step. Once you get the hang of it, the other pages explain how to structure, test and maintain a model.

## Learning the Basics

If you are completely new to Python or need a refresher, I recommend going through:

- [Intro to Programming Course](https://www.kaggle.com/learn/intro-to-programming){: target="_blank"} to understand the basics of programming.
- [Python Course](https://www.kaggle.com/learn/python){: target="_blank"}, which is a concise course for Python.
- [Pandas Course](https://www.kaggle.com/learn/pandas){: target="_blank"} to understand Pandas, as it is fundamental to Python use in many industries.
- (Optional) [Machine Learning Course](https://www.kaggle.com/learn/intro-to-machine-learning){: target="_blank"}, but only if you plan on using Machine Learning in your projects.

I recommend Kaggle because it is an entirely free platform (no annoying paywalls). Familiarizing yourself with Kaggle can be a great way to start your own projects, as it offers plenty of datasets to experiment with.

{: .notice--info}
Once you have finished these courses, the most important advice I can offer is: **absolutely do <u>not</u> enroll in any "Python Certification", watch someone else code, or read books solely about "How to Program in Python"**. Learning Python means learning how to solve problems with it, and the syntax is only a small part of that. You acquire this skill through practice, which courses, videos, or books about the process cannot replace. The same goes for AI assistants: letting one write all your code is the modern version of watching someone else code. Exceptions include higher-level content such as model architecture.

I recommend starting with a project that interests you. All the projects listed below originated from a personal need and helped me develop my Python skills a lot, especially through building open-source projects and occasionally receiving feedback from others.

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

To get started, download the Anaconda Distribution and use a Jupyter Notebook as follows:

1. Go to [https://www.anaconda.com/download](https://www.anaconda.com/download){: target="_blank"} and install the application.
2. Open the "Anaconda Navigator" and launch "Jupyter Notebook". Alternatively, use `jupyter notebook` in the command line.
3. Create a new notebook and start coding!

Jupyter Notebooks should be your primary tool until you have familiarized yourself well with the syntax. See an example of how such a Notebook could look below.

![Jupyter Notebook](/assets/images/modelling/getting-started-with-python/notebook.png)

One of my first projects was simply a collection of Jupyter Notebooks (see [here](https://github.com/JerBouma/AlgorithmicTrading){: target="_blank"}). This was a university project where we used Python for Pairs Trading. It's by no means perfect, but it demonstrates the utility of Jupyter Notebooks for getting started.

{: .notice--info}
**Why work with Jupyter Notebooks?**<br>Jupyter Notebooks are popular because you can easily run code in blocks and see the output immediately. This allows for experimentation and quick feedback. Once you are more familiar with the syntax, you can transition to a code editor like Visual Studio Code or PyCharm. These editors also support Jupyter Notebooks, which remain useful for debugging functions and testing code.

Some tips to focus on while learning Python:

- **Work primarily with foundational packages like NumPy, Pandas, and SciPy.** These packages are commonly used in most projects. Hold off on Machine Learning packages like Scikit-learn or TensorFlow until you have a solid grasp of the basics. You don't want to constantly copy and paste code from StackOverflow without understanding it.
- **Acquire (financial) datasets to experiment with**. Visit [Kaggle](https://www.kaggle.com/learn/python){: target="_blank"} or use the [Finance Toolkit](/projects/financetoolkit). Install it via `pip install financetoolkit` or use `!pip install financetoolkit` in a Jupyter Notebook. The examples found [here](/projects/financetoolkit) should help you get started. Since they rely on NumPy, Pandas, and SciPy, you should be able to work with the data quickly.
- **Look up anything you don't understand.** Someone has likely run into the same problem before, and the documentation of packages like Pandas is excellent.
- **Don't worry about dependency management, linters, pytest, styling, etc., initially.** Until you have a solid understanding of the basics, these tools will likely only confuse you. You will need them later to build models that last, but while you are still learning they only complicate things.

Looking for project ideas? An AI assistant can suggest plenty. Don't be discouraged if your idea has already been implemented. For example, while multiple applications similar to my Personal Finance tracker exist, I designed mine to provide the specific insights I needed.

### Learning with an AI Assistant

AI assistants like ChatGPT, Claude or GitHub Copilot are excellent teachers, as long as you use them to understand code and not only to produce it. Don't avoid them out of concern about "cheating"; you will use them in practice too. What matters is that you can explain every line that ends up in your model. Some ways to use them while learning:

- **Ask for explanations, not just solutions.** When you are stuck, ask why your code fails and what the fix does, instead of only asking for working code. Ask it to explain a function from Pandas or NumPy with a small example.
- **Write it first, then compare.** Try a calculation yourself, such as a rolling volatility or a gross margin over time, and then ask the assistant how it would write it. The differences are often where you learn the most.
- **Check the finance as well as the code.** Assistants are fluent but can be confidently wrong about a formula, a sign convention or whether a ratio uses annual or quarterly data. Verify calculations against a textbook, the original source or a value you calculated by hand.
- **Don't keep code you can't explain.** If you couldn't rewrite a generated piece of code yourself, ask the assistant to walk you through it until you could. Remember that code is read much more often than it is written, also by you, months later.

{: .notice--info}
**Why understanding still matters**<br>An assistant can write a working gross margin function in seconds. Knowing whether it should use revenue or net sales, how it treats missing quarters and where it belongs in your model is still up to you. That is exactly what the rest of this guide is about.

## The Next Steps

Once you are comfortable working with Python, you can start using the following tools to improve your programming skills and code quality:

1. **Install a Code Editor like Visual Studio Code or PyCharm.** These editors help in building actual models using `.py` files and make it easier to work with multiple files that interact with each other. Packages like Pandas and NumPy, which you've likely used, are developed using such editors as they involve multiple interacting files. Most editors now integrate AI assistants (for example GitHub Copilot in VS Code, or editors built around them such as Cursor), and tools like Claude Code can work on a whole project from the terminal. These become far more useful once your project has a clear structure, as described in the next pages.
2. **Create a public or private project on a platform like [GitHub](https://github.com/){: target="_blank"}.** GitHub is a platform where over 100 million developers collaborate on open-source projects and manage Git repositories (e.g., my own [here](https://github.com/JerBouma/FinanceToolkit){: target="_blank"}). Platforms often used within companies include Azure DevOps or BitBucket, which share similar functionality. See a guide about GitHub [here](https://docs.github.com/en/get-started/using-github/hello-world){: target="_blank"}.
3. **Download [Git](https://git-scm.com/){: target="_blank"} to version control your project.** Using commands like `git add`, `git commit -m "Initial commit"`, and `git push`, you can create a version history. This makes it possible to track project evolution and revert changes if necessary. You will need Git, and the pages that follow assume you have it set up.

Once you have completed these steps, it's time to start setting up your project. Visit [Setting up your Project](/modelling/setting-up-your-project) to continue!

[Setting up your Project](/modelling/setting-up-your-project){: .btn .btn--info .btn--large .align-center}
