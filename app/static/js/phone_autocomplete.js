$(document).ready(function(){
    var patient=[];
    
    function getPatientInfo(){
        $.getJSON("/api_patient",function(data){
            for(var i=0;i<data.length;i++){
                console.log("data: ",data[i].phone_no); //data[i].key //key มาจาก as_dict
                patient.push(data[i].phone_no);
                console.log("patient list: ",patient);
            }
        });
    };
    getPatientInfo();
    
    $('#telephone-autocomplete').autocomplete({
        source:patient,minLength:2
    })//autocomplete
});