# Customer Accounts Microservice — DevOps Capstone

[![Accounts CI](https://github.com/vedant412/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg?branch=main)](https://github.com/vedant412/devops-capstone-project/actions/workflows/ci-build.yaml)

A Flask and SQLAlchemy REST service for managing customer accounts. This is the IBM DevOps and Software Engineering Capstone project. The API implements create, list, read, update, and delete. Flask-Talisman adds security headers, and Flask-CORS restricts cross-origin access to configured origins.

## Run and test locally

```sh
python -m pip install -r requirements-dev.txt
export DATABASE_URI=sqlite:///accounts.db
flask --app service:app run --port 8080
```

Use PowerShell's `$env:DATABASE_URI = 'sqlite:///accounts.db'` to set the same variable on Windows. Visit `http://127.0.0.1:8080/` for the service description and `/health` for readiness.

```sh
flake8 service tests
DATABASE_URI=sqlite:///:memory: nosetests tests.test_routes tests.test_models tests.test_cli_commands
```

The test suite clears its database. Use a dedicated test database. The maintained `pynose` distribution provides the `nosetests` command on Python 3.12.

## Account endpoints

| Method | Path | Result |
| --- | --- | --- |
| POST | `/accounts` | Create an account, 201 |
| GET | `/accounts` | List accounts, 200 |
| GET | `/accounts/{id}` | Read an account, 200 |
| PUT | `/accounts/{id}` | Update an account, 200 |
| DELETE | `/accounts/{id}` | Delete an account, 204 |

Set `CORS_ALLOWED_ORIGINS` to a comma-separated list of trusted browser origins. In a TLS environment that forwards the original scheme, set `FORCE_HTTPS=true` to require HTTPS.

## CI and deployment

The GitHub Actions workflow checks out the source, installs dependencies, runs Flake8 and nosetests, builds the Docker image, and verifies the container on port 8080. The Docker image is intended to run with PostgreSQL configured either by `DATABASE_URI` or by the database environment variables shown in `deploy/deployment.yaml`.

In the IBM lab, provision the supplied PostgreSQL template and use the project-scoped registry. Apply the deployment and service manifests with the image tag built for that project. The Tekton files describe the continuous delivery sequence from checkout through deployment. They reference the lab-provided `git-clone` and `buildah` cluster tasks. On OpenShift versions that use installed namespaced tasks, configure their references with the cluster resolver. Use a new tag for each deployment and bind `pipeline-workspace` to `pipelinerun-pvc`.

Adapted from [IBM Skills Network's DevOps Capstone starter](https://github.com/ibm-developer-skills-network/aolwx-devops-capstone-template). See [LICENSE](LICENSE).
