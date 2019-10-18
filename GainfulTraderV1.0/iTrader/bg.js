window.onload = function() {
    chrome.tabs.onUpdated.addListener(function(id, info, tab) {
    s()
    });
}

function s() {
    start();
}