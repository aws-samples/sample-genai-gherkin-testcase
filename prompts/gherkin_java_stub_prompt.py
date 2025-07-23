gherkin_java_stub_prompt = """
You are tasked with generating Cucumber-based Java test scenarios from a given Gherkin Feature file. 
Your goal is to create a well-structured, executable Java code that implements the scenarios described in the feature file.

First, carefully read and analyze the following Gherkin Feature file:

<gherkin_feature>
{feature_file}
</gherkin_feature>

Now, follow these steps to generate the Cucumber-based Java test scenarios:

1. Parse the Gherkin Feature file:
   - Identify the Feature name
   - Extract all Scenarios and Scenario Outlines
   - For each Scenario and Scenario Outline, identify the Given, When, and Then steps

2. Create the Java class structure:
   - Generate a Java class named after the Feature, suffixed with "Steps" (e.g., "LoginFeatureSteps")
   - Import necessary Cucumber annotations (e.g., @Given, @When, @Then)
   - Import other required Java libraries
   - Import RestAssured, Jackson and Junit4 required Java libraries

3. Implement step definitions:
   - For each unique step in the Gherkin file, create a corresponding method in the Java class
   - Use appropriate Cucumber annotations (@Given, @When, @Then) with the step's text as a regular expression
   - Implement the method body with placeholder comments indicating the required action

4: Code Structure definitions: 
    - For path header and query parameters iterate over the maps with a switch statement identifying each key.
    - Use the RestAssured request object for assigning the path, query and header parameters.
    - Do not replace path parameters in the endpoint in the invoke api step.
    - For response validation ensure field is present only. 
    - Add ToDO wherever validation or assignment for review. 
    
    
    Refer below example for sample implementation:
    for (Map<String, String> row : rows) {{
            String paramName = row.get("parameter_name");
            String paramValue = row.get("value");

            switch (paramName) {{
                case "id":
                    // TODO: Replace with actual ID value when available
                    paramValue = "pid";
                    break;
            }}

            pathParams.put(paramName, paramValue);
            request.pathParam(paramName, paramValue);
        }}
    
    
5. Handle Scenario Outlines and Examples:
   - For Scenario Outlines, use parameterized step definitions
   - Include comments explaining how to handle the Examples table data

6. Follow these best practices and conventions:
   - Use descriptive method names for step definitions
   - Implement proper exception handling
   - Include TODO comments for steps that require further implementation
   - Use camelCase for method names and lowerCamelCase for variables

7. Output format:
   - Provide the complete Java code inside <java_code> tags
   - Include comments explaining the purpose of each method and any assumptions made
   - Ensure the code is properly formatted and indented for readability

Remember to generate executable Java code that accurately represents the scenarios in the Gherkin Feature file. 
Remember to use Switch statements for parameter and field validations while iterating the Maps. Do not wrap in conditions.

Remember to validate with field presence and TODO comments only for review.

Do not include any functionality that is not explicitly or implicitly stated in the feature file.

Please provide your generated Cucumber-based Java test scenarios based on the given Gherkin Feature file.
"""