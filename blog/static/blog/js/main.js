// Submit post on submit
$("#myidname").on("submit", function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    create_post();
});
var csrftoken = Cookies.get('csrftoken');
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

// AJAX for posting
function create_post() {
    console.log("create post is working!") // sanity check
    var name = $("#id_name").val();
    var body = $("#id_body").val();
    $.ajax({
        url: $(this).attr('action'), // the endpoint
        type : "POST", // http method
        data: {
            name: name,
            body: body
        },
        // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#id_name').val(''); // remove the value from the input
            $('#id_body').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if (json.success == true && json.up_comment == 1) {
                $("#spanone").replaceWith('<span id="spanone">1 Comment so far</span>');
                $('<ul><li><div class="preview"><img src="/static/blog/images/mike.png" alt=""></div>\
                   <div class="data"><div class="title">'+json.name+'<a>'+json.created+'</a></div>\
                   <p>'+json.body+'</p></div><div class="clear"></div></li></ul>').insertAfter("#internal h2");
            }
            else if (json.success == true && json.up_comment == 2) {
                $("#spantwo").replaceWith('<span id="spantwo">2 Comments so far</span>');
                $("#internal ul").last().append('<li><div class="preview"><img src="/static/blog/images/mike.png" alt=""></div>\
                                                 <div class="data"><div class="title">'+json.name+'<a>'+json.created+'</a></div>\
                                                 <p>'+json.body+'</p></div><div class="clear"></div></li>');
            }
            else {
                if (json.success == true){
                    // $("#internal ul").last().append('<li>'+json.name+'<em>'+json.body+'</em>'+json.created+'</li>');
                    $("#internal ul").last().append('<li><div class="preview"><img src="/static/blog/images/mike.png" alt=""></div>\
                                                     <div class="data"><div class="title">'+json.name+'<a>'+json.created+'</a></div>\
                                                     <p>'+json.body+'</p></div><div class="clear"></div></li>');
                    $('html, body').animate({
                        scrollTop: $("#li_comment li:nth-last-child(2)").offset().top
                    }, 500);
                    $("#spantwo").replaceWith('<span id="spantwo">'+json.up_comment+' Comments so far</span>');
                    //$("#thisspan").replaceWith("<span id='thisspan'>"+json.up_comment+"Comment{{ total_comments|pluralize }} so far</span>");
                    //window.location.reload();
                }
                else if (json.success == false){
                    // handle a non-successful response
                    //error : function(data) {
                    //$('#internal ul').prepend(data); // add the error to the dom
                    console.log(json); // provide a bit more info about the error to the console
                    //}
                }
            }
        }

    });
};

