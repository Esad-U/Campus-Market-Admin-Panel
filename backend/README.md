# Inside of this backend folder there are two main items:

## lambda_functions
### The folder that includes AWS Lambda Functions written in Python language are triggered by corresponding API endpoints as their names suggest.
+ admin-addOrRemoveCategory.py
+ admin-blockUserWithId.py
+ admin-deleteDataWithIdOnAnyTable.py
+ admin-getAllDataFromAnyTable.py
+ admin-unblockUserWithId.py
+ deleteProductOfUser.py
+ forgotPassword.py
+ getAllCategories.py
+ getProductById.py
+ getProductImage.py
+ getProductsOfUser.py
+ getUserCredentials.py
+ getUserImage.py
+ login.py
+ search.py
+ signup.py
+ uploadProduct.py
+ uploadProductImage.py
+ uploadUserImage.py
+ verifyAccount.py

## requirements.txt
### The text file used to specify the dependencies/libraries and their versions that are required for the project to run. 
+ To add all dependencies included in the requirements.txt file, run:
```
pip install -r requirements.txt
```
+ The packages/dependencies and their versions required for the project:
```
boto3==1.34.11
botocore==1.34.11
dnspython==2.4.2
jmespath==1.0.1
PyJWT==2.8.0
pymongo==4.6.1
python-dateutil==2.8.2
s3transfer==0.10.0
six==1.16.0
urllib3==2.0.7
```

## CampusMarketAPI-dev-oas30-api-spec.yaml
### The OpenAPI 3.0.1 API Specification/Configuration File in ".yaml" format.
+ The OpenAPI Specification (OAS) file is a standardized format used to describe and document RESTful APIs. It provides a machine-readable way to define the structure, operations, and behaviors of an API, allowing us to understand how to interact with it without delving into the implementation details. The specification, often written in YAML or JSON, includes information such as endpoints, parameters, request/response formats, authentication methods, and other relevant details. By using the OpenAPI Specification, us can easily generate documentation, client libraries, and server stubs, promoting consistency and interoperability across different programming languages and tools for our case it is AWS Cloud. It serves as a comprehensive contract for API communication, enhancing collaboration between us, and facilitating the development and consumption of APIs.

