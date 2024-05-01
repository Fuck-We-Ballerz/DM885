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
<a href="https://fuck-we-ballerz.github.io/DM885/" style="text-decoration:none;">
  <img src="https://img.shields.io/website?url=https%3A%2F%2Ffuck-we-ballerz.github.io%2FDM885%2F&style=for-the-badge" style="padding-bottom: 5px;"/>
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
* cAdvisor for container resource metrics (which is yet to be implemented).

Regarding the infrastructure, we are using: 

* Adminer for database administration, 
* Keycloak for authentication, 
* Postgres for our databases, 
* and Ingress (which is yet to be implemented).

Our user interface is built using Django and Svelte. We chose different frameworks to allow our teams to work independently and reduce the need for communication. This means we can develop different parts of the system separately and connect them later. The user interface includes a panel for users and a panel for teachers.

Finally, our project is live on Google Cloud and can be accessed through these URLs: [list]. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 👷‍♂️ Getting Started
To run this project, you need Docker and Minikube installed. Docker packages the application with its dependencies. Minikube allows running Kubernetes, which manages the application, locally.

Deploying locally has been simplified with the use of VSCode tasks. These tasks mimic a real pipeline, efficiently managing the necessary stages of deployment. This process includes the creation of secrets, configuration maps, and the building of custom Docker images that are referenced in the Kubernetes YAML files.

The tasks are designed with inherent dependencies, allowing the execution of a single task to trigger multiple stages, enhancing performance. The entire project can be deployed using the `deploy` task. However, there are several tasks available for specific needs:

* `ConfigMaps`: For managing configurations across multiple pods.
* `Secrets`: For storing sensitive data like API keys, passwords, etc.
* `Build Grafana`: For creating a custom Grafana image.
* `Build User`: For creating a custom User service image.
* `Build Teacher`: For creating a custom Teacher service image.
* `Init`: For initializing the deployment process.
* `Deploy`: For deploying the entire project.

We place a high value on ensuring that the development environment mirrors the production environment, with the only differences being the secrets used and the test data available. The services are configured to persist solely on the server they are run on.

This separation of environments is achieved by creating two secret configurations: one with hard-coded development secrets, and the other pulling secrets from the pipeline variables. This ensures a secure and efficient deployment process.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ✅ TODO

- Testing.
- Oploading af filer.
- Tracking af submission.
- Stop submission.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

