gherkin_prompt_placeholder = """
Human:
You are tasked with generating unique Gherkin test scenarios for a specific API endpoint based on a given Swagger 
specification. Follow these instructions carefully to create comprehensive test scenarios.

First, you will be provided with the content of a Swagger specification file:

<swagger_file>
{spec}
</swagger_file>

Next, you will be given the specific API path,HTTP operation and HTTP response code to focus on:

API Path: {API_PATH}
HTTP Operation: {HTTP_OPERATION}
HTTP Response Code: {HTTP_RESPONSE_CODE}

Now, follow these steps to generate the Gherkin test scenarios:

1. Parse the Swagger file for following information:
   - title
   - url
   - Security Schemes Bearer type
   - Locate the specified API path,HTTP operation and HTTP response code in the Swagger file.

2. Parse the url to find following
   - server root (string ending with .de or .com etc)
   - apiurlpath (path after server root)

3. Identify API path,HTTP operation and HTTP response code in the Swagger file.

4. create one Gherkin scenario only for the given  API path, HTTP Operation and HTTP Response Code using the following template:

   ```gherkin
   Feature: [title]
   Scenario: [title] - resource [path] for response code and description
     Given with the server [root] for api [apiurlpath] and the resource [path]
     And for header parameters
       | parameter_name | value |
       | header1 | [HEADER-PARAMETER_NAME-PLACEHOLDER] |
     And for path parameters
       | parameter_name | value |
       | header1 | [PATH-PARAMETER_NAME-PLACEHOLDER] |
     And valid [type] authorization token
     And for query parameters
       | parameter_name | value |
       | query1 | [QUERY-PARAMETER_NAME-PLACEHOLDER] |
     And for body parameters
       | parameter_name | value |
       | body1 | [BODY-PARAMETER_NAME-PLACEHOLDER] |
     When I send a [HTTP_OPERATION] request to [API_PATH]
     Then the response status code should be [RESPONSE_CODE]
     And [Additional assertions based on the response] 

5. Example 1: 
Feature: Customer Management
Scenario: Customer Management - resource /customer for response code 200 OK
  Given with the server "https://xx.yy" for api "/customer/v1" and the resource "/customer"
  And for header parameters
    | parameter_name | value |
    | Accept-Language | [HEADER-ACCEPT-LANGUAGE-PLACEHOLDER] |
  And valid Bearer authorization token
  And for query parameters
    | parameter_name | value |
    | sort | [QUERY-SORT-PLACEHOLDER] |
    | limit | [QUERY-LIMIT-PLACEHOLDER] |
  When I send a GET request to "/customer"
  Then the response status code should be 200
  And the response should contain an array of Customer objects
  And for each Customer object
    | field           | value                      |
    | name              | [CUSTOMER-name-PLACEHOLDER]     |
    | address           | [CUSTOMER-address-PLACEHOLDER] |
    | age               | [CUSTOMER-age-PLACEHOLDER] |
  And for response headers
    | header_name | value |
    | Total | [RESPONSE-Total-PLACEHOLDER] |

6. Example 2:  
Feature: Customer Management
Scenario: Customer Management - resource /customer for response code 401 Unauthorized
  Given with the server "https://xx.yy" for api "/customer/v1" and the resource "/customer"
  And for header parameters
    | parameter_name | value |
    | Accept-Language | [HEADER-ACCEPT-LANGUAGE-PLACEHOLDER] |
  And invalid or missing Bearer authorization token
  And for query parameters
    | parameter_name | value |
    | limit | [QUERY-LIMIT-PLACEHOLDER] |
  And for body parameters
    | parameter_name | value |
    | name              | [CUSTOMER-name-PLACEHOLDER] |
    | address           | [CUSTOMER-address-PLACEHOLDER] |
    | age               | [CUSTOMER-age-PLACEHOLDER] |
  When I send a POST request to "/customer"
  Then the response status code should be 401
  And the response body should contain an Error object
  And for error object
    | field | value |
    | code | [ERROR-CODE-PLACEHOLDER] |
    | message | [ERROR-MESSAGE-PLACEHOLDER] |
    | status | [ERROR-STATUS-PLACEHOLDER] |

7. Include all header, path, and query parameters in the "Given" or "When" steps, using placeholder values as follows:
   - For header parameters: [HEADER-PARAMETER_NAME-PLACEHOLDER]
   - For query parameters: [QUERY-PARAMETER_NAME-PLACEHOLDER]
   - For path parameters: [PATH-PARAMETER_NAME-PLACEHOLDER]
   - For body parameters: [BODY-PARAMETER_NAME-PLACEHOLDER]

8. In the "Then" and "And" steps, assert the response objects using placeholder values as follows
   - For header parameters: [HEADER-PARAMETER_NAME-PLACEHOLDER]
   - For response contains an [object] assert the object field values as [OBJECT-Field-Placeholder]. For example [ERROR-STATUS-PLACEHOLDER] etc.
   - For response contains an Error object only assert code, message and status fields.

9. If the Swagger specification includes example responses or schemas, use them to create more specific assertions in your scenarios.

10. Output your generated Gherkin scenarios within <gherkin_scenarios> tags.


Remember to create scenarios only for response code, from the swagger specification provided as input. 

Remember to include all response schema parameters for the response object with placeholder values as per Swagger file.

Remember to exclude all scenarios that are not part of Swagger file.

Remember to exclude all scenarios that are not for given HTTP response code.


Assistant:
"""
