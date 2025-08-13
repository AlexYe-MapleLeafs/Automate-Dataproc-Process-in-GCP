# References:
#    Sample Image for Dataproc Serverless (https://cloud.google.com/dataproc-serverless/docs/guides/custom-containers)
#    Dockerfile Best Practice (https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

# Debian base images 
FROM gcr.io/google-containers/debian-base:v2.0.0

# Set PROXY
ENV http_proxy=http://gateway.bns:8080
ENV https_proxy=http://gateway.bns:8080 
ENV HTTP_PROXY=http://gateway.bns:8080 
ENV HTTPS_PROXY=http://gateway.bns:8080

# Metadata
LABEL name="Alex Ye"
LABEL email="alex.ye@*****.com"

# SSL Verification
ENV GIT_SSL_NO_VERIFY=1

# Suppress interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# (Required) Install utilities required by Spark scripts. 
RUN apt update && apt upgrade -y && apt install -y bash procps tini libjemalloc2

# Enable jemalloc2 as default memory allocator
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2

# (Optional) Add extra jars.
ENV SPARK_EXTRA_JARS_DIR=/opt/spark/jars/
ENV SPARK_EXTRA_CLASSPATH='/opt/spark/jars/*'
RUN mkdir -p "${SPARK_EXTRA_JARS_DIR}"
# comment out spark-3.2-bigquery-0.30.0.jar to avoid multiple source error.
# COPY ./dataproc/image/jars/spark-3.2-bigquery-0.30.0.jar "${SPARK_EXTRA_JARS_DIR}"
COPY ./dataproc/image/jars/gcs-connector-hadoop2-2.1.1.jar "${SPARK_EXTRA_JARS_DIR}"

# add script to container
COPY ./dataproc/image/scripts/ .

# (Optional) Install and configure Miniconda3.
ENV CONDA_HOME=/opt/miniconda3
ENV PYSPARK_PYTHON=${CONDA_HOME}/bin/python
ENV PATH=${CONDA_HOME}/bin:${PATH}
COPY ./dataproc/image/miniconda3/Miniconda3-py39_23.5.2-0-Linux-x86_64.sh .
RUN bash Miniconda3-py39_23.5.2-0-Linux-x86_64.sh -b -p /opt/miniconda3 \
  && ${CONDA_HOME}/bin/conda config --system --set always_yes True \
  && ${CONDA_HOME}/bin/conda config --system --set auto_update_conda False \
  && ${CONDA_HOME}/bin/conda config --system --prepend channels conda-forge \
  && ${CONDA_HOME}/bin/conda config --system --set channel_priority flexible

  # change strict to flexible to fix the error "libmamba Could not parse mod/etag header"
  # && ${CONDA_HOME}/bin/conda config --system --set channel_priority strict

# let container connect outside to download package
RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"

# (Optional) Install desired packages.
RUN pip install pylibpostal

# (Optional) Install Conda packages.
#
# The following packages are installed in the default image, it is strongly
# recommended to include all of them.
#
# Use mamba to install packages quickly.
RUN ${CONDA_HOME}/bin/conda install mamba -n base -c conda-forge \
    && ${CONDA_HOME}/bin/mamba install -q \
      conda \
      cython \
      fastavro \
      fastparquet \
      gcsfs \
      google-cloud-bigquery-storage \
      google-cloud-bigquery[pandas] \
      google-cloud-bigtable \
      google-cloud-container \
      google-cloud-datacatalog \
      google-cloud-dataproc \
      google-cloud-datastore \
      google-cloud-language \
      google-cloud-logging \
      google-cloud-monitoring \
      google-cloud-pubsub \
      google-cloud-redis \
      google-cloud-spanner \
      google-cloud-speech \
      google-cloud-storage \
      google-cloud-texttospeech \
      google-cloud-translate \
      google-cloud-vision \
      koalas \
      matplotlib \
      nltk \
      numba \
      numpy \
      openblas \
      orc \
      pandas \
      pyarrow \
      pysal \
      pytables \
      python \
      regex \
      requests \
      rtree \
      scikit-image \
      scikit-learn \
      scipy \
      seaborn \
      sqlalchemy \
      sympy \
      virtualenv 

# (Optional) Add extra Python modules.
ENV PYTHONPATH=/opt/python/packages
RUN mkdir -p "${PYTHONPATH}"
COPY ./dataproc/image/myutil/my_custom_util.py "${PYTHONPATH}"

# (Required) Create the 'spark' group/user.
# The GID and UID must be 1099. Home directory is required.
RUN groupadd -g 1099 spark
RUN useradd -u 1099 -g 1099 -d /home/spark -m spark
USER spark

# Unset PROXY
ENV http_proxy=
ENV https_proxy=
ENV HTTP_PROXY=
ENV HTTPS_PROXY=
