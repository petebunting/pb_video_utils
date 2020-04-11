FROM ubuntu:latest 

LABEL authors="Pete Bunting"
LABEL maintainer="petebunting@mac.com" 

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/miniconda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y apt-utils wget bzip2 curl git binutils vim imagemagick ffmpeg python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
    RUN ln -sf /usr/bin/python3 /usr/bin/python

COPY pb_video_utils .

RUN mkdir -p /opt/pb_video_utils
WORKDIR /opt/pb_video_utils
COPY pb_video_utils /opt/pb_video_utils
RUN python3 ./setup.py install

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

CMD [ "/bin/bash" ]

