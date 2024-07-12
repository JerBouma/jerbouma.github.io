---
title: Interactive Dashboard
permalink: /projects/financetoolkit/interactive-dashboard
excerpt: The Interactive Dashboard is a Streamlit app that contains the Finance Toolkit and allows you to interact with the different modules.
description: The Interactive Dashboard is a Streamlit app that contains the Finance Toolkit and allows you to interact with the different modules.
classes: wide-no-sidebar no-title
author_profile: false   
---

<style>
    html, body {
        width: 100%;
        padding: 0px;
    }
    iframe {
        width: 100%;
        height: 600vh;
        overflow: hidden;
        margin: 0px;
        padding: 0px;
        border: none;
    }

    @keyframes fadeInOut {
        0% { opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { opacity: 0; }
    }

    .fade-text {
        animation: fadeInOut 3s ease-in-out forwards;
    }
</style>

{: .notice--info}
<div id="fadeText" class="fade-text">
    🛠️ Please wait while the Finance Toolkit Dashboard is loading..
</div>

<script>
    setTimeout(() => {
        const fadeTextElement = document.getElementById('fadeText');
        if (fadeTextElement) {
            fadeTextElement.remove();
        }
    }, 3000); // Matches the 6s animation duration
</script>


<iframe name="iframe1" id="iframe1" src="https://financetoolkit.streamlit.app?embed=true" frameborder="0"></iframe>
