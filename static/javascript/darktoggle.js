const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
toggleSwitch.addEventListener('change', switchTheme, false);
const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

// Switch the theme
function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');

    }
}

// Save the attribute locally
function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark'); //add this
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light'); //add this
    }
}

// Display saved themed if saved.
if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'dark') {
        toggleSwitch.checked = true;
        $(document).ready(function(){
          $("#bamboozable-img").toggleClass("invert no-filter");
        });
    }
}

$(document).ready(function(){
    $(".slider").click(function(){
        $("#bamboozable-img").toggleClass("invert no-filter");
    });
});

var show = false;
$(document).ready(function(){

  $("#answers").toggle("slow");

  $(".hider").click(function(){
      show = !show;
      $("#answers").toggle("slow");
      console.log("hide");
      if (show) {
        $(".hider").text("Hide Answers!");
      } else {
        $(".hider").text("Show Answers!");
      }
  });


  $('#home').click(function(){
    $.ajax({
      type : 'GET',
      url : "/",
      success: function(response) {
        $("body").html(response);
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","/");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });


  $('.day').click(function(){
    var id = $(this).attr("id");
    $.ajax({
      type : 'POST',
      url : "/previous_vitals/"+id,
      data : {'data':id},
      success: function(response) {
        $("body").html(response);
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","/previous_vitals/"+id);
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $('#generator').click(function(){
    $.ajax({
      type : 'GET',
      url : "/generator",
      success: function(response) {
        $("body").html(response);
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","/generator");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $('#about').click(function(){
    $.ajax({
      type : 'GET',
      url : "/about",
      success: function(response) {
        $("body").html(response);
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","/about");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $('#api').click(function(){
    $.ajax({
      type : 'GET',
      url : "/api",
      success: function(response) {
        $("body").html(response);
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","/api");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $('#generator-custom').click(function(){
    // Get values from form and set defaults
    $.ajax({
      type : 'POST',
      url : "/generating",
      success: function(response) {
        $("body").html(response);
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","/generating");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $("#generator-submit").click(function(){
    var hinkpink_count = $( "input[name='hinkpink_count" ).val();
    var hinkpink_type = $( "input[name='hinkpink_type" ).val();
    var conversation_count = $("input[name='conversation_count']").val();
    $.ajax({
      type : 'POST',
      url : "generator/generating?hinkpink_count="+hinkpink_count+"&hinkpink_type="+hinkpink_type+"&conversation_count="+conversation_count,
      success: function(response) {
        $("#options").toggle("slow");
        $('#generating').toggle("slow");
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","generator/generating");
        $.ajax({
          type : 'POST',
          url : "generating/generated_custom?hinkpink_count="+hinkpink_count+"&hinkpink_type="+hinkpink_type+"&conversation_count="+conversation_count,
          success: function(response) {
            $("body").html(response);
            window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","generator/generating/generated_custom");
          },
          error: function(error) {
              console.log(error);
          }
        });
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $("#new-content").click(function(){
    $.ajax({
      type : 'GET',
      url : "/submit_content",
      success: function(response) {
        $("body").html(response);
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","/submit_content");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $("#submit-content-btn").click(function(){
    var submit_type = $("input[name='submit_type']:checked").val();
    $(".form").each(function() {
      $(this).attr("display", "none");
    });
    var content;
    if (submit_type === "hinkpink") {
      content = $("input[name='hinkpink1']").val()+","+
                $("input[name='hinkpink2']").val()+","+
                $("input[name='hinkpink3']").val()+","+
                $("input[name='hinkpink4']").val();
    } else if (submit_type ==="commonym") {
      content = $("input[name='commonym1']").val()+" - "+
                $("input[name='commonym2']").val()+" - "+
                $("input[name='commonym3']").val()+","+
                $("input[name='commonym_answer']").val();
    } else if (submit_type === "madgab") {
      content = $("input[name='madgab1']").val()+","+
                $("input[name='madgab_answer']").val();
    } else if (submit_type === "conversation") {
      content = $("textarea").val();
    } else if (submit_type === "riddle") {
      content = $("input[name='riddle1']").val()+"$"+
                $("input[name='riddle_answer']").val();
    } else if (submit_type === "suggestion") {
      content = $("textarea").val();
    }
    $.ajax({
      type : 'POST',
      url : "submit_content/submitted?submit_type="+submit_type+"&submit_content="+content,
      success: function(response) {
        $("#submission-form").toggle();
        $("#submitted-response").toggle();
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","submit_content/submitted");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $("#subscribe").click(function(){
    $.ajax({
      type : 'GET',
      url : "/subscribe",
      success: function(response) {
        $("body").html(response);
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","/subscribe");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $(".day-of-week").click(function(){
    var frequency_type = $("input[name='frequency_type']:checked").val();
    if (frequency_type === "daily") {
      $(this).toggleClass("selected");
    } else if (frequency_type === "weekly"){
      $('.selected').each( function() {
        $(this).toggleClass("selected");
      });
      $(this).toggleClass("selected");
    }
  });

  $("#subscribe-btn").click(function(){
    var frequency_type = $("input[name='frequency_type']:checked").val();
    var email = $("input[type='email']").val();
    var hrs = -(new Date().getTimezoneOffset() / 60);
    var time = $("input[type='time']").val();
    var days = [];
    var content = "frequency_type=" + frequency_type + "&date_time=" + time + "&offset="+ hrs + "&email=" + email;
    console.log(hrs);
    if (frequency_type === "daily" || frequency_type === "weekly") {
      content += "&days=";
      $(".selected").each(function() {
        content +=($(this).data('day')) + ",";
        console.log("selected");
      });
      content = content.slice(0, -1);
    }


    $.ajax({
      type : 'POST',
      url : "subscribe/subscribed?"+content,
      success: function(response) {
        $("#subscribe-time-picker").toggle("slow");
        $("#subscribe-success").toggle();
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","subscribe/subscribed");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $("#unsubscribe-btn").click(function(){
    var email = $("input[type='email']").val();
    $.ajax({
      type : 'POST',
      url : "unsubscribe/unsubscribed?email="+email,
      success: function(response) {
        $("body").html(response);
        $("#subscribe-time-picker").toggle("slow");
        $("#subscribe-success").toggle();
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"","unsubscribe/unsubscribed");
      },
      error: function(error) {
          console.log(error);
      }
    });
  });


});


function processAjaxData(response, urlPath){
     document.getElementById("content").innerHTML = response.html;
     document.title = response.pageTitle;
     window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"", urlPath);
}
window.onpopstate = function(e){
     if(e.state){
         document.getElementById("content").innerHTML = e.state.html;
         document.title = e.state.pageTitle;
     }
};

function updateHinkPinkCountTextInput(val) {
  document.getElementById('hinkPinkCountTextInput').value=val;
}
function updateConversationCountTextInput(val) {
  document.getElementById('conversationCountTextInput').value=val;
}

function submission_change(){
  if ($("#submit-content-btn").css("display") == 'none') {
    $("#submit-content-btn").toggle("slow");
  }
  var submit_type = $("input[name='submit_type']:checked").val();
  $(".form").each(function() {
    $(this).css("display", "none");
  });
  if (submit_type === "hinkpink") {
    $("#hinkpink-submission").css("display", "block");
  } else if (submit_type ==="commonym") {
    $("#commonym-submission").css("display", "block");
  } else if (submit_type === "madgab") {
    $("#madgab-submission").css("display", "block");
  } else if (submit_type === "conversation") {
    $("#conversation-submission").css("display", "block");
  } else if (submit_type === "riddle") {
    $("#riddle-submission").css("display", "block");
  } else if (submit_type === "suggestion") {
    $('#suggestion-submission').css('display', 'block');
  }
}

function frequency_change(){
  $('.selected').each( function() {
      $(this).toggleClass("selected");
  });
  if ($("#subscribe-btn").css("display") == 'none') {
    $("#subscribe-btn").toggle("slow");
    $("#clock").toggle("slow");
  }
  var frequency_type = $("input[name='frequency_type']:checked").val();
  if ((frequency_type != "daily" && frequency_type != "weekly") && $("#daily-container").css("display") != 'none') {
    $("#daily-container").toggle("slow");
  }
  if (frequency_type === "daily" || frequency_type === "weekly") {
    if ($("#daily-container").css("display") == 'none') {
      $("#daily-container").toggle("slow");
    }
  }
}
