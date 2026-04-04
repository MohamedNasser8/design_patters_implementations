from schema import RegularHttpBuilder, JsonHttpBuilder, XmlHttpBuilder, HttpDirector

def application():
    print("Application started")

    # Regular GET Request
    print("Regular GET Request")
    regular_http_builder = RegularHttpBuilder()
    http_director = HttpDirector(regular_http_builder)
    request = http_director.build_regular_GET_request("http://localhost:8080/posts", {"Content-Type": "application/json"})
    response = http_director.send_request(request)
    print(response.json())

    # JSON POST Request
    print("JSON POST Request")
    json_http_builder = JsonHttpBuilder()
    json_http_builder.set_body({"title": "Test Title", "body": "Test Body"})
    json_http_builder.set_method("POST")
    json_http_builder.set_url("http://localhost:8080/posts")
    json_http_builder.set_headers({"Content-Type": "application/json"})
    json_http_builder.set_timeout(10)
    json_http_builder.set_retries(3)
    json_http_builder.set_auth({"username": "testuser", "password": "testpassword"})
    request = json_http_builder.build()
    response = http_director.send_request(request)
    print(response.json())


if __name__ == "__main__":
    application()
