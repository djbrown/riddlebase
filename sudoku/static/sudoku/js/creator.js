var Creator = (function () {
    var csrfToken;

    function handleSubmitResponse(json) {

    }

    function submit() {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function () {
            if (ajax.readyState === 4 && ajax.status === 200) {
                handleSubmitResponse(JSON.parse(ajax.responseText))
            }
        };
        ajax.open("POST", "../submit-new/", true);
        ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        ajax.setRequestHeader("X-CSRFToken", csrfToken);

        var data = "solution=123";
        data += "&pattern=123";
        ajax.send(data);
    }

    function init(_csrfToken) {
        csrfToken = _csrfToken;

        var submitButton = document.getElementById("submit");
        submitButton.addEventListener("click", submit);
    }

    return {
        init
    }
}());