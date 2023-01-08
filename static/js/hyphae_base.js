
$(document).ready(function() {
    let calendars = bulmaCalendar.attach("[type='date']", {headerPosition: "bottom"});
    // console.log(calendars);

    // Navbar burger icon https://bulma.io/documentation/components/navbar/
    $(".navbar-burger").click(function() {
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });
});

function toast(type, message="") {
    let color_name, fa_icon;
    if (type == "success") {
        color_name = "success";
        fa_icon = "check";
    }
    else if (type == "warning") {
        color_name = "warning";
        fa_icon = "exclamation-triangle";
    }
    else if (type == "error") {
        color_name = "danger";
        fa_icon = "radiation";
    }
    else {
        color_name = "info";
        fa_icon = "info-circle";
    }
    
    let class_colors = `has-background-${color_name} has-text-${color_name}-light`;
    let icon = `<span class='icon mr-3'><i class='fa fa-${fa_icon}'></i></span>`;
    $(`<div class='toast ${class_colors}'>${icon}${message}</div>`).appendTo("#toaster");
}
