$(document).ready(function(){
    $('#search_image').change(function(event){
        $(this).parents('form').submit();
    });
});