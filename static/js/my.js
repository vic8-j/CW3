// Create image upload box and initialise configuration
Dropzone.options.photoUpload = {
    init: function() {
        this.on("success", function(file, data) {
            $("#loader").css('visibility', 'hidden');
            $("#breed_info").empty();
            $("#breed_info").append("<div id='breed_list' class='u-list u-list-1'></div>");
            display_breeds(data);
            accordion_event();
        });
        this.on("uploadprogress", function(file) {
            $('#carousel_05ed').addClass('u-section-5');
            $('#carousel_4665').css('visibility', 'hidden');
            this.removeAllFiles();
            $("#breed_info").empty();
            $("#breed_info").append("<div class='loader'></div>");
            $('html, body').animate({
                scrollTop: ($('#carousel_4665').offset().top)
            },500);
        });
        this.on("error", function(file, message) {
            $('#error_msg').text(message);
            this.removeAllFiles(file);
        });
    },
    url: "/photoUpload",
    parallelUploads: 1,
    maxFilesize: 1,
    acceptedFiles: ".jpeg,.jpg,.png",
    maxFilesize: 0.3
};

// Display the predicted breed list.
function display_breeds(data) {
     show_result(data);
     breed_chart(data);
     $("#breed_list").append("<h3 class='u-align-left u-text u-head-1'>Prediction Board</h3>");
     //var div_repeater = "<div id='repeater' class='u-repeater u-repeater-1'></div>";
     //$("#breed_list").append(div_repeater);
     for(key in data) {
        var div_container = $("<div></div>");
        div_container.addClass("accordion u-container-style u-list-item u-repeater-item u-list-item-1")
        $("#breed_list").append(div_container);
        var div_item = $("<div></div>");
        div_item.addClass("u-container-layout u-similar-container u-container-layout-1")
        div_container.append(div_item);
        var image = data[key]['name'].replace(' ', '-');
        div_item.append("<div class='u-image u-image-circle u-image-"+image+"'></div>");
        div_item.append("<h6 class='u-text u-text-1'>"+data[key]['name']+"&nbsp;&nbsp;(Possibility:&nbsp;"+data[key]["prob"]+"%)</h6>");
        //div_item.append("<p class='u-small-text u-text u-text-variant u-text-2'>(%&nbsp;Possibility: "+data[key]["prob"]+"%&nbsp;)</p>");
        var div_prob = $("<div></div>");
        div_prob.addClass("panel u-text u-text-3");
        var cat_img = $("<img></img>");
        cat_img.attr("src","static/images/"+image+".jpg");
        cat_img.addClass("cat_breed_image");
        cat_img.attr("align","center");
        div_prob.append(cat_img);
        div_prob.append(data[key]["desc"]);
        div_item.append(div_prob);
        div_item.find("p").addClass("cat_des_text");
     };
};

// Create a bar chart for breeds
function breed_chart(cdata) {
    $("#breed_list").append("<div id='chart'></div>");
    var chart = c3.generate({
    data: {
        json: cdata,
        type : 'bar',
        keys: {
            x: 'name',
            value: ['prob']
        },
        colors: {prob: function(d) {
            if (d.value >= 90){
                return '#006d77';
            } else {
                return '#e29578';
            }
         }}
    },
    axis: {
        x: {
            label: {
                text: 'Breeds',
                position: 'outer',
            },
            type: 'category',
        },
        y: {
            label: {
                text: 'Probability (%)',
                position: 'outer'
            },
            padding: {
                top: 0,
                bottom: 0
            }
        }
    },
    bar: {
        width: {
            ratio: 0.5
        }
    },
    size: {
        height: 340,
        width: 680
    },
    });
};

// Show the summary of result.
function show_result(data) {
    $('#carousel_4665').css('visibility', 'visible');
    pro_breeds = [];
    res_str = "";
    for(key in data) {
        if (data[key]["prob"] > 90) {
            pro_breeds.push(data[key]);
        };
    };
    if (pro_breeds.length == 0) {
        var res_str = "&#128517;&nbsp;It seems this breed of cat haven't been collected in our system because all breed predictions for this cat are below <b>90%</b>. Even so, we still give you some of the most likely answers. Check the information below."
    } else if (pro_breeds.length == 1) {
        var res_str = "Wow! It is more likely to be a <b>" + pro_breeds[0]["name"] + "</b> cat, whose probability is more than <b>90%</b> . Do I guess right? Check the information below.";
    } else {
        var res_str = "&#128521;&nbsp;It is likely to be a mixed breed, "
        for (i = 0; i < pro_breeds.length; i++) {
          res_str += "with <b>"+pro_breeds[i]["prob"]+"%</b> similar to the <b>"+pro_breeds[i]["name"]+"</b> cat, ";
        }
        res_str = res_str.substring(0,res_str.lastIndexOf(','));
        res_str += ". Check the information below."
    }
    $("#result").html(res_str);
};

// Add accordion event for each cat item in the prediction board
function accordion_event() {
    var acc = $(".accordion");
    var i;

    for (i = 0; i < acc.length; i++) {
      acc[i].addEventListener("click", function() {
        $(this).toggleClass("active");
        var panel = $(this).find(".panel");
        if (panel.css('max-height') != '0px') {
          panel.css('max-height', 0);
        } else {
          panel.css('max-height', panel[0].scrollHeight+"px");
        }
      });
    }
}