import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import MetalView, StyleView, SizeView, OrderView


class JSONServer(HandleRequests):
    def do_GET(self):
        # Parse the URL
        url = self.parse_url(self.path)
        # Determine the correct view needed to handle the requests
        view = self.determine_view(url)
        # Get the request body
        # Invoke the correct method on the view
        try:
            view.get(self, url["query_params"], url["pk"])
        # Make sure you handle the AttributeError in case the client requested a route that you don't support
        except AttributeError:
            return self.response(
                "No view for that route",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def do_PUT(self):
        return self.response(
            "No view for that route",
            status.HTTP_405_UNSUPPORTED_METHOD.value,
        )

    def do_POST(self):
        # Parse the URL
        url = self.parse_url(self.path)
        # Determine the correct view needed to handle the requests
        view = self.determine_view(url)
        # Get the request body
        # Invoke the correct method on the view
        try:
            view.post(self, self.get_request_body())
        # Make sure you handle the AttributeError in case the client requested a route that you don't support
        except AttributeError:
            return self.response(
                "No view for that route",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def do_DELETE(self):
        # Parse the URL
        url = self.parse_url(self.path)
        # Determine the correct view needed to handle the requests
        view = self.determine_view(url)
        # Get the request body
        # Invoke the correct method on the view
        try:
            view.delete(self, url["pk"])
        # Make sure you handle the AttributeError in case the client requested a route that you don't support
        except AttributeError:
            return self.response(
                "No view for that route",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def determine_view(self, url):
        """Lookup the correct view class to handle the requested route

        Args:
            url (dict): The URL dictionary

        Returns:
            Any: An instance of the matching view class
        """
        try:
            # creates a dictionary routes that maps resource names to their corresponding view classes
            routes = {
                "orders": OrderView,
                "metals": MetalView,
                "styles": StyleView,
                "sizes": SizeView,
            }
            # tries to access the view class corresponding to the "requested_resource" key in the url dictionary
            matching_class = routes[url["requested_resource"]]
            # If the key is found in the routes dictionary, it creates an instance of the corresponding view class and returns it
            return matching_class()
        except KeyError:
            return status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
# sets up a server that listens on port 8000 and starts it
def main():
    host = ""
    port = 8000
    # The server is an instance of the HTTPServer class
    # The serve_forever method starts the server and makes it run indefinitely
    HTTPServer((host, port), JSONServer).serve_forever()


# checks if the script is being run directly. If it is, it calls the main function to start the server
if __name__ == "__main__":
    main()
