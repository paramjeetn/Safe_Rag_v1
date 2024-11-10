### Running Locally

```shell
#ccd into safe_rag if not already
conda activate something
#if virtual environment not present
python3 -m venv .venv
#else
source .venv/bin/activate
#then
export PGPASSWORD=postgres
```

Then run:

```shell
dbos migrate
dbos start
```

### Postman
POST [`http://localhost:8000/api/v1/check_and_insert_file_status`](http://localhost:8000/api/v1/check_and_insert_file_status)

```
#Put this in BODY as raw json

{
  "file_ids": [101, 102, 103],
  "file_owner_is": ["owner_1", "owner_2", "owner_3"],
  "added_by_user_id": "user_123"
}
```
### Deploying to the Cloud

To deploy this app to DBOS Cloud, first install the DBOS Cloud CLI (requires Node):

```shell
npm i -g @dbos-inc/dbos-cloud
```

Then, run this command to deploy your app:

```shell
dbos-cloud app deploy
```