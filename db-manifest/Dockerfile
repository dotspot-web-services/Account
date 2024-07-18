FROM postgres:13.10-alpine
RUN addgroup -S accgroup && adduser -S accuser -G accuser
RUN mkdir p ~/dbscripts
COPY DB/ dbscripts
RUN chown accuser dbscripts && chgrp accuser dbscripts
USER accuser
CMD ["nc", "-l", "1234"]
