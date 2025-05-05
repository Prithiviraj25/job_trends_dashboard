FROM quay.io/astronomer/astro-runtime:12.8.0
ONBUILD COPY packages.txt .
ONBUILD RUN /usr/local/bin/install-system-packages  