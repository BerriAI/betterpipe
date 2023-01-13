# Betterpipe: Break free from limited observability in DevOps/MLOps platforms

Betterpipe is a package that allows you to pipe your .py file data to an external data warehouse, giving you complete control over your model's performance. With Betterpipe, you can easily troubleshoot issues and make informed decisions based on real-time data. 

## Installation
You can install Betterpipe via pip by running the following command:


`pip install betterpipe`


## Usage
To use Betterpipe, you'll first need to import the package and instantiate a DataPipe object, like so:
```python
import uuid
import os
import sys
from betterpipe import DataPipe

datapipe = DataPipe(user_email="johnsmith@gmail.com") # instantiates betterpipe instance and determines who to send the log url to
```

Then, you can use the @datapipe() decorator to log any console outputs from the functions you want to monitor, like this:

```@datapipe() # logs any console outputs
def my_function():
    print("This is a test.")
    print("This will be saved to a file.")

@datapipe() # logs any console outputs
def my_function_2():
    print("This is a test.")
    print("This will be saved to a file.")
```

Finally, you can call your functions as usual and end the session by calling the end_session() method on the DataPipe object, like so:

```my_function()
my_function_2()
datapipe.end_session() # pushes console output to s3 bucket
```

And that's it! With Betterpipe, you can easily monitor your functions' performance and troubleshoot any issues that may arise.

Please note that in order to use this package you need to configure the credentials for the external data warehouse.
