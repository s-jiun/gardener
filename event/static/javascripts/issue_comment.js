const requestDeleteComment = new XMLHttpRequest();

const onClickDeleteComment = (cardnews_id, NewsReply_id) => {

    const url = 'issue_delete_comment/';
    requestDeleteComment.open('POST', url, true);
    requestDeleteComment.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestDeleteComment.send(JSON.stringify({cardnews_id: cardnews_id, NewsReply_id: NewsReply_id}));
};

const deleteCommentHandleResponse = () => {
    if(requestDeleteComment.status < 400) {

        const {NewsReply_id ,comment_count} = JSON.parse(requestDeleteComment.response);
        const element1 = document.getElementById(`comment-${NewsReply_id}`)
        console.log(element1);
        const element2 = document.querySelector(`#collapseReply-${NewsReply_id}`);
        const element3 = document.querySelector(`#comment_count`);
        if(element2){
            element2.innerHTML = '';
        }
        element1.innerHTML = '';
        element3.innerHTML = comment_count
        if (comment_count == 0) {
            const element4 = document.querySelector(`#issue-detail-comment`)
            element4.innerHTML = `<p>아직 작성된 댓글이 없습니다</p>`
        }
    }
};

requestDeleteComment.onreadystatechange = () => {
    if (requestDeleteComment.readyState === XMLHttpRequest.DONE) {
        deleteCommentHandleResponse();
    }

};

const requestDeleteReply = new XMLHttpRequest();


const onClickDeleteReply = (parent_reply_id, cardnews_id, NewsReply_id) => {

    const url = 'issue_delete_reply/';
    requestDeleteReply.open('POST', url, true);
    requestDeleteReply.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestDeleteReply.send(JSON.stringify({parent_reply_id: parent_reply_id, cardnews_id: cardnews_id, NewsReply_id: NewsReply_id}));
};

const deleteReplyHandleResponse = () => {
    if(requestDeleteReply.status < 400) {

        const {parent_reply_id, cardnews_id, NewsReply_id, comment_count} = JSON.parse(requestDeleteReply.response);
        const element = document.querySelector(`.reply-${parent_reply_id}-${NewsReply_id}`);
        element.innerHTML = '';
        const element_comment_count = document.querySelector(`.comment-count`);
        element_comment_count.innerHTML = comment_count
        if (comment_count == 0) {
            const element3 = document.querySelector(`#issue-detail-comment`)
            element3.innerHTML = `<p>아직 작성된 댓글이 없습니다</p>`
        }
    }
};

requestDeleteReply.onreadystatechange = () => {
    if (requestDeleteReply.readyState === XMLHttpRequest.DONE) {
        deleteReplyHandleResponse();
    }

};