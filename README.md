# Jeff Kayser Homework

## Installation

Clone the source code:

```bash
$ git clone https://github.com/jeffkayser/jk-hw.git
```

## Running

```bash
$ docker-compose up
```

Recommend testing with [HTTPie](https://httpie.org/)


### Create request (valid)

```bash
$ http POST localhost:8088/request title='Pride and Prejudice' email='asdf@example.com'
```


### Create request (bad JSON)

```bash
$ http POST localhost:8088/request
```


### Create request (bad email)

```bash
$ http POST localhost:8088/request title='Pride and Prejudice' email='asdf@'
```


### Create request (bad title)

```bash
$ http POST localhost:8088/request title='Best Book Ever' email='asdf@example.com'
```


### Get all requests

```bash
$ http GET localhost:8088/request
```


### Get single request

Assumptions: request ID=1 exists

```bash
$ http GET localhost:8088/request/1
```


### Delete a request

Assumptions: request ID=1 exists

```bash
$ http DELETE localhost:8088/request/1
```
