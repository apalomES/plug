FROM linuxserver/openssh-server

RUN apk update
RUN apk add gawk

COPY server_files /mnt/bes/pcm
RUN chmod -R 755 /mnt/bes/pcm