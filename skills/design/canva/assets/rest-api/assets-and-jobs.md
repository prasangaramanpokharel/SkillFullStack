# Canva REST API Assets, Uploads & Asynchronous Jobs

## Asset Upload Workflow

Uploading media from external sources or disk requires a two-step staging protocol:

```bash
# Upload local asset
canva api assets upload --file ./assets/hero.png --name "Hero Banner Q3"

# Upload from remote URL
canva api assets upload-url --url "https://cdn.example.com/image.jpg" --name "Remote Graphic"
```

## Polling Asynchronous Jobs

Operations returning `{ "job": { "id": "job_12345", "status": "in_progress" } }` require exponential backoff polling:

```bash
# Poll job status
canva api jobs get --id job_12345
```

Status transitions:
1. `in_progress` -> Keep waiting (increment delay by $1.5\times$).
2. `success` -> Extract `result.asset.id` or `result.design.id`.
3. `failed` -> Abort and report `error.message`.
