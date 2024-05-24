<a name="readme-top"></a>
<p align="center">
<a href="https://sonarcloud.io/summary/new_code?id=Fuck-We-Ballerz_DM885" style="text-decoration:none;">
  <img src="https://img.shields.io/sonar/quality_gate/Fuck-We-Ballerz_DM885?server=https%3A%2F%2Fsonarcloud.io&style=for-the-badge" style="padding-bottom: 5px;"/>
</a>
<a href="https://sonarcloud.io/summary/new_code?id=Fuck-We-Ballerz_DM885" style="text-decoration:none;">
  <img src="https://img.shields.io/sonar/tech_debt/Fuck-We-Ballerz_DM885?server=https%3A%2F%2Fsonarcloud.io&style=for-the-badge" style="padding-bottom: 5px;" />
</a>
<a href="https://sonarcloud.io/summary/new_code?id=Fuck-We-Ballerz_DM885" style="text-decoration:none;">
  <img src="https://img.shields.io/sonar/major_violations/Fuck-We-Ballerz_DM885?server=https%3A%2F%2Fsonarcloud.io&style=for-the-badge" style="padding-bottom: 5px;"/>
</a>
<a href="https://github.com/Fuck-We-Ballerz/DM885/graphs/contributors" style="text-decoration:none;">
  <img src="https://img.shields.io/github/contributors/Fuck-We-Ballerz/DM885.svg?style=for-the-badge" style="padding-bottom: 5px;/">
</a>
<a href="https://github.com/Fuck-We-Ballerz/DM885/blob/main/LICENSE" style="text-decoration:none;">
  <img src="https://img.shields.io/github/license/Fuck-We-Ballerz/DM885.svg?style=for-the-badge" style="padding-bottom: 5px;/">
</a>
<a href="https://zeruscloud.com" style="text-decoration:none;">
  <img src="https://img.shields.io/website?url=https%3A%2F%2Fzeruscloud.com&style=for-the-badge" style="padding-bottom: 5px;"/>
</a>
</p>

<p align="center">
<img src="https://www.sdu.dk/-/media/files/nyheder/logoer/sdu_black_rgb_png.png" width="400" style="padding-bottom: 1em;">
<br />
Exploring microservices using Kubernetes!
<br />
<a href="https://github.com/Fuck-We-Ballerz/DM885"><strong>Explore the code»</strong></a>
</p>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#👋-about-the-project">👋 About The Project</a>
    </li>
    <li>
      <a href="#👷‍♂️-getting-started">👷‍♂️ Getting Started</a>
    </li>
    <li>
      <a href="#👨‍💻-assisting-dev-tools">👨‍💻 Assisting Dev Tools</a>
    </li>
    <li>
      <a href="#🏭-the-pipeline">🏭 The Pipeline</a>
    </li>
    <li>
        <a href="#🤝-contribute">🤝 Contribute</a>
    </li>
    <li>
        <a href="#✅-todo">✅ TODO</a>
    </li>
    <li>
        <a href="#📜-license">📜 License</a>
    </li>
  </ol>
</details>

## 👋 About The Project
This project is about creating a system that can check and provide feedback on programming assignments for students. The system is designed for students, teachers, and administrators. Students can upload their assignments and see the results.

The project is built using Kubernetes, a tool that helps us create a cloud-agnostic scalable system. The services in our system are designed to communicate securely and work independently. However, we have decided not to guarantee availability when the network is partitioned.

We are using existing tools for monitoring our system because they are reliable and well-maintained. These tools include:

* Grafana for dashboards, 
* Loki for logging, 
* Promtail for log collection, 
* Prometheus for metric scraping, 
* Node-exporter for server metrics, 
* Postgres-exporter for database metrics, and 
* cAdvisor for container resource metrics.

Regarding the infrastructure, we are using: 

* Adminer for database administration, 
* Keycloak for authentication, 
* Postgres for our databases, 
* and Ingress.

Our user interface is built using Django and Svelte. We chose different frameworks to allow our teams to work independently and reduce the need for communication. This means we can develop different parts of the system separately and connect them later. The user interface includes a panel for users and a panel for teachers.

