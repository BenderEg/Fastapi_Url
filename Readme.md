Web-page, which can convert long links and return short links.
An access to original link will be provided automaticaly with redirection.

For instance:

1. Using input form user can send a link: https://example.com/long/path?long=query/;
2. Get back a short link: {host_domain_name}/shortstring;
3. If user send http request using short link, he will be redirected to original link.

If user add '+' at the end of a link, user get statistics of the link's usages.

Technology stack:

1. Fastapi;
2. Redis;
3. Pydantic;
4. ChatGPT;
5. Pytest.

The main part of service was created based on Fastapi+Pydantic pair.
To store links I use Redis database.
Frontend part was created by ChatGPT.