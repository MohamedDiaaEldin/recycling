# FrontEnd
  ## tools 
  - HTML
  - CSS 
  - javaScript
Figma front Design https://www.figma.com/file/9S59KDhNeIwBXwabEw0300/recycling?node-id=0%3A1




# Backend
  ## tools 
  - Flask - SqlAlchemy - flask migrate
  - Postgress Database
  
  ## End Points 
- customer POST 
  it returns {
            'status_code' :200 ,
            'success': True
   	     }


- login POST 
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


- /matrials GET 

- /categories GET

- /logout POST 

- /orders/<int:id>