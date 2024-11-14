ARG BUILD_FROM
FROM $BUILD_FROM

# Add Python 3 and required packages
RUN apk add --no-cache python3

# Copy your code
COPY run.py /
COPY config.yaml /

# Set execute permissions
RUN chmod a+x /run.py

CMD [ "python3", "/run.py" ]