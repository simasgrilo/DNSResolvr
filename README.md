# DNS Resolvr

## A simple DNS resolver that supports CNAME and A records resolution recursively in Python.

The implementation follows RFC 1035 and RFC 1034, which respectively defines DNS and Domain Style names (DNS Record definition). Implementing a DNS resolver was an idea suggested by John Cricket in his [Coding Challenges substack](https://codingchallenges.fyi/challenges/intro). It is served as a Flask app listening on port 5000 by default

To start, you can cd to this repository's directory and either build the Dockerfile image with

    docker container build -t namespace/image_name:tag -f Dockerfile . 

and run it with

    docker container run -it -p <hostport>:5000 namespace/image_name:tag,

or install all dependencies locally:

    poetry install
    python3 main.py

or, if you prefer (i'd suggest this one if you're not using the Dockerfile), you can use [Conda](https://docs.conda.io/projects/conda/en/latest/index.html) to manage Python venvs easily and run it with:
    conda init newEnv
    conda install poetry
    conda run poetry install

and execute main.py file.