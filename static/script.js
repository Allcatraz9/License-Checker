Document.getElementById('form-fill').addEventListener('submit',function(event){
    event.preventDefault();
    alert("Form Submitted Successfully!");
    window.location.href='submit';
});
console.log(Document.getElementById('form-fill'));

