FROM python:3.12-alpine

RUN apk update

RUN apk add --no-cache \
    cmake

RUN export CMAKE_POLICY_VERSION_MINIMUM=3.5


RUN apk add --no-cache \
    make \
    swig \
    bash \
    build-base \
    openblas-dev \
    #armadillo \
    armadillo-dev \
    cereal \
    #lz4-libs \
    lz4-dev \
    stb
    #liblz4

RUN apk add --no-cache \
    build-base \
    cmake \
    make \
    g++ \
    openblas-dev \
    lapack-dev

RUN apk add --no-cache \
    boost-dev \
    boost-program_options \
    boost-serialization \
    boost-unit_test_framework
    
RUN pip install --upgrade pip

RUN pip install \
PyYAML \
numpy \
timeout_decorator \
scipy \
scikit-learn \
simplejson

WORKDIR /usr/src/benchmarks
COPY . .
RUN apk add --no-cache bash dos2unix
RUN apk add --no-cache \
    openblas-dev \
    lapack-dev \
    gfortran
    
RUN dos2unix ./libraries/*.sh
RUN chmod +x ./libraries/*.sh
RUN find . -type f -exec sed -i 's/\r$//' {} \;
RUN apk add --no-cache wget curl

RUN make setup

RUN rm -rf ./libraries/*.tar.gz \
    ./libraries/*.zip \
    ./libraries/*.jar

#RUN make datasets

ENTRYPOINT ["/usr/bin/make", "run"]