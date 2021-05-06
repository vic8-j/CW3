// Create image upload box and initialise configuration
Dropzone.options.photoUpload = {
    init: function() {
        this.on("success", function(file, data) {
            $("#loader").css('visibility', 'hidden');
            $("#breed_info").empty();
            $("#breed_info").append("<div id='breed_list' class='u-list u-list-1'></div>");
            display_breeds(data);
        });
        this.on("thumbnail", function() {
            $('#carousel_05ed').addClass('u-section-5');
            $('#carousel_4665').css('visibility', 'hidden');
            this.removeAllFiles();
            $("#breed_info").empty();
            $("#breed_info").append("<div class='loader'></div>");
            $('html, body').animate({
                scrollTop: ($('#carousel_4665').offset().top)
            },500);
        });
    },
    url: "/photoUpload",
    parallelUploads: 1,
    maxFilesize: 1,
    acceptedFiles: "image/*"
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
        div_container.addClass("u-container-style u-custom-color-2 u-list-item u-repeater-item u-list-item-1")
        $("#breed_list").append(div_container);
        var div_item = $("<div></div>");
        div_item.addClass("u-container-layout u-similar-container u-container-layout-1")
        div_container.append(div_item);
        var image = data[key]['name'].replace(' ', '-');
        div_item.append("<div class='u-image u-image-circle u-image-"+image+"'></div>");
        div_item.append("<h6 class='u-text u-text-1'>"+data[key]['name']+"</h6>");
        div_item.append("<p class='u-small-text u-text u-text-variant u-text-2'>(Possibility: "+data[key]["prob"]+"%&nbsp;)</p>");
        div_item.append("<p class='u-text u-text-3'>"+data[key]["desc"]+"</p>");
     };
};

// Create a pie chart of breeds
function breed_chart(cdata) {
    $("#breed_list").append("<div id='chart'></div>");
    var data = {};
    var names = [];
    cdata.forEach(function (e) {
        names.push(e.name);
        data[e.name] = e.prob;
    });
    var chart = c3.generate({
    data: {
        json: data,
        type : 'pie'
    },
    key: {
        x: 'name',
        value: ['prob']
    },
    color: {
        pattern: ['#264653','#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']
    },
    size: {
        height: 460
    }
});
};

// Show the summary of result.
function show_result(data) {
    $('#carousel_4665').css('visibility', 'visible');
    var breed_flag = true;
    for(key in data) {
        if (data[key]["prob"] > 90) {
            breed_flag = false;
        };
    };
    if (breed_flag == false) {
        var res_str = "Wow! It is more likely a <b>" + data[0]["name"] + "</b> cat, with <b>"+data[0]["prob"]+"%</b> possibility. Do I guess right? Check the data below.";
        $("#result").html(res_str);
    } else {
        var res_str = "Wow! It is likely to be a mixed breed, with <b>"+data[0]["prob"]+"%</b> chance of being a <b>"+data[0]["name"]+"</b> cat, <b>"+data[1]["prob"]+"%</b> chance of being a <b>"+data[1]["name"]+"</b> cat and <b>"+data[2]["prob"]+"%</b> chance of being a <b>"+data[2]["name"]+"</b> cat. Check the data below.";
        $("#result").html(res_str);
    }
};