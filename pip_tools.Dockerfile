FROM python:3.8.2-slim

WORKDIR /tmp

RUN pip install -U pip && pip install --no-cache-dir pip-tools

RUN useradd -m appuser
RUN chown -R appuser:appuser /home/appuser
USER appuser

CMD pip-compile -q --generate-hashes requirements.in && pip-compile -q --generate-hashes requirements-dev.in
