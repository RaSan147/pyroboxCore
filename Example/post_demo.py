from http import HTTPStatus

from pyroboxCore import config, logger, SimpleHTTPRequestHandler as SH_base, DealPostData as DPD, run as run_server

class SH(SH_base):
	"""
		Simply inherits from SimpleHTTPRequestHandler
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

@SH.on_req('HEAD')
def default_get(self: SH, *args, **kwargs):
	"""
		Handles all the GET requests
	"""
	return self.send_text(HTTPStatus.OK, """
	<html>
<head>
<title>Post demo</title>
</head>
<body>
	<!-- multipart form -->
	<form action="/post_address" method="post" enctype="multipart/form-data">
		<!-- text field -->
		<label for="text1">Name: </label>
		<input type="text" name="text1" placeholder="Enter Name" />
		</br>
		<label for="text2">Age: </label>
		<input type="text" name="text2" placeholder="Enter Age" />
		</br>
		<input type="submit" value="submit" />
	</form>
</body>

</html>
	""", content_type="text/html; charset=utf-8")

@SH.on_req('POST')
def default_post(self: SH, *args, **kwargs):
	"""
		Handles all the POST requests
	"""
	# you can use the DealPostData class to deal with post data

	post = DPD(self)

	post.start() # start the post data processing
	# this will gather content_length, content_type, boundary from the request headers and reach the end of the headers (and the 1st boundary at line 0)

	n = 1
	while True:
		line = post.get()
		# you can also handle form fields using `post.get_part(verify_name=None, varify_msg=None)`
		# optional `verify_name` and `verify_msg` args can be used to verify the name of the field and the message
		# if not varified, raise `PostError` (this will also cancel the post connection. So you can actually block requests before they even complete) 
		if line is None:
			break
		# do something with the line
		print(f"Line {n}: {line}")
		n += 1
	print("The post data is over")


	# you can also send a file/text/json response
	return self.send_text(HTTPStatus.OK, "<b>Post data received</b>", content_type="text/html; charset=utf-8")
	# you can also post process in the function if you just don't want to return anything yet


def run():
	run_server(handler=SH, port=8080)
	# this will run the server in current directory at port 8080

if __name__ == '__main__':
	run()