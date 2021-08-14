const requestDeleteComment = new XMLHttpRequest();

const onClickDeleteComment = (post_id, comment_id) => {

    const url = 'delete_comment/';
    requestDeleteComment.open('POST', url, true);
    requestDeleteComment.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestDeleteComment.send(JSON.stringify({post_id: post_id, comment_id: comment_id}));
};

const deleteCommentHandleResponse = () => {
    if(requestDeleteComment.status < 400) {

        const {post_id, comment_id} = JSON.parse(requestDeleteComment.response);
        const element1 = document.querySelector(`.comment-${comment_id}`);
            const element2 = document.querySelector(`.reply-${comment_id}`);
            if(element2){
                element2.innerHTML = '';
            }
            element1.innerHTML = '';
    }
};

requestDeleteComment.onreadystatechange = () => {
    if (requestDeleteComment.readyState === XMLHttpRequest.DONE) {
        deleteCommentHandleResponse();
    }

};

const requestDeleteReply = new XMLHttpRequest();


const onClickDeleteReply = (parent_id, post_id, reply_id) => {

    const url = 'delete_reply/';
    requestDeleteReply.open('POST', url, true);
    requestDeleteReply.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestDeleteReply.send(JSON.stringify({parent_id: parent_id, post_id: post_id, reply_id: reply_id}));
};

const deleteReplyHandleResponse = () => {
    if(requestDeleteReply.status < 400) {

        const {parent_id, post_id, reply_id} = JSON.parse(requestDeleteReply.response);
        const element = document.querySelector(`.reply-${parent_id}-${reply_id}`);
        element.innerHTML = '';
    }
};

requestDeleteReply.onreadystatechange = () => {
    if (requestDeleteReply.readyState === XMLHttpRequest.DONE) {
        deleteReplyHandleResponse();
    }

};