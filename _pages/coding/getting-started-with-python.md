---
title: Getting Started with Python
excerpt: All of my talks, both personal and professional, are included here. This include presentations at a variety of universities and webinars.
description: All of my talks, both personal and professional, are included here. This include presentations at a variety of universities and webinars.
author_profile: true
permalink: /modelling/getting-started
classes: wide-sidebar
author_profile: false
sidebar:
  nav: "modelling"
---

<script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>

If you are new to Python or want to get started with Python, this page is for you. I will go over the basics of Python and how to get started with it. I will also share some tips and tricks that I have learned over the years.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,color:white,radius:20px,font-weight:bold;
classDef currentfont fill:#d67f05,stroke-width:0px,color:white,radius:20px,font-weight:bold;

Step0[<a href="/modelling/introduction" style="color:white;text-decoration:none">Introduction</a>]:::boxfont --> Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>]:::currentfont

Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>] --> Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>]:::boxfont

Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>] -->  Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>]:::boxfont

Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>] --> Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>]:::boxfont

Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>] <--> Step5[<a href="/modelling/test-your-model" style="color:white;text-decoration:none">Test your Model</a>]:::boxfont
</div>

This page assumes you have little knowledge about how to work with Python or need a refresher. Perhaps you just got used to working with Jupyter Notebooks and are looking for the next step. Once you get the hang of it, you can visit the other pages to understand how to structure, test and maintain a model.

## Learning the Basics

If you are completely new to Python or need a refresher, I recommend to go through:

- [Intro to Programming Course](https://www.kaggle.com/learn/intro-to-programming){: target="_blank"} to understand the basics of programming.
- [Python Course](https://www.kaggle.com/learn/python){: target="_blank"} which is a very to the point course for Python.
- [Pandas Course](https://www.kaggle.com/learn/pandas){: target="_blank"}  to understand Pandas as it is the bread and butter of Python in basically any industry.
- (Optional) [Machine Learning Course](https://www.kaggle.com/learn/intro-to-machine-learning){: target="_blank"} but only do so if you plan on using Machine Learning in your projects.

I recommend Kaggle because it is an entirely free platform (thus no annoying paywalls) and by familising yourself with Kaggle, it can be a great place to get started with your own projects given there are plenty of datasets over there to experiment with.

{: .notice--info}
Once you have finished these courses, the number one advice I want to give is that **you absolutely should <u>not</u> enroll in any form of "Python Certification", watch someone else code or read books about "How to Program in Python"**. Learning Python is not about learning the syntax, it is about learning how to solve problems with Python. This is something you can only learn by doing and not by courses, watching videos or reading books how to do it. Exceptions are higher level content such as model architecture.

I recommend to start with a project that you are interested in and start working on it. All of the projects listed below came out of a personal need and have allowed me to really develop my Python skills especially through building in open-source, receiving feedback from others occasionally.

<div class="row">
<div markdown="1" class="thirty-three-column mobile-max-column-width">

With the **Finance Toolkit** I wanted to see if I could improve my own fundamental analysis through Python while in the meantime getting the hang of NumPy and Pandas.

<a href="/projects/financetoolkit"><img src="https://user-images.githubusercontent.com/46355364/242269801-198d47bd-e1b3-492d-acc4-5d9f02d1d009.jpg" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jerbouma&repo=financetoolkit)](/projects/financetoolkit)

</div>

<div markdown="1" class="thirty-three-column mobile-max-column-width">

With the **Finance Database** I wanted to see if I could create a database that would allow me to find the products that I could then use with the functions of the Finance Toolkit.

<a href="/projects/financedatabase"><img src="https://user-images.githubusercontent.com/46355364/220746807-669cdbc1-ac67-404c-b0bb-4a3d67d9931f.jpg" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jerbouma&repo=financedatabase)](/projects/financedatabase)

</div>

<div markdown="1" class="thirty-three-column mobile-max-column-width" style="padding-right:0px">

With **Personal Finance** I wanted to understand my spending habits and how much money would be left by the end of the month to use for investing. This also allowed me to experiment with Excel and PowerBI integrations.

<a href="/projects/personalfinance"><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/46355364/275324611-33a88b7d-f48f-42f0-83ae-d0950a3aed6e.jpg" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jerbouma&repo=personalfinance)](/projects/personalfinance)
</div>
</div>

## Installing and Working with Python

To get started, acquire the Anaconda Distribution and use a Jupyter Notebook as follows:

