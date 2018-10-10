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

function getUpdates(result){
    updatedHtml = ""
    var pedido = result['pedidos']
    for(var i = 0; i < pedido.length; i++){
        updatedHtml += "<div class='grid-item pedidos-item col-md-6 col-sm-12'>\n\t" +
                       "<p>Pizzas: ";
        if(pedido[i][1]['pizzas']!=undefined)
            updatedHtml += pedido[i][1]['pizzas'];
        updatedHtml += "</p>\n\t<p>Refrigerantes: ";
        if(pedido[i][1]['refrigerante']!=undefined)
            updatedHtml += pedido[i][1]['refrigerante'];
        updatedHtml += "</p>\n\t<p>Preço: " + pedido[i][1]['preco'] + "</p>\n\t" +
        "<p>Endereço: " + pedido[i][1]['endereco'] + "</p>\n\t" +
        "<p>Telefone: " + pedido[i][1]['telefone'] + "</p>\n\t" +
        "<p>Status: " + pedido[i][1]['status'] + "</p>\n\t" +
        "<p>Observações: " + pedido[i][1]['observacao_pedido'] + "</p>\n\t" +
        "<form name='complete' style='border-style: none; margin : 0%; : 0%;' action='" + $("#orderUrl").attr("data-url") + "' method='POST'>\n\t\t" +
        "<input type='hidden' name='csrfmiddlewaretoken' value='" + csrftoken + "'>\n\t\t" +
        "<button class='btncont btn btn-info' type='submit' name='pedido' value='" + pedido[i][0] + "'>Completo</button>\n\t" + 
        "</form>\n</div>\n";
    };

    $("#listaPedidos").html(updatedHtml);
    addSubmitHandler();
}

addSubmitHandler();
setInterval(function() { checkUpdates("pedidos", getUpdates) }, 5000);