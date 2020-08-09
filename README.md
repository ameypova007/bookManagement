# IgniteAssignment
Interview Assessment questions Answer

Step to use routes.py
1. Create a virtual Environment on local.
2. Add below packages in requirement.txt
  - pip3
  - flask
  - pymysql
  - request
  - OS
3. Add your DB details in connection object (Mentioned in CAPS).
4. I have used MySQL Dump, so request you to use same.
5. Take dump on your local and used route.py
6. Sample JSON payload to test API.
6.1. JSON input : {"author":[], "language":[], "topic":[], "title":[], "mimeType":[], "bookId":[], "pageNumber":}
6.2. To retrieve the books without any filter use
      {"author":[], "language":[], "topic":[], "title":[], "mimeType":[], "bookId":[], "pageNumber":1} or
      {"author":null, "language":null, "topic":null, "title":null, "mimeType":null, "bookId":null, "pageNumber":2}
6.3 To retrive using specific filter use
      {"author":["abc"], "language":[], "topic":[], "title":["pqr","mlp"], "mimeType":["qwe","poi"], "bookId":[], "pageNumber":9}

      
