$('#addInput').click(function(){
    var html='';
    html += '<div id="controll-allergy" class="controll-allergy" style="margin-bottom:5px;">';
        html += '<div class="row">';
            html+='<div class="col-btn">';
                html += '<button id="removeInput" class="btn btn-danger btn-sm">';
                html += '<i class="bi bi-x-circle"></i></button>';
                
            html+='</div>';
            html+='<div class="col-input">';
                html += '<input type="text" name="allergy">';
            html+='</div>';
        html += '</div>';
    html += '</div>';
   
    $("#newRow").append(html);
});
$(document).on('click','#removeInput',function(){
    $(this).closest("#controll-allergy").remove();
});