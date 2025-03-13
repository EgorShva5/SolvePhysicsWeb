let HomeBtn = document.querySelector('.ImageButton')
let SolveBtn = document.getElementById('Solve')
let AboutUsBtn = document.getElementById('AboutUs')
let DownloadBtn = document.getElementById('Download')

HomeBtn.addEventListener('click', function() {
    window.location.href="/Main";
});

SolveBtn.addEventListener('click', function() {
    window.location.href="/SolvePart";
});

AboutUsBtn.addEventListener('click', function() {
    window.location.href="/AboutUs";
});

DownloadBtn.addEventListener('click', function() {
    window.location.href="/Download";
});