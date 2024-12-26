[AnySMS Component](https://github.com/martinhoess/anysms) for Home Assistant
 
### ❗❗❗ ❗❗❗ ❗❗❗ ❗❗❗ ❗❗❗ ❗❗❗ ❗❗❗ 
# Work in progress
### ❗❗❗ ❗❗❗ ❗❗❗ ❗❗❗ ❗❗❗ ❗❗❗ ❗❗❗ 

# What This Is:
This is a custom [Homeassistant](https://home-assistant.io) component for the [AnySMS HTTP gateway](https://www.any-sms.info/).

# What It Does:
It sends a notification as a SMS via the AnySMS HTTP gateway (https://www.any-sms.biz/docs/any_sms_gateway.pdf):

# Requirements

This component needs a valid [Any-sms account](https://www.any-sms.info/anmelden.php) and sufficient credit balance

# Installation

Place the anysms folder inside your custom_components folder (create if it not exists)


# Configuration

```
- notify:
  - platform: anysms
    name: anysms
    client_id: 000000
    api_key: abc
    code: 20
    sender: 0176123456789
    recipient: 0049176987654321
```

# Usage

Same as any other home assistant notify component

```
service: notify.anysms
data:
    message: Hello world
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `client_id`      | `integer` | **Required** your customer id |
| `api_key`      | `string` | **Required** your password or api key |
| `sender`      | `string` | **Required** sender of the sms (16 numbers or 11 characters) |
| `recipient`      | `string` | **Required** recipient of the sms (international format) |
| `code`      | `integer` | sms gateway 20 (default), 28, 29 |


# ToDo
* error handling
* dynamic sender via data 
* dynamic recipient via data
* dynamic gateway via code
* support for multiple recipients
* setup via UI/flow
* service to query account credit balance
* support for receipt confirmation
* unicode support
* test long sms
* support for time offset dispatch

