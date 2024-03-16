# Bipartite and Tripartite Project

To install the required dependencies we created a `Makefile` to make this process easier, you need to run it in linux, or if you are using windows [follow this tutorial](https://stackoverflow.com/questions/2532234/how-to-run-a-makefile-in-windows). Follow the steps:

1. To execute the installation of the dependencies, for the frontend and backend execute the following command:
`make`

2. This command are going to create a virtualenvironment for the project and also install the node dependencies in their corresponding folders.

3. To run the backend server you can execute in a terminal:
`make run-backend`

4. To run the frontend you can execute in a different terminal:
`make run-frontend`

If you want to delete all the dependencies of the project just run:
`make clean`