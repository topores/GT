var text="nothing";
var resText="nothing";
var action="";
var id="";
var lastid=id;
var spot = 0;
var balance = 0;
var callPayout = 0;
var putPayout = 0;
var position = "hold"
var val=""



function call() {
    try {
        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            // query the active tab, which will be only one tab
            //and inject the script in it
            chrome.tabs.executeScript(tabs[0].id, {file: "call.js"}, function(result){
                if (result[0].indexOf("EX")!==-1){
                    sendError(result[0])
                }
            });
        });
    }
    catch (e){
        setTimeout(function(){sendError("errorWithClicking call")},100)
    }
    checkState("call")
    setTimeout(checkAction, 100)

}

function put() {
    try {
        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            // query the active tab, which will be only one tab
            //and inject the script in it
            chrome.tabs.executeScript(tabs[0].id, {file: "put.js"}, function(result){
                if (result[0].indexOf("EX")!==-1){
                        sendError(result[0])
                    }
            });
        });
    }
    catch (e){
        setTimeout(sendError("errorWithClickingPut"),100)
    }
    checkState("put")
    setTimeout(checkAction, 100)


}


function start() {
    alert(start);
    try {

        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            // query the active tab, which will be only one tab
            //and inject the script in it
            chrome.tabs.executeScript(tabs[0].id, {file: "docstart.js"},function f(res) {
                try {

                if (res[0] !== null) {
                    sendError(res[0])
                }
            } catch (e) {}
            });
        });
    }
    catch (e){
        alert("error starting code")
    }
    setTimeout(checkAction, 10)

    //checkAction()
}


function checkAction(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'iTrader.ac', true);
    xhr.onreadystatechange = function()
    {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            text=xhr.responseText
        } else {text="can not read file"}

        setTimeout(parseText, 100)
    };
    xhr.send();
}

function parseText(){
    lastid=id;
    a=text.indexOf("position:");
    b=text.indexOf("id:");
    c=text.indexOf("value:");
    action = text.slice(a+10, b-1);

    id = text.slice(b+4, c-1);
    val= text.slice(c+7, text.length-1);
    if (id!==lastid){
        setTimeout(handleAction, 10)

    } else {
        //checkState('hold')
        setTimeout(checkAction, 10)
    }

}
function handleAction() {
    position=action;
    if (action.indexOf("hold")!==-1) {
        setTimeout(checkAction, 10)
    } else if (action.indexOf("call")!==-1) {
        setTimeout(call, 10)
    } else if (action.indexOf("put")!==-1) {
        setTimeout(put, 10)
    }

}

function checkState(pos) {
    position=pos;
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        // query the active tab, which will be only one tab
        //and inject the script in it
        chrome.tabs.executeScript(tabs[0].id, {file: "parse.js"}, function handleParams(ans) {
            a=ans[0]
            spot = a["spot"];
            balance = a["balance"];
            callPayuot = a["callPayout"];
            putPayuot = a["putPayout"];
            setTimeout(sendState,100)
        });
    });


}


function sendState(){
    var xhr = new XMLHttpRequest();
    try {
        if (position==="call"){ payout=callPayout}
        else if (position==="put"){ payout=putPayout}
        else payout="NoPayout"
        params = "?spot=" + spot + "&balance=" + balance + "&position=" + position+
        "&id=" + id + "&value=" + val+"&payout=" + payout;

    } catch (e){
        params="?errcode=params_error";
    }
    url='http://localhost:8000/'+params
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function()
    {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            resText=xhr.responseText
        } else resText="can not send state"
        setTimeout(checkAction, 100);
    };
    xhr.send();
    spot = 0;
    balance = 0;
    callPayuot = 0;
    putPayuot = 0;

}


function sendError(state){
    var xhr = new XMLHttpRequest();
    url='http://localhost:8000/?errcode='+state;
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function()
    {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            resText=xhr.responseText
        } else resText="can not send error"
    };
    xhr.send();
    window.close();
}
