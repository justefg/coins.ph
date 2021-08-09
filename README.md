Coins.ph Home Assignment
================

## Requirements
Docker-compose and docker.

## How do I play with it?
Simply run the following commands:
```
docker-compose run web python manage.py makemigrations app
docker-compose run web python manage.py migrate app
docker-compose up -d
```

## API endpoints
- `/create_user/<name>/email`

Creates account with <name> and <email>
```
curl 'http://localhost:8000/app/create_user/bob/someemail'
{"status": "created"}%
```
- `/get_user/<name>`

Get user info and balance
```
curl 'http://localhost:8000/app/get_user/emil'
{"name": "emil", "email": "emilchess@yandex.ru", "balance": 0}
```
- `/transfer/<src>/<dst>/<amount>`

Transfers `amount` from `src` to `dst`
```
curl 'http://localhost:8000/app/transfer/alice/bob/100'
{"tx_id": 10, "status": "PENDING"}
```

## From the author
I think the task is a great illustration of the problems one might
come across when designing a payment system. It might like an easy
problem but when you start thinking in-depth it's actually quite complex. What if a deadlock happens? What if a node running a transaction goes down?
How do you scale the system to hundreds of millions transactions daily?
Shard the data? master-master replication?
While I don't have answers to all of the questions I'll describe
my approach that scales quite easily and handles most of the problems.
When a client makes a transaction we generate a `unique id` for it
and store it in a queing system such as Rabbit or Kafka that guarantees
order of the messages and at least once delivery.

Once we have a unique id for the transaction our workers will grab messages
from the queue and try to run a transfer transaction in the database
until they succeed. The key point here is that each transaction has
a unique id assigned to it at the time of a request. That's why
we can rerun it if a node goes down, for example. To illustrate
this point let's assume our users `alice` and `bob` live in different
database shards, say `shard_a` and `shard_b`.
When a request comes, for example, alice transfers
`100$` to bob we assign it a unique id and store it in a queue.
Transfer means essentially subtracting some amount from one user
and adding it to another. So that's what we'll do. Our worker
will `atomically` subtract `100$` from alice and store the `transaction id` in the
`operations` table of `shard_a`.
Obviosly, we'll first need to validate that alice has sufficient funds.
After that it'll update the operations table in `shard_b`.
Because we store the transaction id the pipeline will fail if try to execute
any operation twice.


I timeboxed the assignment to around 2,5 hours and naturally had to make sacrifices.
Some obvious improvements include:
- unit tests
- large piece of logic related to executing transactions in the database with the approach described. A celery worker or a separate thread/process.
- `create_user` and `transfer` should obviously be `POST` methods
- input validation and error handling
- CI job for running testing and pylint/flake8 checks

## Useful links
- https://www.postgresql.org/docs/9.1/explicit-locking.html
- https://www.rabbitmq.com/getstarted.html
