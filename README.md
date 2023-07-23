# pyroboxCore
A simple and fun server framework to avoid using django and big stuff

# Feel Free to Support Me:
<a href="https://www.buymeacoffee.com/RaSan147" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

# Usage
* Import the module
```python
from pyroboxCore import config, logger, SimpleHTTPRequestHandler as SH_base, DealPostData as DPD, run as run_server
```
    * config: A class containing the configuration of the server. Kindly check the code comments for more info.
	* logger: Logger module to log stuffs and also supress the logs.
	* SimpleHTTPRequestHandler: A class that inherits from BaseHTTPRequestHandler and has some extra features. This is the main class that you will be using.
	* DealPostData: A class that uses the SimpleHTTPRequestHandler class functions to deal with post data.
	* run: A function that runs the server.

* Incase you need to change SimpleHTTPRequestHandler methods or funtionality Create a class that inherits from SimpleHTTPRequestHandler and override the methods you want to change. You can check an example in [here](https://github.com/RaSan147/pyrobox/blob/c18462f2674cfe8aac1b2e86ac1f79f3866c671d/dev_src/local_server_pyrobox.py#L145) 

* Lets make our first server
```python
from http import HTTPStatus

from pyroboxCore import config, logger, SimpleHTTPRequestHandler as SH_base, run as run_server

class SH(SH_base):
	"""
		Simply inherits from SimpleHTTPRequestHandler
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

@SH.on_req('HEAD') # HEAD or GET both requests will be handled by this function
def default_get(self: SH, *args, **kwargs):
	"""
		Handles all the GET requests
	"""
	self.send_text(HTTPStatus.OK, "Hello World")


def run():
	run_server(handler=SH, port=8080)
	# this will run the server in current directory at port 8080

if __name__ == '__main__':
	run()
```

* So you've seen how it works.
  * **NOTE THAT** The `@SH.on_req` decorator acts as switch case for the request type. So make sure to put default case at the end of handlers tree. Also handle 404 errors in the default case.

* Lets spice it up a bit
```python
from http import HTTPStatus

from pyroboxCore import config, logger, SimpleHTTPRequestHandler as SH_base, run as run_server

class SH(SH_base):
	"""
		Simply inherits from SimpleHTTPRequestHandler
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

@SH.on_req('HEAD', url='/') # HEAD or GET both requests will be handled by this function
def index(self: SH, *args, **kwargs):
	"""
		Handles index page ("/") request only
	"""
	self.send_text(HTTPStatus.OK, "Hello World")

@SH.on_req('HEAD', url='/test') # @SH.on_req has many more args to handle request url and query string. Check the code comments for more info
def test(self: SH, *args, **kwargs):
	"""
		Handles requests to "/test" only
	"""
	self.send_text(HTTPStatus.OK, "This is a test")
	# you can also send json data
	# self.send_json({"test": "This is a test"})

	# or send a file
	# self.send_file("path/to/file")

@SH.on_req('HEAD') # anything other than home and /test will raise 404
def default_get(self: SH, *args, **kwargs):
	"""
		Handles all the other GET requests
	"""
	self.send_error(HTTPStatus.NOT_FOUND, "Page not found")

def run():
	run_server(handler=SH, port=8080)
	# this will run the server in current directory at port 8080

if __name__ == '__main__':
	run()
```

* Now lets see how to deal with post data
```python
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
```

# For more Examples,
Check 
* [pyrobox](https://github.com/RaSan147/pyrobox/tree/master/src) : A remote file manager server
* [AI_girl](https://github.com/RaSan147/VoiceAI-Asuna/blob/main/src/App_server.py) : A simple chatbot server with messaging interface
