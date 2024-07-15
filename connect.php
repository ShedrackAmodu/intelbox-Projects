<?php

$con=mysqli_connect('localhost', 'root','','my store');

if(!$con){
    die(mysqli_error($con));
}

?>