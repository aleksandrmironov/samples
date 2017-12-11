# JSON_diff api #

## Basics ##
This api compares two JSON objects. It has three endpoints:
  * /v1/diff/\<ID\>/left - to upload fist JSON, base64encoded JSON format
  * /v1/diff/\<ID\>/right - to upload second JSON, base64encoded JSON format
  * /v1/diff/\<ID\> - to get diff operation result in JSON format
  
\<ID\> is an unique identificator of JSONSs to compare pair. It shoud be [A-Za-z0-9].


Api returns three results of comparison:
  * both JSONs have the same length and are equal:
    ```json
    {"foo":"bar"}
    ```
    and
    ```json
    {"foo":"bar"}
    ```
    Result JSON will be:
    ```json
    {
      "Diff": "None", 
      "SameSize": "True", 
      "Equal": "True"
    }  
    ```
  * JSONs have different length and are not equal:
    ```json
    {"foo":"bar", "john":"doe"}
    ```
    and
    ```json
    {"foo":"bar"}
    ```
    Result JSON will be:      
    ```json
    {
      "Diff": "Not applicable", 
      "SameSize": "False", 
      "Equal": "False"
    }
    ```
  * JSONs have the same length and are not equal:
    ```json
    {"foo":"bar"}
    ```
    and
    ```json
    {"teo":"bal"}
    ```  
    Result JSON will be:    
    ```json
    {
      "Diff": [
        {
          "Length": 2, 
          "Offset": 2
        }, 
        {
          "Length": 1, 
          "Offset": 10
        }
      ],
      "SameSize": "True", 
      "Equal": "False"
    }
    ```
  
## HOWTOs ##
    
#### How to upload JSON from linux shell   
HowTo upload base64 encoded JSON to left|right endpoint:
```bash
$ echo '{"foo":"bar"}' | base64 | curl -vvv --data @- http://example.com/v1/diff/aaa/left
```

#### How to SetUp Docker container with nginx+uwsgi ####
```bash
$ cd ./Docker && docker build -t nginx_uwsgi .
$ docker run -d --name nginx_uwsgi -p 80:80 -v ./samples/json_diff:/app nginx_uwsgi
```
