# API Specification

## API for external services
```yaml
paths:
  /classify:
    post:
      summary: classifies the provided traffic data object
      description: |
        Applications can request the classification of one 
        logged interaction from the IAM Solution. Returns the classification
        of the traffic object.
      consumes:
      - application/json
      produces: 
      - application/json
      parameters:
      - in: body
        name: features
        description: unlabeled traffic interaction that should be classified
        required: true
        schema:
          $ref: '#/definitions/LoggingData'
      responses:
        200:
          description: |
            Classification of data was successful, the resulting label is 
            returned.
          schema: 
            $ref: '#/definitions/Labels'
        400:
          description: Bad request
        409:
          description: No model deployed as classifier
        500:
          description: something went wrong in the server
  /misclassification:
    post:
      summary: Report misclassified traffic
      description: |
        Interface for Applications to report misclassified 
        interactions
      consumes: 
      - application/json
      parameters:
      - in: body
        name: trafficData
        description: the misclassified interaction that is reported
        schema:
          $ref: '#/definitions/Misclassification'
      responses:
        200:
          description: Misclassification acknowledged
        400:
          description: Bad request
        500:
          description: something went wrong in the server
definitions:
  LoggingData:
    type: string
    additionalProperties:
      type: number
    example: {"key": 789, "key2": 22}
  Labels:
    type: string
    enum: [harmless, attack]
  Date:
    type: number
  Misclassification:
    type: object
    required:
    - features
    - label
    - timestamp
    properties:
      features:
        $ref: '#/definitions/LoggingData'
      label:
        $ref: '#/definitions/Labels'
      timestamp:
        $ref: '#/definitions/Date'

```
## Backend For Frontend API
```yaml
paths:
  /models:
    get:
      tags:
      - model
      summary: returns names of all existing models
      produces:
      - application/json
      responses:
        200:
          description: the names of all existing models
          schema:
            type: array
            items:
              type: string
        500:
          description: something went wrong in the server
  /models/{modelname}/isActive:
    get:
      tags:
      - model
      summary: returns wheather model is currently used as classifier
      parameters:
      - in: path
        name: modelname
        description: name of model
        type: string
        required: true
      produces:
      - application/json
      responses:
        200:
          description: is model active
          schema:
            type: boolean
        404:
          description: model not found
        500:
          description: something went wrong in the server
  /models/{modelname}: 
    get:
      tags:
      - model
      summary: get the statistics of the model
      parameters:
      - in: path
        name: modelname
        description: name of model
        type: string
        required: true
      responses: 
        200:
          description: stats of the requested model
          schema: 
            $ref: '#/definitions/Statistics'
        404:
          description: model not found
        500:
          description: something went wrong in the server
    delete:
      tags:
      - model
      summary: delete a model
      parameters:
      - in: path
        name: modelname
        description: name of the model that should be deleted
        required: true
        type: string
      responses:
        200:
          description: OK, delete successfull
        404:
          description: model not found
        500:
          description: something went wrong in the server
  /models/train:
    post:
      tags:
      - model
      summary: create and train a new model
      description: |
        starts the training process for a newly created machine learning model
      parameters:
      - in: query
        name: modelName
        description: name of the new model
        type: string
        required: true
      - in: query
        name: filterName
        description: Name of the filter that should be used 
        required: true
        type: string
      responses:
        200:
          description: Training successful, response is accuracy with testing set
          schema:
            type: number
            example: 0.93
        400:
          description: invalid arguments
        500:
          description: something went wrong in the server
  /models/availability/{modelname}:
    get:
      tags:
      - model
      summary: check whether modelname is still available
      parameters:
      - in: path
        name: modelname
        description: the name for the new model
        type: string
        required: true
      responses:
        200:
          description: Response whether name is still available
          schema:
            type: boolean
            example: true
        500:
          description: something went wrong in the server
  /models/set/{modelname}:
    get:
      tags:
      - model
      summary: change the model responsible for classification
      parameters:
      - in: path
        name: modelname
        description: the model that should be used for classification
        type: string
        required: true
      responses:
        200:
          description: Model successfully changed
        404:
          description: Model could not be found or used
        500:
          description: something went wrong in the server
  /filters:
    get:
      tags:
      - feature set
      summary: get the names of all available feature sets
      responses:
        200:
          description: List with all available feature sets
          schema:
            type: array
            items:
              type: string
        500:
          description: something went wrong in the server
definitions:
  Statistics:
    type: object 
    required:
    - hits
    - misses
    properties:
      hits:
        type: integer
        minimum: 0
      misses:
        type: integer
        minimum: 0
```
