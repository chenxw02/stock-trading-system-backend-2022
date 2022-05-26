# API_list

## A1组负责



## A2组负责



## A3组负责



## A4组负责



## A5组负责

除登录和注册外，其他请求需要携带Header: `Authorization`，表示用户登录后的身份认证，值为token值。

### POST /admin/login

登录股票管理员用户，返回token。

request body: 

```json
{
    "admin_id": "beet",
    "password": "123456"
}
```

response body:

```json
{
    "code": 0,
    "data": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbl9pZCI6ImJlZXQiLCJ0eXBlIjoiYWRtaW4iLCJleHAiOjE2NTM1MDM0Mjh9.7B8yU34jAMDVakE6WazvCTUcssnk1QuRo1CCWVh93n4",
    "message": "success"
}
```

### POST /admin

注册股票管理员用户。

request body: 

```json
[
    {
        "admin_id": "haha",
        "password": "123456"
    }
]
```

是一个数组，可以一次性注册多个（前端并不使用这个接口，纯方便用）。

response body:

```json
{
    "code": 0,
    "data": null,
    "message": "success"
}
```

### PUT /stock/status

需要等股票部分写完。

### 待续

