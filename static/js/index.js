var timeout = 41;

$(document).ready(function() {
 $("#text").keyup(function() {
     var input = $("#text")[0].value;
     var max = $("#hc")[0].innerHTML;
     updateStatusTextCharCounter(input, max);
 });

 $("#post_button").click(function(){
    text = $("#text").get(0).value;
    url = $("#post_form").attr('action');
    $("#text").attr('disabled', 'disabled');
    $("#post_button").attr('disabled', 'disabled');
    loading(true);
    $.post(url, { text: text },
      function(data){
        refresh();
        $("#post_button").removeAttr('disabled');
        $("#text").removeAttr('disabled');
        $("#text")[0].value = "";
      });

    return false;
 });

 $("#viewmore").click(function(){
    view_more();

    return false;
 });

 shover(true);
});

function loading(bool){
    if (bool)
        $("#refresh_img").css("display", "block");
    else
        $("#refresh_img").css("display", "none");
}

function refresh(){
    id = $(".sweet:first").attr("id");
    if (!id){
        id = 0;
    }
    refresh_uri = $("#refresh_uri").html();
    page = $("#pagenumber").html();
    if (page > 1)
    {
        return false;
    }
    loading(true);
    $.get(refresh_uri+"/"+id, function(data){
        $("#sweets").prepend(data);
        sweet = $(".sweet:first");
        while(sweet.attr('id') > id){
            sweet.hide();
            sweet.fadeIn("slow");
            sweet.addClass("new");
            sweet = sweet.next();
        }

        loading(false);
        shover(true);
    });
}

function view_more(){
    id = $(".sweet:last").attr("id");
    if (!id){
        id = 0;
    }
    refresh_uri = $("#refresh_uri").html();
    $("#view_more").hide();
    $("#loading_view_more").show();
    $.get(refresh_uri+"/"+id+"?viewmore=1", function(data){
        $("#sweets").append(data);
        sweet = $(".sweet:last");
        while(sweet.attr('id') < id){
            sweet.hide();
            sweet.fadeIn("slow");
            sweet.addClass("new");
            sweet = sweet.prev();
        }

        $("#loading_view_more").hide();
        $("#view_more").show();
        shover(false);
    });
}

function updateStatusTextCharCounter(value, max) {
    len = value.length;
    res = max - len;
    $('#counter').html('' + res);
    if (len > max) {
        if ($("#new").attr('disabled') != 'disabled') {
            $('#new').attr('disabled', 'disabled');
        }
    } else {
        if ($("#new").attr('disabled') == true) {
            $('#new').removeAttr('disabled');
        }

        if (res > 10) {
            $('#counter').css('color', '#999' );
        } else if (res > 5) {
            $('#counter').css('color', '#940000' );
        } else {
            $('#counter').css('color', '#f00' );
        }
    }
}

function shover(settimeout_refresh){
 $(".sweet").hover(function(){
        $(this).css("background-color", "#ffffff");
        $(this).find(".tools").show();
    },
    function(){
        $(this).css("background-color", "transparent");
        $(this).find(".tools").hide();
    });
 if (settimeout_refresh)
    mytime = setTimeout("refresh()", timeout*1000);
}
