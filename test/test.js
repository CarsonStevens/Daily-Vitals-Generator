
$(document).ready(function(){
    $(".day-of-week").click(function(){
      $(this).toggleClass("selected");
    });

    $("#subscribe-btn").click(function(){
      var frequency_type = $("input[name='frequency_type']:checked").val();
      var email = $("input[type='email']").val();
      var time = $("input[type='time']").val();
      var days = [];
      var content = "frequency_type=" + frequency_type + "&date_time=" + time;
      if (frequency_type === "daily") {
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

});

function frequency_change(){
  if ($("#subscribe-btn").css("display") == 'none') {
    $("#subscribe-btn").toggle("slow");
    $("#clock").toggle("slow");
  }
  var frequency_type = $("input[name='frequency_type']:checked").val();
  if (frequency_type != "daily" && $("#daily-container").css("display") != 'none') {
    $("#daily-container").toggle("slow");
  }
  if (frequency_type === "daily") {
    $("#daily-container").toggle("slow");
    console.log("daily");
  }
}
