function linkBridge() {
    bridge.to_client.connect(fromKernel);
}

function fromKernel(message) {
    var data = JSON.parse(message);
    var content = $('#content');
    content.append("<span class=\"" + data.author + "\">" + data.tag + "</span> " + data.message);
    window.scrollTo(0, document.body.scrollHeight);
}

$(function() {
    $('#search').keypress(function(e) {
        // Enter pressed?
        if (e.which == 10 || e.which == 13) {
            bridge.from_client($('#search').val());
            $('#search').val('');
        }
    });
});