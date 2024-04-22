FROM --platform=linux/x86_64 python:3.11.6-slim


RUN echo "Hello from hillel" >> test.txt


CMD ["/bin/bash"]