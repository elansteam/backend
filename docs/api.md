Временная документация к API. Используется до релиза Documentation NG

# Методы

## `POST /api/auth/signin`
### Input
```js
{
    login: string,
    password: string
}
```
### Output
```js
{
    access_token: string,
    refresh_token: string
}
```
## `POST /api/auth/signup`
### Input
```js
{
    first_name: string,
    email: string,
    password: string
}
```
### Output
```js
{
    access_token: string,
    refresh_token: string
}
```
