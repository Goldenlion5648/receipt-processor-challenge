Run this command

```docker build -t processor . && docker run -p 8080:8080 -it processor```

You can then access it here with a POST request

```http://localhost:8080/receipts/process```

with a json in your payload. 

You will get a response with an id, and that id can be used at
```http://localhost:8080/receipts/{response_id}/points```

look in `test.py` to see examples of usage.

For debugging:

`docker run -it --entrypoint /bin/bash processor`