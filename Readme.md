# API документация

Добро пожаловать в документацию API. Здесь вы найдете информацию о доступных конечных точках и их использовании.


### Авторизация

`POST /api/authirize/`

Параметры:
- `phone_number` (строка): номер до 15 знаков 


запрос:
```json
{
    "phone_number": "89132561873",
    
}
```

Ответ:
```json
{
    "message":"Authorization code: {auth_code}"
}
```
Ошибка:
```json
{
    "message":"Invalid phone number"
}
```
### Верификация

Принимает код верификации, и в случае соответсвия аутентифицирует пользователя методом сессий

`POST /api/verify/`

Параметры:
- `phone_number` (строка): номер до 15 знаков 
- `auth_code` (строка): числовой код верификации в 4 знака

запрос:
```json
{
    "phone_number":"89132561873",
    "auth_code": "1234",
}
```
Ответ:
```json
{
    "message":"Code verified"
}
```
Ошибка:
```json
{
    "message":"Incorrect code or number"
}
```
### Профиль текущего пользователя
выводит данные текущего пользователя, а также всех пользователей, активировавших реферральную ссылку


`GET /api/profile/`


Ответ:
```json

{
    "id": 38,
    "referred_phone_numbers": [],
    "last_login": "2023-08-20T07:04:43.200381Z",
    "phone_number": "895128483928",
    "auth_code": "2872",
    "referral_code": "y5zcQM",
    "used_referral_code": ["89421834983"]
}
```

### Ввод реферальной ссылки
Позволяет текущему пользователю отправить активировать реферальную ссылку. Происходит проверка на единственность активации и не совмпадение с собственной ссылкой

`POST api/enter_referral`

Параметры:
- `referral_code` (строка): 6-значный набор букв и цифр 


запрос:
```json
{
    "referral_code": "r2d211",
}
```
Ответ:
```json
{
    "message":"Invitation code activated"
}
```
Ошибки:
```json
{
    "message":"Incorrect invite code",
    "message":"You have already used an invitation code",
    "message":"You can't use your code"
}
```
### Профиль пользователя по номеру телефона
выводит номер телефона и реферральный код пользователя по введенному номеру


`GET /api/user/<str:phone_number>`


Ответ:
```json

{
    "phone_number": "895128483928",
    "referral_code": "y5zcQM",
    
}
```
Ошибки:
```json
{
    "message":"User profile not found"
}
```
# Также присутствуют Django Templates в минималистичном интерфейса, где осуществляется весь тот же функционал
