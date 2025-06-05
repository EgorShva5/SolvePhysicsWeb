let AllTheory = document.querySelectorAll('.TheoryBtn')
let SearchBtn = document.getElementById('textsearch')
let SearchEdit = document.getElementById('linesearch')

function TheoryShow() {
    for (let i = 1; i < AllTheory.length; i++) {
        if (AllTheory[i].querySelector('h1').innerText.includes(SearchEdit.value)) {
            AllTheory[i].style.display = 'flex';
        } else {
            AllTheory[i].style.display = 'none';
        };
    };
}

SearchBtn.addEventListener('click', TheoryShow);

SearchEdit.addEventListener('keypress', function(event){
    if(event.keyCode==13){
        TheoryShow();
        event.preventDefault();
    };
});

