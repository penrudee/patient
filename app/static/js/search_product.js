$(document).ready(function(){
    var tradename=[];
    async function loadTradeName(){
        try{
            $.getJSON("/api",
            function(data,status,xhr){
                for(var i=0;i<data.length;i++){
                    tradename.push(data[i].title);
                }
            })
        }catch(error){
            console.log(error)
        }
    }
    loadTradeName().then();
    $(".searchProduct").autocomplete({
        source:tradename
    })
})  