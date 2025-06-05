let HomeBtn = document.querySelector('.ImageButton')
let SolveBtn = document.getElementById('Solve')
let AboutUsBtn = document.getElementById('AboutUs')
let DownloadBtn = document.getElementById('Download')
let TheoryBtn = document.getElementById('TheoryBtn')
let RegistrationBtn = document.getElementById('Register')
let FeedBtn = document.getElementById('News')
let EnterBtn = document.getElementById('Enter')

HomeBtn.addEventListener('click', function() {
    window.location.href="/Main";
});

SolveBtn.addEventListener('click', function() {
    window.location.href="/SolvePt";
});

AboutUsBtn.addEventListener('click', function() {
    window.location.href="/AboutUs";
});

DownloadBtn.addEventListener('click', function() {
    window.location.href="/Download";
});

TheoryBtn.addEventListener('click', function() {
    window.location.href = "/Theory";
}); 

FeedBtn.addEventListener('click', function() {
    window.location.href="/Feed";
});

if(RegistrationBtn && EnterBtn){
    RegistrationBtn.addEventListener('click', function() {
        window.location.href = "/Register";
    }); 

    EnterBtn.addEventListener('click', function() {
        window.location.href = '/Enter'
    });
};