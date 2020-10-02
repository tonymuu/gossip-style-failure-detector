
# MP1 README - Membership Protocol

## Basic tips

Read the specification document thoroughly on Coursera.

Create a high level design covering all scenarios / test cases before you start coding.

## How to submit for grading

To submit your work for autograding on the server, you need to generate a fresh submission token from the Coursera assignment web page. It's a text string you can copy and paste. Then, you need to run the submission script from your workspace directory:

```
python3 ./submit.py
```

It will ask you to enter your Coursera email address and the submission token.

## Local testing

### How do I test if my code passes all the test cases ?

Run the grader. Tests are initiated with `Tester.sh`. You can run this test suite locally like this:

```
$ chmod +x Tester.sh
$ ./Tester.sh
```

### How do I run the CRUD tests separately?

First, compile your project:

```
$ make clean
$ make
```

Then use one of these invocations:

```
$ ./Application ./testcases/create.conf
$ ./Application ./testcases/delete.conf
$ ./Application ./testcases/read.conf
$ ./Application ./testcases/update.conf
```

You may need to do `make clean && make` in between tests to make sure you have a clean run.
