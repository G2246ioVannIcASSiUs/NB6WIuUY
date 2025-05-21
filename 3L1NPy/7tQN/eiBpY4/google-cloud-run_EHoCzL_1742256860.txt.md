
## Test Cloud Run Button's Underlying Command Locally with Local Go

1. Run the tests:
    ```
    go test ./cmd/cloudshell_open
    ```
1. Build the command:
    ```
    go build -o /tmp/cloudshell_open ./cmd/cloudshell_open
    ```
1. To test the command:
    1. [Enable the cloudresourcemanager API](https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview)
    1. [Enable the billing API](https://console.developers.google.com/apis/api/cloudbilling.googleapis.com/overview)
    1. Create a Service Account with the following roles:
        * Cloud Run Admin (`roles/run.admin`), 
        * Service Usage Admin (`roles/serviceusage.serviceUsageAdmin`), 
        * Service Account User (`roles/iam.serviceAccountUser`), and
        * Storage Admin (`roles/storage.admin`).
    1. [Download the Service Account key as a JSON file](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating)
        ```
        export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_YOUR_SERVICE_ACCOUNT_KEY_FILE
        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
        export SKIP_CLONE_REPORTING=true
    1. Run the button:
        ```
        (cd /tmp; rm -rf cloud-run-hello; ./cloudshell_open --repo_url=https://github.com/GoogleCloudPlatform/cloud-run-hello.git; rm -rf cloud-run-hello)
        ```
        Other `cloudshell_open` flags: `--git_branch`, `--dir`, `--context`

## Test Cloud Run Button's Underlying Command Locally in a Container

⚠️ This will download very large Docker images to your system.

1. Download the key json file for the new service account
1. Build the Container
    ```
    docker build -f Dockerfile -t cloud-run-button .
    ```
1. Set an env var pointing to the Service Account's JSON file:

    ```

1. Run Cloud Run Button via Docker:
    ```
    docker run -it -v /var/run/docker.sock:/var/run/docker.sock \
      -v $KEY_FILE:/root/user.json \
      -e GOOGLE_APPLICATION_CREDENTIALS=/root/user.json \
      -e TRUSTED_ENVIRONMENT=true \
      --entrypoint=/bin/sh cloud-run-button -c \
      "gcloud auth activate-service-account --key-file=/root/user.json \
      --quiet && gcloud auth configure-docker --quiet && \
      /bin/cloudshell_open \
    ```

## Test Instrumentless
Test getting a coupon from the instrumentless API:
```
go run ./cmd/instrumentless_test YOUR_EVENT $(gcloud auth print-access-token)
```

## Contributor License Agreement

Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
your current agreements on file or to sign a new one.

(even if it was for a different project), you probably don't need to do it

## Code reviews

All submissions, including submissions by project members, require review. We
information on using pull requests.

## Community Guidelines
Guidelines](https://opensource.google.com/conduct/).
