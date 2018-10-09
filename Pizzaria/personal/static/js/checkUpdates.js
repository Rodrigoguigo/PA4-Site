var csrftoken = getCookie('csrftoken');

//Getting csrf token
function getCookie(name){
    var cookieValue = null;
    if(document.cookie && document.cookie!==''){
        var cookies = document.cookie.split(';');
        for(var i=0; i<cookies.length; i++){
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function checkUpdates(data, callback){
    $.ajax({
        url: $("#url").attr("data-url"),
        type: "POST",
        data: {
            'message': data,
            'csrfmiddlewaretoken': csrftoken
        },
        dataType: 'json',
        success: callback
    });
}