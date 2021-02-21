FROM continuumio/miniconda:4.7.12

RUN conda create --name py36 python=3.6

ENV BASE_PATH=/app
RUN mkdir -p $BASE_PATH
WORKDIR $BASE_PATH

ENV PATH /opt/conda/envs/py36/bin:$PATH
ENV PYTHONPATH=$BASE_PATH

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "run.py"]