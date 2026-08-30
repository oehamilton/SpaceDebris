# SpaceDebris

This repository is a first exercise in training and deploying a small convolutional neural network, not an operational space-debris detection system. Imagery that resolves individual on-orbit fragments such as bolts or heat-shield tiles was not available at useful resolution, and catalog tracking of debris is performed primarily with radar and specialized optical sensors that record unresolved points or streaks rather than nadir Earth-observation RGB. Sentinel-2 land tiles were therefore used as a stand-in, with synthetic high-contrast shapes added as proxy labels so the full loop—preprocessing, training a compact TensorFlow classifier, serving it from Flask, and presenting results in a React client—could be completed end to end. The work showed that a narrow visual task can run in a very small model and that the binding constraint is labeled data that matches the actual sensor. That limitation is what the project is meant to document, and it is the reason later work turned toward task-specific models small enough to run on drones, robots, and other edge devices, trained on an operator’s own examples rather than on unavailable catalog imagery

https://spacedebris.netlify.app/
*The api to the TinyLM has be decomissioned.

Satellite Image Classification for Space Debris Detection



Building a machine learning model to classify satellite images and detect space debris is a critical challenge in space exploration. The project uses Python, TensorFlow, and AWS to process and classify images, demonstrating your ability to develop and deploy AI-driven solutions. This project is relevant to space tech companies (e.g., SpaceX, Planet Labs) and can be adapted to energy (e.g., detecting defects in solar panels) or sciences (e.g., environmental monitoring).

The SpaceDebris project requires the following packages:

tensorflow==2.15.0
pandas==2.2.2
opencv-python==4.10.0
matplotlib==3.9.2
flask==3.0.3
boto3==1.35.24

# Space Debris Detection

A machine learning project to classify satellite images for space debris detection using TensorFlow, Flask, React, and AWS.

## Goals

- Train a CNN to identify space debris in satellite imagery.
- Deploy the model via AWS SageMaker with a React dashboard for visualization.

## Setup

1. Clone the repo: `git clone https://github.com/oehamilton/SpaceDebris`
2. Create a conda environment: `conda create -n spacedebris python=3.9`
3. Install dependencies: `conda install tensorflow pandas opencv matplotlib flask && pip install boto3`

## Progress

- [x] Initialized repo and project structure
- [x] Data preprocessing
- [x] CNN model training
- [x] Flask API Developed
- [x] React Front End Website Developed
- [x] Fask API deployed to Heroku
- [x] React Website deployed to Netlify
- [ ] Webiste vistor logged to database
