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
    
      <pre> - customer POST 
                returns {
                  'status_code' :200 ,
                  'success': True
                } 
      </pre>

    - login POST 
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

    - /matrials GET 

    - /categories GET

    - /logout POST 

    - /orders/<int:id> 

    
  