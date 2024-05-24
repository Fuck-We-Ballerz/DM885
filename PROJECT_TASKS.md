Project tasks
===

* Student

  - [ ] Create own profile that can be accessed with a username and password
  - [ ] Login into the system
  - [ ] Get the list of his or her assignments
  - [ ] Submit a solution to an assignment
  - [ ] Check if the evaluation of an assignment has been done
  - [ ] If not processed yet, cancel the submission of an assignment
  - [ ] See the results of the assignment
  - [ ] API access 
  - [x] GUI support

* Teacher

  - [x] Add an assignment
  - [x] Update the configuration information of the assignment (e.g., change the docker image, the visibility, etc.)
  - [x] Pause an assignment
  - [x] Delete an assignment
  - [x] Add or remove individual students from the assignment
  - [x] Add or remove in bulk students from the assignment
  - [x] Given an assignment and a student, get the list of student submissions
  - [x] Given a submission, get the status, output, and result of the submission
  - [x] Delete a programming assignment
  - [ ] Trigger the re-evaluation of a submission
  - [ ] Stop the evaluation of a submission
  - [ ] Given an assignment, stop the evaluation of all submissions
  - [x] Given an assignment, extract in bulk all the students’ submissions logs in a zip file (i.e., the text in logs.txt)
  - [x] Given an assignment, extract in bulk all the students’ submission metadata (e.g., student name, submission ID, submission time, result string contained in result.txt) in a CSV file
  - [x] Given an assignment and a student, extract in bulk all the student’s submissions logs in a zip file
  - [x] Given an assignment and a student, extract in bulk all the student’s submission metadata in a CSV file
  - [x] API access 
  - [x] GUI support

* Administrator

  - [x] monitoring and logging the platform using a dashboard
  - [x] add teachers
  - [x] pause a teacher
  - [x] delete a student or a teacher
  - [ ] API access 
  - [x] GUI support

* System Developer

  - [x] Use Continuous Integration and Deployment
  - [x] Infrastructure as a Code with an automatic DevOps pipeline
  - [x] Scalable, supporting multiple users exploiting if needed more resources in the cloud (note: an assignment validation requires a vCPU and therefore the number of vCPUs limits the number of parallel evaluations possible.)
  - [ ] Have tests to test the system (at least unit test, integration) <span style="color:orange">- PARTIALLY DONE: We have some tests but not part of the pipeline.</span>
  - [x] Security (proper credential management and common standard security practices enforced). Note that the evaluation of the docker must not tamper with the remaining part of the system since potentially the code of the students is non-trusted <span style="color:orange">- PARTIALLY DONE: DinD technically have some vulnerabilities</span>
  - [x] Provide user stories to explain how the system is intended to be used
  - [x] Provide minimal documentation to deploy and run the system
  - [x] The possibility to deploy on multi-clouds and avoid vendor lock-in is a plus
  - [x] A proper team organization and teamwork management are needed and a plus