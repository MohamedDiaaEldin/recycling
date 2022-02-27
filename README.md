# FrontEnd
  - ## tools 
    - HTML
    - CSS 
    - javaScript
  - [Figma Front Design](https://www.figma.com/file/9S59KDhNeIwBXwabEw0300/recycling?node-id=0%3A1)



# Backend

  - ## tools 
    - Flask - SqlAlchemy - flask migrate
    - Postgress Database


  - ## End Points 
    - /customer POST       
      <pre>           
          returns {
                    'status_code' :200 ,
                    'success': True
                  }
      </pre>

    - /login POST       
      <pre>
                   
          returns {
                    'success': True,
                    'status_code' : 200
                  }
            or 
                  {
                    'success' : False,
                    'status_sode': 401,
                    'message' :' unauthorized user'
                 } 
      </pre> 

    - /customer_email POST

      <pre>
         - request body 
         {
           "email" : "example.com"
         }
         - sucess response 
         
            {
                    'success': True,
                    'status_code' : 200
            }
         
      </pre>


    - /customer_email POST

      <pre>
         - request body 
              {
              "email"  : "mdiaan404@gmail.com",
              "otp" : "581484"
               }

        - sucess response 
         
            {
                    'success': True,
                    'status_code' : 200
            }
         
          
        -wrong otp response 
          {
            'success' : False,
            'status_sode': 401,
            'message' :"unauthorized user"
          }
      </pre>


      
    - /matrials GET 
      <pre> {
              "length": 3,
              "matrials": [
                  {
                      "id": 1,
                      "name": "plastic"
                  },
                  {
                      "id": 2,
                      "name": "glass"
                  },
                  {
                      "id": 3,
                      "name": "aluminum"
                  }
              ]
          }
      </pre>

    - /categories GET
      <pre> 
            {              
              "length": 4 , 
              "categories": [
                  {
                      "id": 1,
                      "name": "chair"
                  },
                  {
                      "id": 2,
                      "name": "bottle"
                  },
                  {
                      "id": 3,
                      "name": "window"
                  },
                  {
                      "id": 4,
                      "name": "table"
                  }
              ]
          }
      </pre>

    - /logout POST 

    - /orders/<int:id> 

    
  