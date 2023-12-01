---
title: Financial Modelling with Python
excerpt: Explore Financial Modeling with Python, develop robust models, avoid pitfalls, and learn from practical experience for professional insights.
description: Explore Financial Modeling with Python, develop robust models, avoid pitfalls, and learn from practical experience for professional insights.
author_profile: true
permalink: /modelling/introduction
classes: wide-sidebar
redirect_from:
  - /modelling
  - /literature
author_profile: false
sidebar:
  nav: "modelling"
---

<script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">

Python, a versatile and powerful programming language, has made significant inroads into the financial industry in recent years. Its simplicity, readability, and extensive libraries have made it a favorite tool for financial analysts, quantitative researchers and myself as I have spend thousands of hours by now in Python using it for both personal and institutional purposes.

</div>

<div markdown="1" class="fourty-column mobile-max-column-width show-on-desktop">

![](/assets/images/modelling/FinancialModelling.png)

</div>
</div>

With that, I've acquired a solid understanding of how to design models and algorithms that are tailored to the needs of the financial industry both in terms of financial sophistication as well as creating model structures that are robust, effective and easily maintainable. Especially in the area of keeping the model up-to-date and making sure that it is able to handle new data and new situations, I have made plenty of mistakes and learned a lot from them. With that said, these pages are about sharing my knowledge and experience with you so that you can avoid making the same mistakes I did.

Within this financial modelling guide you can find information how to get started with Python, how to set up a project and structure, build and test a model. Here, I share what has worked well for me from what I've gathered from several employers. The contents can be found on the left-hand side of this page as well as by clicking on the different buttons below which appear on every page.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,color:white,radius:20px,font-weight:bold;
classDef currentfont fill:#d67f05,stroke-width:0px,color:white,radius:20px,font-weight:bold;

Step0[<a href="/modelling/introduction" style="color:white;text-decoration:none">Introduction</a>]:::currentfont --> Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>]:::boxfont

Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>] --> Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>]:::boxfont

Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>] -->  Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>]:::boxfont

Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>] --> Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>]:::boxfont

Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>] <--> Step5[<a href="/modelling/test-your-model" style="color:white;text-decoration:none">Test your Model</a>]:::boxfont
</div>

{: .notice--info}
**Financial Literature**<br>Most of the modelling I do is based on a solid amount of financial literature. The Notion page below serves as my repository for the literature that captures my interest, primarily focusing on investing, economics, and behavioral finance. I strive to include public links within the page, allowing easy access to the documents for further reading.<br><br>[Visit My Notion Page](https://resolute-cowbell-004.notion.site/74edba0752fa4037aa22116afbe0e29d?v=be67f50a79e34f68891bfda3086a4bb4){: .btn .btn--info target="blank"}<br><br>[![Jeroen Bouma's Notion Page](/assets/images/literature/notion.png)](https://resolute-cowbell-004.notion.site/74edba0752fa4037aa22116afbe0e29d?v=be67f50a79e34f68891bfda3086a4bb4){: target="_blank"}

Have suggestions? This entire website is open-source so feel free to contribute [here](https://github.com/JerBouma/jerbouma.github.io){:, target="blank"}!