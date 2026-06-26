FROM jenkins/jenkins:lts

# Switch to root to install packages
USER root

# Install prerequisites
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg

# Add Docker's official GPG key (Modern secure approach)
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc

# Set up the repository dynamically for your Mac's architecture (arm64) and current Debian version
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker CLI
RUN apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
    apt-get clean

# Add the jenkins user to the docker group so it can run docker commands
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Drop back to the standard jenkins user
USER jenkins