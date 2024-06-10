


const videosList = [
	{
		video: '{% static "videos/vid-9.mp4" %}',
		title: '3D helicopter animation'
	},
	{
		video: '{% static "videos/vid-3.mp4" %}',
		title: 'emoji falling animation'
	},
	{
		video: '{% static "videos/vid-4.mp4" %}',
		title: 'house flood animation'
	},
	{
		video: '{% static "videos/vid-2.mp4" %}',
		title: 'zoombie walking animation'
	},
	{
		video: '{% static "videos/vid-4.mp4" %}',
		title: '3D town animation'
	},
	{
		video: '{% static "videos/vid-5.mp4" %}',
		title: 'man chasing carrot animation'
	},
	{
		video: '{% static "videos/vid-6.mp4" %}',
		title: 'door hinge animation'
	},
	{
		video: '{% static "videos/vid-7.mp4" %}',
		title: 'poeple walking in town animation'
	},
	{
		video: '{% static "videos/vid-8.mp4" %}',
		title: 'knight chasing virus animation'
	},
	]
	
	
	document.addEventListener("DOMContentLoaded",function(){
	
	
	const categories = [...new Set(videosList.map((item) => { return item }))]
	document.getElementById('videosList').innerHTML = categories.map((item) => {
		var { video, title } = item;
		return (
			`<div class="list active">
			<video src=${video} class="list-video"></video>
			<h3 class="list-title">${title}</h3>
			</div>`
			)
	}).join('')
	
	let videoList = document.querySelectorAll('.video-list-container .list');
	videoList.forEach(remove => { remove.classList.remove('active') });
	videoList.forEach(vid => {
		vid.onclick = () => {
			videoList.forEach(remove => { remove.classList.remove('active') });
			vid.classList.add('active');
			let src = vid.querySelector('.list-video').src;
			let title = vid.querySelector('.list-title').innerHTML;
			document.querySelector('.main-video-container .main-video').src = src;
			document.querySelector('.main-video-container .main-video').play();
			document.querySelector('.main-video-container .main-vid-title').innerHTML = title;
		};
	});
	})
	