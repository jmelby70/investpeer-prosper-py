#!/bin/bash
gcloud functions deploy function-investpeer-prosper-py \
--gen2 \
--source . \
--entry-point receive_message_function \
--trigger-topic investpeer-prosper-topic \
--runtime python312 \
--region us-central1