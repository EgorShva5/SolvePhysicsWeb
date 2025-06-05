let ConvertWindow = document.getElementById('ConverterWindow');

let ConvertBtn, From, ConvertTemperature, ConvertWeight, ConvertVolume, ConvertDistance, Search, Change, Close, AllItemsContainer
let Multiplier = 1.0;

let IsOpen = false;
let IsResult = false


UpdateContainerContent()
UpdateFunctions()
HideAll()
ConvertWeight.style.display = 'flex';

function UpdateContainerContent() {
    ConvertBtn = document.getElementById('konvert');
    From = document.getElementById('From');
    ConvertTemperature = document.getElementById('ConvertTemperature');
    ConvertWeight = document.getElementById('ConvertWeight');
    ConvertVolume = document.getElementById('ConvertVolume');
    ConvertDistance = document.getElementById('ConvertDistance');
    Search = document.getElementById('SearchBtn');
    Change = document.getElementById('ChangeOn');
    Close = document.getElementById('back');
    AllItemsContainer = document.getElementById('allItems'); 
}

function VisibleMode() {
    if (IsOpen == false) {
        ConvertWindow.style.display = 'flex';
        ConvertWindow.style.flexDirection = 'column';
        IsOpen = true;
    } else if(IsOpen == true) {
        ConvertWindow.style.display = 'none';
        IsOpen = false;
    };
};

function HideAll() {
    ConvertTemperature.style.display = 'none';
    ConvertWeight.style.display = 'none';
    ConvertVolume.style.display = 'none';
    ConvertDistance.style.display = 'none';
};

function ConvertResults() {
    if (IsResult == true) {
        document.getElementById('ResultTabl').remove()
        UpdateContainerContent()
        UpdateFunctions()
        AllItemsContainer.style.display = 'block'
        IsResult = false
    } else if (IsResult == false) {
        AllItemsContainer.style.display = 'none'
        let Dict = ConvertWeightFunc(parseInt(Search.value, 10), Multiplier)
        let TableResult = '<div id = "ResultTabl"> <h1 class = "SimpleText White">Результат: </h1> <table class = "SimpleTable">';
        let Keys = Object.keys(Dict);
        for (let i=0; i < Keys.length; i++) {
            TableResult += '<tr> <td>'
            TableResult += Keys[i] +'</td> <td>'
            TableResult += Dict[Keys[i]] + '</td> </tr>'
        }
        TableResult += "</table> <button id = 'BackBtn' class='SimpleBtn InputStyle' type='button'; name = 'popbtn'></button> <label class = 'MainLabel' style = 'font-size: 24px' for ='BackBtn'>Назад</label> </div> "
        ConvertWindow.innerHTML += TableResult
        let BckBtn = document.getElementById('BackBtn')
        if (BckBtn) {
            BckBtn.addEventListener('click', ConvertResults);
        }

        IsResult = true
    };
};

document.addEventListener('keydown', function(event) {
    if (event.altKey && event.code == 'KeyC') {
        VisibleMode();
    } ;
});

function UpdateFunctions() {
    Close.addEventListener('click', VisibleMode);

    ConvertBtn.addEventListener('click', function() {
        if (Search.value != '' && !(/[a-z, A-Z, а-я, А-Я]/.test(Search.value))) {
            ConvertResults();
        } else if (/[a-z, A-Z, а-я, А-Я]/.test(Search.value)) {
            alert('Строка должна содержать только цифры!');
        } else {
            alert('Введи что-нить');
        };
    });

    From.addEventListener('change', function() {
        let Result = From.value;
        switch(Result){
            case 'Температура': 
                HideAll()
                ConvertTemperature.style.display = 'flex';
                break;
            case 'Объём':
                HideAll()
                ConvertVolume.style.display = 'flex';
                break;
            case 'Расстояние':
                HideAll()
                ConvertDistance.style.display = 'flex';
                break;
            case 'Масса':
                HideAll()
                ConvertWeight.style.display = 'flex';
                break;
        };
    });

    ConvertWeight.addEventListener('change', function(){
        let Result = ConvertWeight.value;
        switch(Result){
            case 'Килограмм':
                Multiplier = 1.0;
                break;
            case 'Милиграмм':
                Multiplier = 0.000001;
                break;
            case 'Микрограмм':
                Multiplier = 0.000000001;
                break;
            case 'Грамм':
                Multiplier = 0.001;
                break;
            case "Тонн":
                Multiplier = 1000;
                break;
            case 'Килотонн':
                Multiplier = 1000000;
                break;
            case 'Карат':
                Multiplier = 0.0002;
                break;
            case 'Ньютон':
                Multiplier = 0.102;
                break;
        };
    });
}

function ConvertWeightFunc(Num, Mnojit) {
    let kg = Num * Mnojit;
    let gr = kg *1000;
    let tn = kg/1000;
    let kt = kg/1000000;
    let nut = kg * 9.8;
    let mg = kg*1000000;
    let karat = kg*5000;
    let microgr = kg*1000000000;
    let Message = {
        'Килограмм: ': Round(kg),
        'Грамм: ': Round(gr), 
        'Тонн: ': Round(tn), 
        'Ньютон(На поверхности Земли): ':  Round(nut), 
        'Милиграмм: ': Round(mg), 
        'Карат: ': Round(karat),
        'Микрограмм: ': Round(microgr),
        'Килотонн: ': Round(kt)
    };
    return Message;
};

function Round(Num, To=8) {
    return parseFloat((Num).toFixed(To), 10)
}

function ConvertVolumeFunc(Num, Mult) {
    alert('ghghghgh')
};