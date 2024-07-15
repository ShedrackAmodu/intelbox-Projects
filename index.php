<!--connect file-->
<?php
include('includes/connect.php');
?>

<!DOCTYPE HTML>
<html lang="en>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ecommerce Webiste using PHP and MySQL</title>
    <!-- bootstrap CSS link -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <!-- font awesome link -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.0/css/all.min.css" integrity="sha512-3PN6gfRNZEX4YFyz+sIyTF6pGlQiryJu9NlGhu9LrLMQ7eDjNgudQoFDK3WSNAayeIKc6B8WXXpo4a7HqxjKwg==" crossorigin="anonymous" referrerpolicy="no-referrer" />

    <!-- css file -->
    <link rel="stylesheet" href="style.css">

  </head>
<body>
    <!-- navbar -->
    <div class="container-fluid p-0">
        <!-- first child -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
  <div class="container-fluid">
    <img src="./Pictures/logo1.png" alt="" class="logo">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Products</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Register</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Contact</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#"><i class="fa fa-shopping-cart" aria-hidden="true"></i><sup>1</sup>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Total Price</a>
        </li>
      </ul>
      <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-light" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>
 
<!-- second child -->
 <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <u1 class="navbar-nav me-auto">
  <li class="nav-item">
          <a class="nav-link" href="#">Welcome Guest</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Login</a>
        </li>
  </u1>
 </nav>

<!-- third child -->
 <div class="bg-light">
  <h3 class="text-center">Hidden Store</h3>
  <p class="text-center text-italicize">Shop Smart, Live Better</p>
 </div>

 <!-- fourth child -->
<div class="row">
  <div class="col-md-10">
     <!-- products -->
    <div class="row">
     <div class="col-md-4 mb-2">
     <div class="card">
  <img src="./pictures/Sunglasses.jpg" class="card-img-top" alt="...">
   <div class="card-body">
      <h5 class="card-title">Sunglasses</h5>
      <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      <a href="#" class="btn btn-primary">Add to Cart</a>
      <a href="#" class="btn btn-dark">View More</a>
    </div>
  </div>
     </div>
    <div class="col-md-4 mb-2">
    <div class="card">
  <img src="./pictures/Teeshirt.jpg" class="card-img-top" alt="...">
    <div class="card-body">
      <h5 class="card-title">Designer Tee-shirt</h5>
      <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      <a href="#" class="btn btn-primary">Add to Cart</a>
      <a href="#" class="btn btn-dark">View More</a>
    </div>
  </div>  
      </div>
     <div class="col-md-4 mb-2">
     <div class="card">
  <img src="./pictures/whitechair.jpg" class="card-img-top" alt="...">
    <div class="card-body">
      <h5 class="card-title">White Chair</h5>
      <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      <a href="#" class="btn btn-primary">Add to Cart</a>
      <a href="#" class="btn btn-dark">View More</a>
    </div>
  </div>
    </div>
<div class="col-md-4 mb-2">
    <div class="card">
  <img src="./pictures/sneakers.jpg" class="card-img-top" alt="...">
    <div class="card-body">
      <h5 class="card-title">Nike Sneakers</h5>
      <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      <a href="#" class="btn btn-primary">Add to Cart</a>
      <a href="#" class="btn btn-dark">View More</a>
    </div>
  </div>
    </div>
  <div class="col-md-4 mb-2">
      <div class="card">
    <img src="./pictures/sofa.jpg" class="card-img-top" alt="...">
      <div class="card-body">
        <h5 class="card-title">Comfortable Sofa</h5>
        <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
        <a href="#" class="btn btn-primary">Add to Cart</a>
        <a href="#" class="btn btn-dark">View More</a>
      </div>
    </div>
         </div>
  <div class="col-md-4 mb-2">
      <div class="card">
    <img src="./pictures/table.jpg" class="card-img-top" alt="...">
      <div class="card-body">
        <h5 class="card-title">Wooden Table</h5>
        <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
        <a href="#" class="btn btn-primary">Add to Cart</a>
        <a href="#" class="btn btn-dark">View More</a>
      </div>
    </div>
  </div>
</div>
</div>

  <div class="col-md-2 bg-dark p-0">
     <!-- Brands to be displayed -->
    <ul class="navbar-nav me-auto text-center">
      <li class="nav-item bg-primary">
        <a href="#" class="nav-link text-light"><h4>Delivery Brands</h4></a>
      </li>
      <?php
      
$select_brands="Select * from 'brands'";
$result_brands=mysqli_query($con,$select_brands);
// $row_data=mysqli_fetch_assoc($result_brands);
// echo $row_data['brand_title'];
// echo $row_data['brand_title'];
while(row_data=mysqli_fetch_assoc($result_brands)){
  $brand_title=$row_data['brand_title'];
  $brand_id=$row_data['brand_id'];
  echo "<li class='nav-item'>
        <a href='index.php?brand=$brand_id' class='nav-link text-light'>$brand_title</a>
      </li>"
}
?>

    </ul>

    <!-- Categories to be displayed -->
    <ul class="navbar-nav me-auto text-center">
      <li class="nav-item bg-primary">
        <a href="#" class="nav-link text-light"><h4>Categories</h4></a>
      </li>
      <?php
      
      $select_categories="Select * from 'categories'";
      $result_categories=mysqli_query($con,$select_categories);
      // $row_data=mysqli_fetch_assoc($result_categories);
      // echo $row_data['category_title'];
      // echo $row_data['category_title'];
      while(row_data=mysqli_fetch_assoc($result_categories)){
        $category_title=$row_data['category_title'];
        $category_id=$row_data['category_id'];
        echo "<li class='nav-item'>
              <a href='index.php?category=$category_id' class='nav-link text-light'>$category_title</a>
            </li>"
      }
      ?>
    </ul>
  </div>
</div>


<!-- last child -->
<div class="bg-primary p-3 text-center text-light">
  <p>All rights reserved © Designed by Aisha & Princess - 2024</p>
</div>
</div>





<!-- bootstrap jss link -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>