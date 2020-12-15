function clear(){
    document.getElementById('result').innerHTML="";
}

function searchData(){
    var cont = $('#content').val();
    $.ajax({
        url:'/search/'+cont,
        type:'GET',
        contentType: 'application/json',
        dataType:'json',
        success: function(response){
            alert(JSON.stringify(response));
            var i = 0;
            $.each(response, function(){
                f = '<a class="alert alert-primary">';
                f = f + response[i];
                f = f + '</a>';
                i = i+1;
                $('#result').append(f);
            });
        },
        error: function(response){
            alert(JSON.stringify(response));
        }
    });
}