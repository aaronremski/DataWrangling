# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import wptools

# Your code here: get the E.T. page object
# This cell make take a few seconds to run
page = wptools.page('E.T. the Extra-Terrestrial').get()

# Accessing the image attribute will return the images for this page
page.data['image']


