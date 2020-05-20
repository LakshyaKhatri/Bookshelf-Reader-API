# Bookshelf-Reader-API
A browsable REST API built using Django REST Framework for recognizing book spines in an image.

Uploaded Image        | Result
:--------------------:|:---------------------------:
<img src="assets/spines.jpg" alt="Uploaded Image" width="300" />|<img src="assets/drawn_spines.jpeg" alt="Resulted Image" width="300" />

# Installation
* To run this project locally, clone or download this repository.
* Install requirements using:
    ```
    pip install -r requirements.txt
    ```
* Then run the migrations using:
    ```
    python3 manage.py makemigrations  
    python3 manage.py migrate
    ```
* Run the application:
    ```
    python3 manage.py runserver
    ```

# Usage
Add these URLs after your landing URL

Function                | url                    | Return  
:----------------------:|:----------------------:|:----------------------------------------------------:  
Upload Bookshelf Image  | /api/create-bookshelf/ | ID of the created uploaded image (Inside the Response Header)  
Spine Line Drawn Image  | /api/bookshelf/\<bookshelf-id\>/ | Spine line drawn image
Cropped Spines          | /api/spines/\<bookshelf-id\>/ | URLS of the cropped spines images

# Further Implementation

This project contains scrappers to scrap the information of all the books recognized in the spine image. Recognized spine can be sent for text recognition and then the recieved text can be uploaded to below URL's for scrapping the book's information information.

> *NOTE 1:* It's okay if the recognized text is not accurate. The scrapper will automatically find the correct book.  
> *NOTE 2:* The uloaded text is expected to be the book title \[and author name\].

Function                | url                    | Return  
:----------------------:|:----------------------:|:----------------------------------------------------:  
Upload book title text for scrapping information  | /api/add-book/ | ID of the created Book object (Inside the Response Header)
Get Book Information | /api/book/\<book-id\>/ | Scrapped book information.

# Client Side Application
If you want to see how can this REST API can be used at client side then checkout [Bookshelf Reader Android Application](https://github.com/LakshyaKhatri/Bookshelf-Reader)

# Liscence
MIT License

Copyright (c) 2020 Lakshya Khatri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
