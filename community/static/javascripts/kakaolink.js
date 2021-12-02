function sendLinkCustom(thumbnail, likeNum, commentNum, view, title, postid) {
	if (!Kakao.isInitialized()) {
		Kakao.init('673bc569637b7dc9ae3111971d08e04a')
	}
	Kakao.Link.sendCustom({
		templateId: 66239,
        templateArgs: {
            title: title,
            imageUrl: 'https://ourplant.kr' + thumbnail, 
            likes: likeNum, 
            comments: commentNum, 
            watch: view,
            mobileWebUrl: 'community/post/' + postid,
            webUrl: 'community/post/' + postid
        }
	});
}