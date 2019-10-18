var ans = {};

ans["spot"] = document.getElementById("spot").innerText;
var callPayout = document.getElementsByClassName("col price_comment")[0].innerText;
var putPayout = document.getElementsByClassName("col price_comment")[1].innerText;

a=callPayout.indexOf("Return");
ans["callPayout"]=callPayout.substring(a+7,callPayout.length);
a=putPayout.indexOf("Return");
ans["putPayout"]=callPayout.substring(a+7,callPayout.length);

ans["balance"] = document.getElementsByClassName("topMenuBalance")[0].innerText;
ans["balance"]=ans["balance"].replace(",","");

ans["start"] = document.getElementsByClassName("select-dropdown")[0].innerText;
ans["timeType"] = document.getElementsByClassName("select-dropdown")[1].innerText;
ans["timeAmount"] = document.getElementById("duration_amount").value;
ans["timeUnit"] = document.getElementsByClassName("select-dropdown")[2].innerText;
ans["payoutType"] = document.getElementsByClassName("select-dropdown")[5].innerText;
ans["timeAmount"] = document.getElementById("amount").innerText;

ans
