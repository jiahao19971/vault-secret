FROM ubuntu

WORKDIR /app

RUN apt update
RUN apt install python3 python3-pip -y
RUN apt update && apt install -y --no-install-recommends gpg curl lsb-release ca-certificates openssl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
      chmod +x ./kubectl && \
      mv ./kubectl /usr/local/bin/kubectl
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list
RUN apt update && apt install vlt -y --no-install-recommends
RUN apt clean && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "./secret.py"]


# COPY secret.sh secret.sh

# RUN chmod +x secret.sh

# CMD [ ./secret.sh ]