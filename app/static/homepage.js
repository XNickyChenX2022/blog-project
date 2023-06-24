function scroll_page(){
    var isFetching = false;
    var isBottomReached = false;
    $(window).on('scroll', function () {
        var $windowtop = $(window).scrollTop();
        var $windowheight = $(window).height();
        var $docheight = $(document).height();
        if(!isFetching && $windowtop + $windowheight > $docheight - 100 && !isBottomReached){
            isFetching = true;
            fetch("/more", {
                method: "POST",
                headers: {
                "Accept": "application/json", 
                "Content-Type": "application/json"
                }
            })
            .then((res) => res.text())
            .then((data) => $('#homepage').append(data));
        }
    });
};