$(function replyTo(){
    $("#comment_tree").on("click", ".reply-to", function(){
        var commentId = $(this).data("comment");
        var username = $(this).data("username");
        var box = $(`#reply-box-${commentId}`);
        var textarea = box.find("textarea");
        if (textarea.val().indexOf(`${username}`) == -1) {
            textarea.val(`@${username} `)
        } 
        box.css("display", "block");      
        $('html, body').stop().animate({
            scrollTop: box.offset().top - $(window).height()/2
        }, 50);
        });
    });


$(function insertComment(){
    $("#comment_box").on("click", function(e){
        e.preventDefault();
        var text_box = $("#text_box");
        var text = text_box.val();
        if (text.trim().length < 1){
            alert("Please Enter Text...");
            return; 
        };
        var postId = $(this).data("postid") 
        var data_submit = {
            postId: postId,
            text: text
        };
        fetch("/blog_pages/comment", {
            method: "POST", 
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json" 
            },
            body: JSON.stringify(data_submit)})
        .then((res) => res.text())
        .then((data) => {
            text_box.val("");
            $("#comment_tree").append(data);
        });
    });
});

$(function insertCommentToComment(){
    $("#blog_pages_box").on("click", ".reply-to-comments", function(){
        var commentId = $(this).data("comment");
        var box = $(`#reply-box-${commentId}`);
        var textbox = box.find("textarea");
        var text = textbox.val();
        if (text.trim().length < 1){
            alert("Please enter text...");
            return; 
        };
        var data_submit = {
            commentId: commentId,
            text: text
        };
        fetch("/blog_pages/reply_to_comments", {
            method: "POST", 
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json" 
            },
            body: JSON.stringify(data_submit)})
        .then((res) => res.text())
        .then((data) => { 
            textbox.val("");
            closeForm(commentId);
            $(`#comment-branch-${commentId}`).append(data);
        });
    });
});

$(function likeDislikePost(){
        $(".like_dislike_post").on("click", function(){
            var mode = $(this).data("mode");
            var postId = $(this).data("post");
            var likeButton = $("#like_post").find("i");
            var dislikeButton = $("#dislike_post").find("i");
            var likeDislikeValue = $("#post_value")
            var data_mode = {
                mode:mode,
                postId:postId
            };
            fetch('/blog_pages/post/mode', {
                method: "POST", 
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json" 
                },
                body: JSON.stringify(data_mode)})
                .then((res) => res.json())
                .then((data) => {
                    if (data["new_mode"] == 1){
                        dislikeButton.attr("class", "fa-regular fa-thumbs-down fa-lg");
                        likeButton.attr("class", "fa-solid fa-thumbs-up fa-lg");
                    } else if (data["new_mode"] == 2){
                        likeButton.attr("class", "fa-regular fa-thumbs-up fa-lg");
                        dislikeButton.attr("class", "fa-solid fa-thumbs-down fa-lg");
                    } else {
                        likeButton.attr("class", "fa-regular fa-thumbs-up fa-lg");
                        dislikeButton.attr("class", "fa-regular fa-thumbs-down fa-lg");
                    }
                    likeDislikeValue.text(data["like_dislike_value"]);
            });
        });
    });

$(function likeDislikeComment(){
    $("#comment_tree").on("click", ".like_dislike_comment", function(){
        var mode = $(this).data("mode");
        var commentId = $(this).data("comment");
        var likeButton = $(`#like_comment-${commentId}`).find("i");
        var dislikeButton = $(`#dislike_comment-${commentId}`).find("i");
        var likeDislikeValue = $(`#like_dislike_value-${commentId}`);
        var data_mode = {
            commentId: commentId,
            mode: mode
        }; 
        fetch('/blog_pages/comment/mode', {
            method: "POST",
            headers: { 
                "Accept": "application/json",
                "Content-Type": "application/json" 
            },
            body: JSON.stringify(data_mode)})
            .then((res) => res.json())
            .then((data) => {     
                if (data["new_mode"] == 1){
                    dislikeButton.attr("class", "fa-regular fa-thumbs-down fa-sm");
                    likeButton.attr("class", "fa-solid fa-thumbs-up fa-sm");
                } else if (data["new_mode"] == 2){
                    likeButton.attr("class", "fa-regular fa-thumbs-up fa-sm");
                    dislikeButton.attr("class", "fa-solid fa-thumbs-down fa-sm");
                } else {
                    likeButton.attr("class", "fa-regular fa-thumbs-up fa-sm");
                    dislikeButton.attr("class", "fa-regular fa-thumbs-down fa-sm");
                }
                likeDislikeValue.text(data["like_dislike_value"]);
            });
        });
    });

var editedCommentId;

$(function editcomment(){
    $("#comment_tree").on("click", ".edit-to", function(){
        var commentId = $(this).data("comment");
        var box = $("#edit-box");
        var text = $(`#comment-text-${commentId}`).text();
        var textarea = box.find("textarea");
        textarea.val(text);
        $('#comment-info-label').attr('data-comment-info', `commentId`);
        box.css("display", "block");  
        $('body').css('overflow', 'hidden');
        editedCommentId = commentId;
    });
});    

$(function submitEdit(){
    $("#blog_pages_box").on("click", ".submit-edit", function(){
     var text = $(`#submit-box`).val();
     var data_submit = {
            commentId: editedCommentId,
            text: text
        };
        fetch("/blog_post/edit-comment", {
            method: "POST", 
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json" 
            },
            body: JSON.stringify(data_submit)})
        .then((res) => res.json())
        .then((data) => (data));
        $(`#comment-text-${editedCommentId}`).text(text);
        closeEdit();
    })
})

$(function deleteComment(){
    $("#comment_tree").on("click", ".delete-to", function(){
        var currentUser = $(this).data("current-user");
        var owner = $(this).data("owner");
        var commentId = $(this).data("comment");
        if (currentUser != owner){
            alert("You Can Only Delete Your Post");
            return;
        }
        data_submit = {
            commentId: commentId,
        }
        fetch("/blog_post/delete", {
            method: "POST", 
            headers:{
                "Accept":"application/json", 
                "Content-Type": "application/json"
            }, 
            body:JSON.stringify(data_submit)})
        .then((res) => res.json())
        .then((data) => {
            if (data["check"] == false){
                alert("For the purpose of not being able to delete other user's comments, you can only delele posts with no replies");
            }
            else{
                $(`#comment-box-${commentId}`).remove();
            }
        });
    });
});

function closeForm(commentId){
    $(`#reply-box-${commentId}`).hide();
}


function closeEdit(){
    $("#edit-box").hide();
    $('body').css('overflow', 'visible');
}