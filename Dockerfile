# syntax=docker/dockerfile:1.3
FROM registry.seculayer.com:31500/ape/python-base:py3.7 as builder
ARG app="/opt/app"

RUN pip3.7 install wheel
RUN git config --global http.sslVerify false

# pycmmn setup
# specific branch
RUN --mount=type=secret,id=token git clone -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" -b SLCAI-54-automl-module https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-dataconvertor.git $app/dataconverter
#RUN --mount=type=secret,id=token git clone -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-dataconvertor.git $app/dataconverter
WORKDIR $app/pycmmn
RUN pip3.7 install -r requirements.txt -t $app/pycmmn/lib
RUN python3.7 setup.py bdist_wheel

# dataconverter setup
# specific branch
RUN --mount=type=secret,id=token git clone -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" -b SLCAI-54-automl-module https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-dataconverter.git $app/dataconverter
#RUN --mount=type=secret,id=token git clone -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-dataconverter.git $app/dataconverter
WORKDIR $app/da
RUN pip3.7 install -r requirements.txt -t $app/dataconverter/lib
RUN python3.7 setup.py bdist_wheel

# dprs setup
# specific branch
RUN --mount=type=secret,id=token git clone -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" -b SLCAI-54-automl-module https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-dprs.git $app/dprs
#RUN --mount=type=secret,id=token git clone -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-dprs.git $app/dprs
WORKDIR $app/dprs
RUN pip3.7 install -r requirements.txt -t $app/dprs/lib
RUN python3.7 setup.py bdist_wheel


FROM registry.seculayer.com:31500/ape/python-base:py3.7 as app

ARG app="/opt/app"
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

# pycmmn install
RUN mkdir -p /eyeCloudAI/app/ape/pycmmn
WORKDIR /eyeCloudAI/app/ape/pycmmn

COPY --from=builder "$app/pycmmn/lib" /eyeCloudAI/app/ape/pycmmn/lib
COPY --from=builder "$app/pycmmn/dist/pycmmn-1.0.0-py3-none-any.whl" \
        /eyeCloudAI/app/ape/pycmmn/pycmmn-1.0.0-py3-none-any.whl

RUN pip3.7 install /eyeCloudAI/app/ape/pycmmn/pycmmn-1.0.0-py3-none-any.whl --no-dependencies  \
    -t /eyeCloudAI/app/ape/pycmmn/ \
    && rm /eyeCloudAI/app/ape/pycmmn/pycmmn-1.0.0-py3-none-any.whl

# dataconverter install
RUN mkdir -p /eyeCloudAI/app/ape/dataconverter
WORKDIR /eyeCloudAI/app/ape/dataconverter

COPY --from=builder "$app/dataconverter/lib" /eyeCloudAI/app/ape/dataconverter/lib
COPY --from=builder "$app/dataconverter/dist/dataconverter-1.0.0-py3-none-any.whl" \
        /eyeCloudAI/app/ape/dataconverter/dataconverter-1.0.0-py3-none-any.whl

RUN pip3.7 install /eyeCloudAI/app/ape/dataconverter/dataconverter-1.0.0-py3-none-any.whl --no-dependencies  \
    -t /eyeCloudAI/app/ape/dataconverter/ \
    && rm /eyeCloudAI/app/ape/dataconverter/dataconverter-1.0.0-py3-none-any.whl

# dprs install
RUN mkdir -p /eyeCloudAI/app/ape/dprs
WORKDIR /eyeCloudAI/app/ape/dprs

COPY ./dprs.sh /eyeCloudAI/app/ape/dprs
RUN chmod +x /eyeCloudAI/app/ape/dprs/dprs.sh

COPY --from=builder "$app/dprs/lib" /eyeCloudAI/app/ape/dprs/lib
COPY --from=builder "$app/dprs/dist/dprs-1.0.0-py3-none-any.whl" \
        /eyeCloudAI/app/ape/dprs/dprs-1.0.0-py3-none-any.whl

RUN pip3.7 install /eyeCloudAI/app/ape/dprs/dprs-1.0.0-py3-none-any.whl --no-dependencies  \
    -t /eyeCloudAI/app/ape/dprs \
    && rm /eyeCloudAI/app/ape/dprs/dprs-1.0.0-py3-none-any.whl

RUN groupadd -g 1000 aiuser
RUN useradd -r -u 1000 -g aiuser aiuser
RUN chown -R aiuser:aiuser /eyeCloudAI
USER aiuser

CMD []
