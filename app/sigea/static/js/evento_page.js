$('document').ready(function () {
    $("#select_capa").change(function () {
        var file = this.files[0];
        var reader = new FileReader();
        reader.onload = function () {
                $('.page-baner').css('background', 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),  url("'+ reader.result +'")');
                $('.page-baner').css('background-position:', 'center center');
                $('.page-baner').css('background-repeat', 'no-repeat');
                
            }

        if (file) {
            reader.readAsDataURL(file);
            console.log(reader)
        } else {
        }
});
});
