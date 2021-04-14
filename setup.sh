#!/bin/bash
git clone https://github.com/yskmt/pb.git
pip install -r requirements.txt
cd tools && python setup.py