Finally, our project is live on Google Cloud and can be accessed on [https://zeruscloud.com](https://zeruscloud.com) with additional services exposed on [/api]([https://zeruscloud.com](https://zeruscloud.com)), [/grafana](https://zeruscloud.com/grafana), or [/keycloak](https://zeruscloud.com/keycloak). 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 👷‍♂️ Getting Started
To run this project, you need to install Docker, Minikube, and Helm. Docker packages the application with its dependencies. Minikube allows running Kubernetes, which manages the application locally. Helm is for Kubernetes deployment.

Deploying locally has been simplified with the use of VSCode tasks. These tasks mimic a real pipeline, efficiently managing the necessary stages of deployment. This process includes the creation of helm Charts and the building custom Docker images that are referenced in the Kubernetes YAML files.

The tasks are designed with inherent dependencies, allowing the execution of a single task to trigger multiple stages, enhancing performance. The entire project can be deployed using the `minikube start` -> `Enable Ingress` -> `Helm Deploy` -> `minikube tunnel` tasks. However, there are several tasks available for specific needs:

* `Build Grafana`: For creating a custom Grafana image.
* `Build User`: For creating a custom User service image.
* `Build Teacher`: For creating a custom Teacher service image.
* `Enable Ingress`: Initialize ingress to use NGINX.
* `Deploy Deploy Infrastructure`: For deploying the infrastructure.
* `Deploy Deploy Monitoring`: For deploying the monitoring.
* `Deploy Deploy Frontend`: For deploying the frontend.
* `Deploy Helm`: For deploying the entire project.

A minimal values.yaml are provided for the three helm charts: `infrastructure`, `monitoring`, and `frontend`. For each of the three helm charts, a values-prod.yaml is provided to overwrite the default values.yaml for production.

We value ensuring that the development environment mirrors the production environment. The only differences are the values in `values-prod.yaml` and minimal if-statements in the templates. The services are configured to persist solely on the server they are run on.

This separation of environments is achieved by creating two secret configurations: one with hard-coded development secrets, and the other pulling secrets from the pipeline variables. This ensures a secure and efficient deployment process.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 👨‍💻 Assisting Dev Tools
We have integrated SonarCloud into our development process to ensure the consistent and efficient delivery of high-quality code. This code review tool seamlessly integrates with GitHub, enhancing our CI/CD workflow with quality gates. It provides immediate feedback on all pull requests, enabling us to maintain our coding standards. Anyone can access our SonarCloud dashboard [HERE](https://sonarcloud.io/organizations/fuck-we-ballerz). Besides analyzing pull requests, it is also possible to synchronize the SonarLint plugin in our IDE with the rules defined in our SonarCloud server. This ensures that the code violations identified by SonarLint match those detected by SonarCloud after pushing to the repository. We have not implemented this yet, but it could be a worthwhile addition to our workflow.

In addition, we have set up Dependabot to scan our repository for updates to packages and Docker images. Using outdated versions can often lead to vulnerabilities that have not been addressed. Dependabot helps mitigate these risks by automatically creating pull requests for these updates. We can then review and merge these updates as deemed appropriate. This ensures our codebase remains secure and up-to-date.

## 🏭 The Pipeline
The Pipeline automates the build, test and deployment stages. It is currently configured to function with google cloud kubernetes engine and its associated services, but can be migrated to any cloud platform.

__Prerequisite__:
Before you can run the workflow, you need to create a Google Cloud service account with the following permissions: 
**Kubernetes Engine Admin**
**Artifact Registry Admin**
**Remote Build Execution Admin**

Once You have created the account, you can export the service account secret key as a .json.

__Github Action secrets__:
To run the CI/CD Pipeline you will need to add some secrets in the `Github` -> `Settings` -> `Secrets & Variables`:

* **[GCR_HOSTNAME]**: The region that your GCKE cluster is deployed in.
* **[CLOUDSDK_CONTAINER_CLUSTER]**: Specifies the name of your cluster
* **[PROJECT_ID]**: Your Google Cloud Project ID
* **[GKE_SA_KEY]**: The contents of the secret key .json file.

__Running the workflow__:
Once everything has been set up according to the directions here, the workflow can be executed by going to `Github` -> `Actions` -> `CI/CD Pipeline` -> `Run Workflow` and then specify the branch to run the file on.
Alternatively, you can edit the part of the CI/CD Pipeline file that looks like this:
```yml
on:
  workflow_dispatch:
```
To specify a set of branches to automatically deploy on when a push to that branch occurs:
```yml
on:
  push:
    branches: [ "main", "otherBranch" ]
  pull_request:
    branches: [ "main", "otherBranch" ]
  workflow_dispatch:
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Api

To interface with the application there exists these following interfaces.

### Teacher

#### `GET /api/v1/teachers`

##### Description

Returns all the teachers

##### returns

```JSON
{
    "message": string,
    "teacher": [
        {
            "id": string,
            "name": string,
            "username": string,
            "is_paused": bool
        }
    ]
}
```


#### `GET /api/v1/teachers/[id]`


##### Description

Gets the information about a teacher

##### returns

```JSON
{
    "message": string,
    "teacher": [
        {
            "id": string,
            "name": string,
            "username": string,
            "is_paused": bool
        }
    ]
}
```

#### `GET /api/v1/teachers/[id]/submission/[submission_id]/`

##### Description

Get the status, logs and the result for a given submission

###### Unused

* `[id]`

###### returns

```JSON
[
    {
        "status": string,
        "stdout": string,
        "stderr": string,
        "result": string,
    }
]
```

#### `POST /api/v1/teachers/[id]/submission/[submission_id]/status`


##### Description

Sets the status of the given submission

##### Unused

* `[id]`

##### Body

```JSON
{
    "status": "pending" | "running" | "completed" | "failed" | "cancelled"
}
```

##### returns

```JSON
{
    "message": string
}
``` 

#### `GET /api/v1/teachers/[id]/courses`

##### Description

Returns a list of all the courses

##### Unused

* `[id]`

##### returns

```JSON
{
    "message": string,
    "courses": [
        {
            "id": number,
            "name": string,
        }
    ]
}
```

#### `POST /api/v1/teachers/[id]/assignment`

##### Description

Enrolls a student into the given assignment

##### Unused

* `[id]`

##### Body

```json
{
    student_id: [ number ]
}
```

##### returns

```JSON
{
    "message": string,
}
```

#### `GET /api/v1/teachers/[id]/assignment`

##### Description

Returns all the submissions made by a student for a given assignment

##### Unused

* `[id]`

##### Body

```json
{
    student_id: number,
    assignment_id: number,
}
```

##### returns

```JSON
{
    "message": string,
    "submissions": [
        {
            "id": number,
            "grade": string,
            "status": string,
            "submission": string,
            "submission_std": string,
            "submission_err": string,
            "submission_time": date,
            "assignment_id": number,
            "student_id": number,
        }
    ]
}
```

#### `DELETE /api/v1/teachers/[id]/assignment`

##### Description

Unenrolls a student from the given assignment

##### Unused

* `[id]`

##### Body

```json
{
    student_id: number,
    assignment_id: number,
}
```

##### returns

```JSON
{
    "message": string
}
```

#### `GET /api/v1/teachers/[id]/assignment/student`

##### Description

Returns all the submissions made by the given student for the given assignment

##### Unused

* `[id]`

##### Body

```json
{
    student_id: number,
    assignment_id: number,
}
```

##### returns

```JSON
{
    "message": string,
    "submissions": [
        {
            "id": number,
            "grade": string,
            "status": string,
            "submission": string,
            "submission_std": string,
            "submission_err": string,
            "submission_time": date,
            "assignment_id": number,
            "student_id": number,
        }
    ]
}
```

#### `POST /api/v1/teachers/[id]/assignment/student/[student_id]`

##### Description

Enrolls the specific student into the assignment

##### Unused

* `[id]`

##### Body

```json
{
    assignment_id: number,
}
```

##### returns

```JSON
{
    "message": string
}
```

#### `POST /api/v1/teachers/[id]/assignment/stop/[assignment_id]`

##### Description

Cancels the evaluation of all submissions for an assignment

##### Unused

* `[id]`

##### returns

```JSON
{
    "message": string
}
```

#### `POST /api/v1/teachers/[id]/assignment/pause/[assignment_id]`

##### Description

Pauses or unpauses an assignment.

##### Unused

* `[id]`

##### Body

```json
{
    is_visible: bool,
    assignment_id: number,
}
```

##### returns

```JSON
{
    "message": string,
    "is_visible": bool
}
```

#### `GET /api/v1/teachers/[id]/assignment/metadata`

##### Description

Returns a csv file containing the metadata for a given student for a given assignment

##### Unused

* `[id]`

##### Body

```json
{
    student_id: number,
    assignment_id: number,
}
```

##### returns

```JSON
{
    "message": string,
    "csv": string
}
```


#### `GET /api/v1/teachers/[id]/assignment/metadata/[assignment_id]`

##### Description

Returns a csv file containing the metadata for each student for a given assignment

##### Unused

* `[id]`

##### Body

```json
{
    assignment_id: number,
}
```

##### returns

```JSON
{
    "message": string,
    "csv": string
}
```


#### `GET /api/v1/teachers/[id]/assignment/logs`

##### Description

Retuns a zip file containing for a given student a folder and within that folder a file for stdout and another for stderr for a given assignment

##### Unused

* `[id]`

##### Body

```json
{
    assignment_id: number,
    student_id: number,
}
```

##### returns

```JSON
zil file blob
```


#### `GET /api/v1/teachers/[id]/assignment/logs/[assignment_id]`

##### Description

Retuns a zip file containing for each student a folder and within that folder a file for stdout and another for stderr for a given assignment

##### Unused

* `[id]`

##### returns

```JSON
zil file blob
```


#### `GET /api/v1/teachers/[id]/assignment/delete/[assignment_id]`

##### Description

Deletes an assignment and unassigns the teachers and students that were assigned to that assignment.

##### Unused

* `[id]`

##### returns

```JSON
{
    "message": string,
    deleted_assignment: number
}
```


## 🤝 Contribute
We have automated our local development process using VSCode tasks to create a simulated pipeline. This allows us to streamline our development workflow and ensure consistency across our team. Detailed instructions on how to set up and use these tasks is provided in the section <a href="#👷‍♂️-getting-started">Getting Started</a>.

For deployment on the Google Cloud Platform (GCP), we leverage GitHub Actions. This powerful tool allows us to build, test, and deploy our project directly from our GitHub repository to GCP. The advantage of this approach is twofold:

* It simplifies the deployment process, reducing the potential for human error.
* It ensures that our project on GCP is always up-to-date with the latest version of our code.

To maintain the integrity of our main branch, we have implemented branch protection rules. These rules help us manage the changes to the project and ensure that the main branch always has production-ready code. Each merge to the master branch triggers a deployment on the Google Cloud Platform (GCP) using GitHub Actions, and each pull request triggers a CI build on our [SonarCloud](https://sonarcloud.io/project/overview?id=Fuck-We-Ballerz_DM885). A PR must *always* pass the SonarCloud quality gate; otherwise, merge to master is disallowed.

We welcome contributions from all developers. Before contributing, please read through the above guidelines and ensure your changes adhere to them. Thank you for your interest in our project!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ✅ TODO
This section is dedicated to highlighting areas in the project that require further attention or improvement. These areas could be related to functionality, maintainability, or even critical aspects such as security. The following list provides a brief overview of the tasks that need to be addressed:

* Testing: Implement comprehensive testing strategies to ensure the application behaves as expected under various conditions. This includes unit tests, integration tests, and end-to-end tests.
* Upload of Files: Develop a secure and efficient file upload feature.
* Tracking of Submissions: Create a system to track user submissions. This could involve logging submission times, user details, and the status of the submission.
* Stop Submission: Implement a feature that allows users or administrators to stop or cancel a submission process. This could be useful in situations where an error has been identified, or a change needs to be made.

Remember, this is a living document. As the project evolves, new tasks may emerge and existing ones may become irrelevant.

For a succinct overview of the hard requirements, please refer to [PROJECT_TASKS.md](./PROJECT_TASKS.md), and our user stories are available [HERE](./USER_STORIES.pdf).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

