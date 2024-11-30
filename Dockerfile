# syntax=docker/dockerfile:1
FROM python:latest AS base

# Stage 1: Copy data
FROM base AS kaggle 
WORKDIR /app

RUN echo "TEST"







