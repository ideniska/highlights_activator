$("#start-trial").click(startTrial);

function startTrial() {
    $.ajax({
        type: "GET",
        url: `/api/user/trial/`,
        success: function (data) {
            console.log("success", data)
            window.location.reload();
        },
        error: function (data) {
            console.log("error", data)
        }
    })
}