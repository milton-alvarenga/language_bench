FROM golang:1.23


# Install the github.com/lib/pq package globally
#RUN go install github.com/lib/pq@latest

# Add /go/bin to PATH
ENV PATH="/go/bin:${PATH}"

# Set the entrypoint to your startup script
ENTRYPOINT ["/app/start_go.sh"]