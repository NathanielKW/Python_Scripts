import base64
import sys


argLen = len(sys.argv)

if argLen < 2:
    print("No string to encode was provided")
else:
    baseString = sys.argv[1]
    stringBytes = baseString.encode("ascii")
    b64Bytes = base64.b64encode(stringBytes)
    b64String = b64Bytes.decode("ascii")

    print(f"Encoded string: {b64String}")