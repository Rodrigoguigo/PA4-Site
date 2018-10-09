function changeTab(pizzaName, tabName){
    var i, tabcontent;

    tabcontent = document.getElementsByClassName(pizzaName + "Tab");
    console.log(tabcontent);
    for(i=0; i<tabcontent.length; i++)
        tabcontent[i].style.display = "none";

    document.getElementById(pizzaName + tabName).style.display = "block";
}

var i, itemsList = document.getElementsByName("defaultOpen");
console.log(itemsList);
for(i=0; i<itemsList.length; i++)
    itemsList[i].click();

$(function(){
    $("#remove").on('submit', function(e){
        if(!confirm("Remover do cardápio?"))
            return false;
    });
});