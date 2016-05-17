Creator = function () {
    var csrfToken;

    function init(_csrfToken) {
        csrfToken = _csrfToken;

        var submitButton = document.getElementById("submit");
        submitButton.addEventListener("click", submit);
    }

    function handleSubmitResponse(data) {
        console.log(data);
    }

    function submit() {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function () {
            if (ajax.readyState == 4 && ajax.status == 200) {
                var response = JSON.parse(ajax.responseText);
                console.log(response);
            }
        };
        ajax.open("POST", "../submit-new/", true);
        ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        ajax.setRequestHeader("X-CSRFToken", csrfToken);
        var data = "solution=123";
        data += "&pattern=123";
        ajax.send(data);
    }

    return {
        init: init
    }
}();