1. Go to [https://www.anaconda.com/download](https://www.anaconda.com/download){: target="_blank"} and install the application.
2. Open up the "Anaconda Navigator" and launch the "Jupyter Notebook". Alternatively, use `jupyter notebook` in the command line.
3. Create a new notebook and start coding!

Jupyter Notebooks should be your go-to until your familiarized yourself well with the syntax. See an example of how such a Notebook could look like below.

![Jupyter Notebook](/assets/images/modelling/getting-started-with-python/notebook.png)

One of my first projects was just a combination of Jupyter Notebooks (see [here](https://github.com/JerBouma/AlgorithmicTrading){: target="_blank"}). This was a University project in which we had to use Python to perform Pairs Trading. It is by no means perfect but it demonstrates the elegance of a Jupyter Notebook and how it can be used to get started.

{: .notice--info}
**Why work with Jupyter Notebooks?**<br>The reason Jupyter Notebooks are so popular is because you can easily run code in blocks and see the output immediately. This allows you to experiment with code and see what it does. Once you are more familiar with the syntax, you can start using a code editor such as Visual Studio Code or PyCharm. These editors also support Jupyter Notebooks as the Notebooks remain the go-to for debugging functions and testing code.

Some tips to focus on while learning Python:

- **Work primarily with the largest packages which are NumPy, Pandas and SciPy.** In basically any project, these packages tend to be there. I would not recommend trying to work with Machine Learning packages such as Scikit-learn or TensorFlow until you have a solid understanding of the basics. The last thing you want is constantly copy + pasting code from StackOverflow without understanding what it does.
- **Acquire (financial) datasets to experiment with**. For example visit [Kaggle](https://www.kaggle.com/learn/python){: target="_blank"} or use the [Finance Toolkit](/projects/financetoolkit). You can do so through `pip install financetoolkit` or in a Jupyter Notebook use `!pip install financetoolkit`. The examples as found [here](/projects/financetoolkit) should get you going quickly and as all of it relies on NumPy, Pandas and SciPy, you should be able to work with the data rather quickly.
- **Google any issue you don't understand.** Someone will definitely have had the same issue and there will be a solution for it. This is also were the open-source community shines given that there is a solution for nearly everything.
- **Definitely use ChatGPT whenever you are stuck with your code.** While ChatGPT (or any similar application) can write all of your code, the quality tends to vary a lot and in the end: code is read much more often that it is written. Therefore, I recommend to use ChatGPT to fix mistakes and get a general idea of how to solve a problem but then write the code yourself. Don't limit yourself by not using Artificial Intelligence (AI) because it could be seen as "cheating" or not being your own work.
- **Don't bother with dependency management, linters, pytest, styling and more**. Until you have a solid understanding of the basics, it will only confuse you. Even though these are all things that are very crucial to have once you develop a proper model it will only complicate things for you when you are still learning.

Looking for Project ideas? Google and ChatGPT should have plenty. Also, don't be discouraged if it has already been created. For example there are multiple applications similar to my Personal Finance tracker but I have made it the way it gives me the most insights.

## The Next Steps

Once you got the hang of working with Python, you can start utilising the following to level up your programming experience and quality.

1. **Install a Code Editor like Visual Studio Code or PyCharm.** These help in designing actual models through `.py` files and can work together. As you have used packages like Pandas and NumPy, these are built through these code editors given that multiple files interact with each other. 
2. **Create a public or private project on a platform like [GitHub](https://github.com/){: target="_blank"}.** This is a platform where 100+ million developers come together to contribute to the open-source community and manage Git repositories (e.g. my own [here](https://github.com/JerBouma/FinanceToolkit){: target="_blank"}). A platform often used within companies is Azure DevOps or BitBucket which shares similar functionality. See a guide about GitHub [here](https://docs.github.com/en/get-started/quickstart/hello-world){: target="_blank"}.
3. **Download [Git](https://git-scm.com/){: target="_blank"} to version control your project.** Through `git add`, `git commit -m Initial Commit` and `git push` you can create a version history making it possible to understand how the project has evolved and, possibly, revert changes that shouldn't have been made. Using Git is extremely important and on the other pages I assume you have this setup.

Once you have done these steps it's time to start set up your project. Visit [Setting up your Project](/modelling/setting-up-your-project) to continue!

[Setting up your Project](/modelling/setting-up-your-project){: .btn .btn--info .btn--large .align-center}
