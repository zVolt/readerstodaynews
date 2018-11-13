from google.cloud import firestore
import requests
import json
from repr import repr
import datetime
import cloudinary.uploader

app = firestore.Client()
posts_ref = app.collection('posts')
posts = posts_ref.order_by(u'date', direction=firestore.Query.DESCENDING).limit(50).get()
for _ in range(50):
	p = next(posts)
	data = p.to_dict()
	data['summary'] = data['excerpt'] or data['title'] or data['content'][:30]
	data['tags'] = [dict(name=x) for x in ['new', 'trending']]
	image_url = data['feature_img']
	print(image_url)
	if image_url:
		try:
			res = cloudinary.uploader.upload(image_url, folder='post_images')
		except:
			print('error uplloading image')
		else:
			url = res.get('url')
			print(url)
			data['media_items'] = [{"media_type": {"name": "image"}, "image": url, "video_url": "", "title": "some title"}]
			print(int(data['date'])/1000)
			date = datetime.datetime.fromtimestamp(int(data['date'])/1000)

			data['last_modified_on'] = date.strftime("%Y-%m-%dT%I:%M")

			del data['excerpt']
			print(repr(data))
			print(repr(data.keys()))
			if data:
				res = requests.post('http://localhost:8000/api/post/', json=[data])
				print res.ok
