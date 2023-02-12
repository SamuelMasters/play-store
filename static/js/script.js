/* Handles toast messages shown to user */
/* Code provided by Richard Ash, https://code-institute-room.slack.com/archives/C7HS3U3AP/p1633769555244600?thread_ts=1633696310.225500&cid=C7HS3U3AP */
let toastElList = [].slice.call(document.querySelectorAll('.toast'))
let toastList = toastElList.map(function (toastEl) {
    let option = {
        animation: true,
        autohide: true,
        delay: 5000,
    };
    let bsToast = new bootstrap.Toast(toastEl, option)
    bsToast.show();
});