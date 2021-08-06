const requestAddComment = new XMLHttpRequest();

const onClickAddComment = (id) => {
    const ct = document.getElementById(`comment-${id}`).value;
    const url = 'add_comment/';
    requestAddComment.open('POST', url, true);
    requestAddComment.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestAddComment.send(JSON.stringify({id: id, ct:ct}));

};

const addCommentHandleResponse = () => {
    if (requestAddComment.status <400) {
        const {id,ct,comment_id} = JSON.parse(requestAddComment.response);
        const comments = document.querySelector(`.comments-${id}`)
        const makecomment = document.querySelector(`#comment-${id}`)
        const newcomment = ct
        comments.innerHTML += `<div class = 'comment-${comment_id} spanlength'>${newcomment}
                <button class = 'deletecomment-${comment_id}' type = 'submit'  onclick='onClickDeleteComment(${comment_id},${id})'>삭제</button>
            </div>`
        makecomment.value= ''
    };
};
requestAddComment.onreadystatechange = () => {
    if (requestAddComment.readyState === XMLHttpRequest.DONE) {
        addCommentHandleResponse();
    }
};

const requestDeleteComment = new XMLHttpRequest();

const onclickDeleteComment = (comment_id, post_id) => {
    const url = 'delete_comment/';
    requestDeleteComment.open('POST', url, true);
    requestDeleteComment.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestDeleteComment.send(JSON.stringify({comment_id: comment_id, post_id: post_id}));
};

const deleteCommentHandleResponse = () => {
    if(requestDeleteComment.status < 400) {
        const {post_id, comment_id} = JSON.parse(requestDeleteComment.response);
        const comment = document.querySelector(`.comments-${post_id} .comment-${comment_id}`)
        comment.innerHTML = '';
    }
};

requestDeleteComment.onreadystatechange = () => {
    if (requestDeleteComment.readyState === XMLHttpRequest.DONE) {
        deleteCommentHandleResponse();
    }
};