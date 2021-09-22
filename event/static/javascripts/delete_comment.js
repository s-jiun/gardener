const requestDeleteComment = new XMLHttpRequest();

const onClickDeleteComment = (challenge_id, challengeReply_id) => {

    const url = 'delete_comment/';
    requestDeleteComment.open('POST', url, true);
    requestDeleteComment.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestDeleteComment.send(JSON.stringify({challenge_id: challenge_id, challengeReply_id: challengeReply_id}));
};

const deleteCommentHandleResponse = () => {
    if(requestDeleteComment.status < 400) {

        const {challenge_id, challengeReply_id, comment_count} = JSON.parse(requestDeleteComment.response);
        const element1 = document.querySelector(`.comment-${challengeReply_id}`);
        const element2 = document.querySelector(`#collapseReply-${challengeReply_id}`);
        if(element2){
            element2.innerHTML = '';
        }
        element1.innerHTML = '';
        const element_comment_count = document.querySelector(`.comment-count`);
        element_comment_count.innerHTML = comment_count
    }
};

requestDeleteComment.onreadystatechange = () => {
    if (requestDeleteComment.readyState === XMLHttpRequest.DONE) {
        deleteCommentHandleResponse();
    }

};

const requestDeleteReply = new XMLHttpRequest();


const onClickDeleteReply = (parent_reply_id, challenge_id, challengeReply_id) => {

    const url = 'delete_reply/';
    requestDeleteReply.open('POST', url, true);
    requestDeleteReply.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestDeleteReply.send(JSON.stringify({parent_reply_id: parent_reply_id, challenge_id: challenge_id, challengeReply_id: challengeReply_id}));
};

const deleteReplyHandleResponse = () => {
    if(requestDeleteReply.status < 400) {

        const {parent_reply_id, challenge_id, challengeReply_id} = JSON.parse(requestDeleteReply.response);
        const element = document.querySelector(`.reply-${parent_reply_id}-${challengeReply_id}`);
        element.innerHTML = '';
    }
};

requestDeleteReply.onreadystatechange = () => {
    if (requestDeleteReply.readyState === XMLHttpRequest.DONE) {
        deleteReplyHandleResponse();
    }

};