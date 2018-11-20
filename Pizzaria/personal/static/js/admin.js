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

function addSubmitHandler(){
    document.getElementsByName("complete").forEach(comp => {
        comp.addEventListener("submit", function(e){
            e.preventDefault();
            $.ajax({
                url: $(this).attr("action"),
                data: {
                    'message': 'pedidos',
                    'pedido': $(this).children("button[name='pedido']").attr("value"),
                    'csrfmiddlewaretoken': csrftoken
                },
                dataType: 'json',
                method: $(this).attr("method"),
                success: getUpdates
            });
        });
        comp.childNodes[0].addEventListener("click", function(){
            $(this).closest("div.grid-item").css({ "background-color" : "red"});
        });
    });
}