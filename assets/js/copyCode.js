const codeBlocks = document.querySelectorAll('figure > pre > code');
const copyCodeButtons = document.querySelectorAll('.copy-code-button');
copyCodeButtons.forEach((copyCodeButton, index) => {
  const code = codeBlocks[index].innerText;

  copyCodeButton.addEventListener('click', () => {
    window.navigator.clipboard.writeText(code);
    copyCodeButton.classList.remove('fa-copy');
    copyCodeButton.classList.add('fa-check');
 
    setTimeout(() => {
      copyCodeButton.classList.remove('fa-check');
      copyCodeButton.classList.add('fa-copy');
    }, 2000);
  });
});