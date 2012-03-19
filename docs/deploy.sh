#!/bin/bash
make html && scp -r _build/html/* sf:public_html/houdini/ocean/docs
