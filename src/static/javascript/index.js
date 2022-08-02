function myFunction(xx) {
    /* Get the text field */
    var copyText = document.getElementById(xx);
    console.log(copyText.value)
  
    /* Select the text field */
    copyText.select();
    //copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text inside the text field */
    navigator.clipboard.writeText(copyText.value);
    
    /* Alert the copied text */
    alert("Copiado al portapapeles: " + copyText.value);
  }