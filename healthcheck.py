import http.client
import sys

try:
    conn = http.client.HTTPConnection("localhost", 8000)
    conn.request("GET", "/health")
    response = conn.getresponse()
    if response.status == 200:
        print("Health check passed")
        sys.exit(0)
    else:
        print(f"Health check failed with status code: {response.status}")
        sys.exit(1)
except Exception as e:
    print(f"Health check failed with exception: {e}")
    sys.exit(1)
