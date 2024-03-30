const shortExtraDataTitles = {
    "chess/puzzle": "Game PGN"
};

$(".short-type-option").on("change", () => {

    const shortType = $(".short-type-option").val() || "";
    const shortExtraDataTitle = shortExtraDataTitles[shortType];

    if (shortExtraDataTitle) {
        $(".short-extra-data-container").css("display", "flex");
        $(".short-extra-data-title").html(shortExtraDataTitle);
    } else {
        $(".short-extra-data-container").css("display", "none");
    }

});

$(".produce-video").on("click", () => {

    const socket = io({ reconnection: false });

    socket.on("connect", () => {
        $(".production-logs").css("display", "flex");
        $(".production-logs").html("<span>Spawning Python process...</span>");

        socket.emit(
            "produce",
            $(".short-type-option").val() || "",
            $(".short-extra-data").val() || ""
        );

        socket.on("render info", message => {
            $(".production-logs").append(`<span>${message}</span>`);
        });
    });

});

const logsObserver = new MutationObserver(() => {
    const logsContainer = $(".production-logs").get(0);
    logsContainer.scrollTop = logsContainer.scrollHeight;
});

logsObserver.observe($(".production-logs").get(0), {
    childList: true
});