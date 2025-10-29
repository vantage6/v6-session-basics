# basic python3 image as base
FROM harbor2.vantage6.ai/infrastructure/algorithm-base:5.0

# This is a placeholder that should be overloaded by invoking
# docker build with '--build-arg PKG_NAME=...'
ARG PKG_NAME="v6-session-basics"

# install federated algorithm
COPY . /app
# TODO v5+ should remove --prerelease=allow when official release is made
RUN uv pip install --system -e /app --prerelease=allow

# Set environment variable to make name of the package available within the
# docker image.
ENV PKG_NAME=${PKG_NAME}

# Tell docker to execute `wrap_algorithm()` when the image is run. This function
# will ensure that the algorithm method is called properly.
CMD python -c "from vantage6.algorithm.tools.wrap import wrap_algorithm; wrap_algorithm()"
