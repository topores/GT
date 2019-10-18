ex1="EXstocksAreClosed"
ex2="EXerrorClickingTheButton"

function closePopup(){
    document.getElementById("close_confirmation_container").click()
}

if (document.getElementsByClassName("col contract_error")[0].innerText.indexOf("Trading on forex")!==-1){
    ex1;
} else {
    try{
document.getElementById("purchase_button_bottom").click()
setTimeout(closePopup,5000)
    }
    catch (e){
        ex2;
    }
}