FROM python:3.7.0 as base

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /usr/local/app
ENV PYTHONPATH /usr/local/app

FROM base as test
ADD test_requirements.txt /tmp/
RUN pip install -r /tmp/test_requirements.txt
ADD . .
RUN py.test --cov=dependabot_access --cov-report=term-missing -n=auto
RUN flake8 --max-complexity=4


FROM base
ADD . .
ENTRYPOINT [ "python", "-m", "dependabot_access" ]