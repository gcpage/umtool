FROM scratch
ADD centos-7-docker.tar.xz /

LABEL name="CentOS Base Image" \
    vendor="CentOS" \
    license="GPLv2" \
    build-date="20170911"

CMD ["/bin/bash"]

RUN yum install -y ipmitool ;
    pip install -r requirements.txt
