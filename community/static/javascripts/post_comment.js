// const requestAddComment = new XMLHttpRequest();

// const onClickAddComment = (id) => {
//     const ct = document.getElementById(`comment-${id}`).value;
//     const url = 'add_comment/';
//     requestAddComment.open('POST', url, true);
//     requestAddComment.setRequestHeader(
//         'Content-Type',
//         'application/x-www-form-urlencoded'
//     );
//     requestAddComment.send(JSON.stringify({id: id, ct:ct}));

// };

// const addCommentHandleResponse = () => {
//     if (requestAddComment.status <400) {
//         const {id,ct,comment_id} = JSON.parse(requestAddComment.response);
//         const comments = document.querySelector(`.comments-${id}`)
//         const makecomment = document.querySelector(`#comment-${id}`)
//         const newcomment = ct
//         comments.innerHTML += `<div class = 'comment-${comment_id} spanlength'>${newcomment}
//                 <button class = 'deletecomment-${comment_id}' type = 'submit'  onclick='onClickDeleteComment(${comment_id},${id})'>삭제</button>
//             </div>`
//         makecomment.value= ''
//     };
// };
// requestAddComment.onreadystatechange = () => {
//     if (requestAddComment.readyState === XMLHttpRequest.DONE) {
//         addCommentHandleResponse();
//     }
// };

const requestDeleteComment = new XMLHttpRequest();


const onClickDeleteComment = (parent_id, post_id, reply_id) => {

    const url = 'delete_comment/';
    requestDeleteComment.open('POST', url, true);
    requestDeleteComment.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestDeleteComment.send(JSON.stringify({parent_id: parent_id, post_id: post_id, reply_id: reply_id}));
};

const deleteCommentHandleResponse = () => {
    if(requestDeleteComment.status < 400) {

        const {parent_id, post_id, reply_id} = JSON.parse(requestDeleteComment.response);
        if(parent_id != None){
            const element = document.querySelector(`.reply-${reply_id}`)
            element.innerHTML = ``
        }
        else{
            const element1 = document.querySelector(`.comment-${parent_id}`)
            const element2 = document.querySelector(`.reply-${reply_id}`)
            element2.innerHTML = ``
            element1.innerHTML = ``
        }
    }
};

requestDeleteComment.onreadystatechange = () => {
    if (requestDeleteComment.readyState === XMLHttpRequest.DONE) {
        deleteCommentHandleResponse();
    }

};

