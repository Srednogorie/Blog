// Submit post on submit
$("#myidemail").on("submit", function(event){
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
    var email = $("#sign_email").val();
    $.ajax({
        url: $("#myidemail").attr('action'), // the endpoint
        type : "POST", // http method
        data: {
            email: email
        },

        // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#sign_email').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check

            if (json.success == true) {
                $("#grid2_bottom_one").replaceWith('<p id="grid2_bottom_one">'+json.message+'</p>');
                //$('<ul><li><div class="preview"><img src="/static/blog/images/mike.png" alt=""></div>\
                //<div class="data"><div class="title">'+json.name+'<a>'+json.created+'</a></div>\
                //<p>'+json.body+'</p></div><div class="clear"></div></li></ul>').insertAfter("#internal h2");
            }
            else if (json.success == false) {
                //$.each(json, function(key, value){
                    //console.log(key);
                    //console.log(value.errors);
                //});
                $("#grid2_bottom_one").replaceWith('<p id="grid2_bottom_one">'+JSON.parse(json.errors).email[0].message+'</p>');
                //$("#internal ul").last().append('<li><div class="preview"><img src="/static/blog/images/mike.png" alt=""></div>\
                                                 //<div class="data"><div class="title">'+json.name+'<a>'+json.created+'</a></div>\
                                                 //<p>'+json.body+'</p></div><div class="clear"></div></li>');
            }
        }

    })
};

/*
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

*/